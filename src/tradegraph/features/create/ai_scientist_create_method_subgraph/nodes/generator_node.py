from logging import getLogger

from jinja2 import Environment

from tradegraph.create.create_method_subgraph.prompt.generator_node_prompt import (
    generator_node_prompt,
)
from tradegraph.typing.paper import CandidatePaperInfo
from tradegraph.utils.api_client.llm_facade_client import LLM_MODEL, LLMFacadeClient

logger = getLogger(__name__)


def generator_node(
    llm_name: LLM_MODEL,
    base_method_text: CandidatePaperInfo,
    add_method_texts: list[CandidatePaperInfo],
    client: LLMFacadeClient | None = None,
) -> str:
    if client is None:
        client = LLMFacadeClient(llm_name=llm_name)

    env = Environment()
    template = env.from_string(generator_node_prompt)
    data = {
        "base_method_text": base_method_text,
        "add_method_texts": add_method_texts,
    }
    messages = template.render(data)
    output, cost = client.generate(
        message=messages,
    )
    if output is None:
        raise ValueError("Error: No response from the model in generator_node.")
    return output
