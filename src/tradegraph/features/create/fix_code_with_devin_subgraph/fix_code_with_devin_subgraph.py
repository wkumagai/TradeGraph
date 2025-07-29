import logging
from typing import Literal, cast, Any

from langgraph.graph import END, START, StateGraph
# In newer langgraph, compiled graphs are returned by StateGraph.compile()
from typing_extensions import TypedDict

from tradegraph.core.base import BaseSubgraph
from tradegraph.features.create.fix_code_with_devin_subgraph.nodes.fix_code_with_devin import (
    fix_code_with_devin,
)
from tradegraph.features.create.fix_code_with_devin_subgraph.nodes.llm_decide import (
    llm_decide,
)
from tradegraph.features.create.fix_code_with_devin_subgraph.prompt.llm_decide import (
    llm_decide_prompt,
)
from tradegraph.features.create.nodes.check_devin_completion import (
    check_devin_completion,
)
from tradegraph.services.api_client.llm_client.llm_facade_client import LLM_MODEL
from tradegraph.utils.check_api_key import check_api_key
from tradegraph.utils.execution_timers import ExecutionTimeState, time_node
from tradegraph.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

fix_code_timed = lambda f: time_node("fix_code_subgraph")(f)  # noqa: E731


class FixCodeWithDevinSubgraphInputState(TypedDict):
    experiment_session_id: str
    output_text_data: str
    error_text_data: str
    executed_flag: Literal[
        True
    ]  # This should be True if the GitHub Actions workflow was executed successfully


class FixCodeWithDevinSubgraphHiddenState(TypedDict):
    judgment_result: bool


class FixCodeWithDevinSubgraphOutputState(TypedDict):
    output_text_data: str
    push_completion: bool
    executed_flag: bool


class FixCodeWithDevinSubgraphState(
    FixCodeWithDevinSubgraphInputState,
    FixCodeWithDevinSubgraphHiddenState,
    FixCodeWithDevinSubgraphOutputState,
    ExecutionTimeState,
):
    pass


class FixCodeWithDevinSubgraph(BaseSubgraph):
    InputState = FixCodeWithDevinSubgraphInputState
    OutputState = FixCodeWithDevinSubgraphOutputState

    def __init__(self, llm_name: str = "o3-mini-2025-01-31"):
        self.llm_name = llm_name
        check_api_key(
            llm_api_key_check=True,
            devin_api_key_check=True,
            github_personal_access_token_check=True,
        )

    @fix_code_timed
    def _llm_decide_node(self, state: FixCodeWithDevinSubgraphState) -> dict[str, bool]:
        if not state.get("executed_flag", True):
            raise ValueError(
                "Invalid state: GitHub Actions workflow was not executed (expected executed_flag == True)"
            )

        judgment_result = llm_decide(
            llm_name=cast(LLM_MODEL, self.llm_name),
            output_text_data=state["output_text_data"],
            error_text_data=state["error_text_data"],
            prompt_template=llm_decide_prompt,
        )
        return {
            "judgment_result": judgment_result,
        }

    @fix_code_timed
    def _fix_code_with_devin_node(self, state: FixCodeWithDevinSubgraphState) -> dict:
        fix_code_with_devin(
            session_id=state["experiment_session_id"],
            output_text_data=state["output_text_data"],
            error_text_data=state["error_text_data"],
        )
        return {"executed_flag": False}

    def _check_devin_completion_node(
        self, state: FixCodeWithDevinSubgraphState
    ) -> dict[str, bool]:
        result = check_devin_completion(
            session_id=state["experiment_session_id"],
        )
        if result is None:
            return {"push_completion": False}
        return {"push_completion": True}

    def _route_fix_or_end(self, state: FixCodeWithDevinSubgraphState) -> str:
        if state.get("judgment_result") is True:
            return "finish"
        return "fix_code_with_devin_node"

    def build_graph(self) -> Any:
        graph_builder = StateGraph(FixCodeWithDevinSubgraphState)
        graph_builder.add_node("llm_decide_node", self._llm_decide_node)
        graph_builder.add_node(
            "fix_code_with_devin_node", self._fix_code_with_devin_node
        )
        graph_builder.add_node(
            "check_devin_completion_node", self._check_devin_completion_node
        )

        graph_builder.add_edge(START, "llm_decide_node")
        graph_builder.add_conditional_edges(
            "llm_decide_node",
            self._route_fix_or_end,
            {
                "fix_code_with_devin_node": "fix_code_with_devin_node",
                "finish": END,
            },
        )
        graph_builder.add_edge(
            "fix_code_with_devin_node", "check_devin_completion_node"
        )
        graph_builder.add_edge("check_devin_completion_node", END)
        return graph_builder.compile()


# def main():
#     # input = {}
#     # result = FixCodeSubgraph().run(input)
#     print(f"result: {json.dumps(result, indent=2)}")

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         logger.error(f"Error running FixCodeSubgraph: {e}")
#         raise
