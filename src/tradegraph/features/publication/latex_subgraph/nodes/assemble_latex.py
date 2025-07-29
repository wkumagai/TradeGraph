import os
import re
import shutil
import tempfile
from logging import getLogger

from pydantic import BaseModel

from tradegraph.services.api_client.llm_client.llm_facade_client import (
    LLM_MODEL,
    LLMFacadeClient,
)

logger = getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class LLMOutput(BaseModel):
    latex_full_text: str


class LatexNode:
    def __init__(
        self,
        llm_name: LLM_MODEL,
        save_dir: str,
        pdf_file_name: str = "generated_paper.pdf",
        template_file_name: str = "template.tex",
        max_iterations: int = 5,
        timeout: int = 30,
        client: LLMFacadeClient | None = None,
    ):
        self.llm_name = llm_name
        self.save_dir = save_dir

        self.max_iterations = max_iterations
        self.timeout = timeout
        self.client = client or LLMFacadeClient(self.llm_name)

        self.latex_template_dir = os.path.abspath(
            os.path.join(SCRIPT_DIR, "..", "latex")
        )

        self.pdf_file_name = pdf_file_name
        self.template_file_name = template_file_name

        self.latex_instance_file = os.path.join(
            self.save_dir, os.path.splitext(pdf_file_name)[0] + ".tex"
        )

    def _call_llm(self, prompt: str) -> str | None:
        system_prompt = """
You are a helpful LaTeX rewriting assistant.
The value of \"latex_full_text\" must contain the complete LaTeX text."""
        messages = system_prompt + prompt
        try:
            output, cost = self.client.structured_outputs(
                message=messages,
                data_model=LLMOutput,
            )
            return output["latex_full_text"]
        except Exception as e:
            logger.error(f"Error: No response from LLM in _call_llm: {e}")
            return None

    def _copy_template(self):
        shutil.copytree(self.latex_template_dir, self.save_dir, dirs_exist_ok=True)
        tmp = os.path.join(self.save_dir, self.template_file_name)
        shutil.copyfile(tmp, self.latex_instance_file)
        os.remove(tmp)

    def _fill_template(self, content: dict) -> str:
        with open(self.latex_instance_file, "r") as f:
            tex_text = f.read()

        for section, value in content.items():
            placeholder = f"{section.upper()} HERE"
            tex_text = tex_text.replace(placeholder, value)
        with open(self.latex_instance_file, "w") as f:
            f.write(tex_text)
        return tex_text

    def _write_references_bib(self, references_bib: dict[str, str]):
        bib_file_path = os.path.join(self.save_dir, "references.bib")
        try:
            with open(bib_file_path, "a", encoding="utf-8") as f:
                for entry in references_bib.values():
                    f.write("\n\n" + entry.strip())
            logger.info(
                f"Wrote {len(references_bib)} BibTeX entries to {bib_file_path}"
            )
        except Exception as e:
            logger.error(f"Failed to write references.bib: {e}")

    def _check_references(self, tex_text: str) -> str:
        cites = re.findall(r"\\cite[a-z]*{([^}]*)}", tex_text)
        bib_path = os.path.join(self.save_dir, "references.bib")
        if not os.path.exists(bib_path):
            raise FileNotFoundError(f"references.bib file is missing at: {bib_path}")

        with open(bib_path, "r") as f:
            bib_text = f.read()
        missing_cites = [cite for cite in cites if cite.strip() not in bib_text]

        if not missing_cites:
            logger.info("Reference check passed.")
            return tex_text

        logger.info(f"Missing references found: {missing_cites}")
        prompt = f""""\n
# LaTeX text
--------
{tex_text}
--------
# References.bib content
--------
{bib_text}
--------
The following reference is missing from references.bib: {missing_cites}.
Only modify the BibTeX content or add missing \\cite{{...}} commands if needed.

Do not remove, replace, or summarize any section of the LaTeX text such as Introduction, Method, or Results.
Do not comment out or rewrite any parts. Just fix the missing references.
Return the complete LaTeX document, including any bibtex changes."""
        llm_response = self._call_llm(prompt)
        if llm_response is None:
            raise RuntimeError(
                f"LLM failed to respond for missing references: {missing_cites}"
            )
        return llm_response

    def _check_figures(
        self,
        tex_text: str,
        figures_name: list[str],
        pattern: str = r"\\includegraphics.*?{(.*?)}",
    ) -> str:
        referenced_paths = re.findall(pattern, tex_text)
        referenced_figs = [os.path.basename(path) for path in referenced_paths]

        fig_to_use = [fig for fig in referenced_figs if fig in figures_name]

        if not fig_to_use:
            logger.info("No figures referenced in the LaTeX document.")
            return tex_text

        prompt = f"""\n
# LaTeX Text
--------
{tex_text}
--------
# Available Images
--------
{fig_to_use}
--------
Please modify and output the above Latex text based on the following instructions.
- Only “Available Images” are available. 
- If a figure is mentioned on Latex Text, please rewrite the content of Latex Text to cite it.
- Do not use diagrams that do not exist in “Available Images”.
- Return the complete LaTeX text."""

        tex_text = self._call_llm(prompt) or tex_text
        return tex_text

    def _check_duplicates(self, tex_text: str, patterns: dict[str, str]) -> str:
        for element_type, pattern in patterns.items():
            items = re.findall(pattern, tex_text)
            duplicates = {x for x in items if items.count(x) > 1}
            if duplicates:
                logger.info(f"Duplicate {element_type} found: {duplicates}.")
                prompt = f"""\n
# LaTeX text
--------
{tex_text}
--------
Duplicate {element_type} found: {", ".join(duplicates)}. Ensure any {element_type} is only included once. 
If duplicated, identify the best location for the {element_type} and remove any other.
Return the complete corrected LaTeX text with the duplicates fixed."""
                tex_text = self._call_llm(prompt) or tex_text
        return tex_text

    def _fix_latex_errors(self, tex_text: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tex", delete=True
            ) as tmp_file:
                tmp_file.write(tex_text)
                tmp_file.flush()

                ignored_warnings = "-n2 -n24 -n13 -n1 -n8 -n29 -n36 -n44"
                check_cmd = f"chktex {tmp_file.name} -q {ignored_warnings}"
                check_output = os.popen(check_cmd).read()

                if not check_output:
                    return tex_text

                error_messages = check_output.strip().split("\n")
                formatted_errors = "\n".join(
                    f"- {msg}" for msg in error_messages if msg
                )
                logger.info(f"LaTeX error detected: {formatted_errors}")

                prompt = f"""\n
# LaTeX text
--------
{tex_text}
--------
Please fix the following LaTeX errors: {formatted_errors}.      
Make the minimal fix required and do not remove or change any packages unnecessarily.
Pay attention to any accidental uses of HTML syntax, e.g. </end instead of \\end.

Return the complete corrected LaTeX text."""

                tex_text = self._call_llm(prompt) or tex_text
            return tex_text
        except FileNotFoundError:
            logger.error("chktex command not found. Skipping LaTeX checks.")
            return tex_text

    def assemble_latex(
        self,
        paper_tex_content: dict[str, str],
        references_bib: dict[str, str],
        figures_name: list[str],
    ) -> str:
        self._copy_template()
        tex_text = self._fill_template(paper_tex_content)
        self._write_references_bib(references_bib)

        for i in range(self.max_iterations):
            logger.info(f"=== Iteration {i + 1} ===")
            updated = tex_text
            updated = self._check_references(updated)
            updated = self._check_figures(updated, figures_name)
            updated = self._check_duplicates(
                updated,
                {
                    "figure": r"\\includegraphics.*?{(.*?)}",
                    "section header": r"\\section{([^}]*)}",
                },
            )
            # updated = self._fix_latex_errors(updated)

            if updated == tex_text:
                logger.info("All checks complete.")
                break
            tex_text = updated
        else:
            logger.warning("Max iterations reached.")

        with open(self.latex_instance_file, "w") as f:
            f.write(tex_text)

        return tex_text


if __name__ == "__main__":
    llm_name = "o3-mini-2025-01-31"
    tmp_dir = "/workspaces/airas/tmp"
    paper_tex_content = {
        "abstract": "This is a sample abstract.",
        "introduction": "This is a sample introduction.",
        "method": "This is a sample method.",
        "results": "These are the sample results.",
        "conclusion": "This is a sample conclusion.",
    }

    references_bib = {
        "ref1": """@article{ref1,
  title={Sample Reference},
  author={Doe, John},
  journal={Sample Journal},
  year={2025}
}"""
    }

    image_file_name_list = ["figure1.png", "figure2.jpg"]

    result = LatexNode(llm_name=llm_name, save_dir=tmp_dir).assemble_latex(
        paper_tex_content=paper_tex_content,
        references_bib=references_bib,
        figures_name=image_file_name_list,
    )
