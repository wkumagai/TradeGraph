import json
import logging
from typing import Any

from langgraph.graph import END, START, StateGraph
# In newer langgraph, compiled graphs are returned by StateGraph.compile()
from typing_extensions import TypedDict

from tradegraph.core.base import BaseSubgraph
from tradegraph.features.create.create_code_with_devin_subgraph.nodes.push_code_with_devin import (
    push_code_with_devin,
)
from tradegraph.features.create.nodes.check_devin_completion import (
    check_devin_completion,
)
from tradegraph.utils.check_api_key import check_api_key
from tradegraph.utils.execution_timers import ExecutionTimeState, time_node
from tradegraph.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

push_code_timed = lambda f: time_node("push_code_subgraph")(f)  # noqa: E731


class CreateCodeWithDevinSubgraphInputState(TypedDict):
    new_method: str
    experiment_code: str
    github_repository: str
    branch_name: str


class CreateCodeWithDevinSubgraphHiddenState(TypedDict): ...


class CreateCodeWithDevinSubgraphOutputState(TypedDict):
    push_completion: bool
    experiment_session_id: str
    experiment_devin_url: str
    experiment_iteration: int


class CreateCodeWithDevinSubgraphState(
    CreateCodeWithDevinSubgraphInputState,
    CreateCodeWithDevinSubgraphHiddenState,
    CreateCodeWithDevinSubgraphOutputState,
    ExecutionTimeState,
):
    pass


class CreateCodeWithDevinSubgraph(BaseSubgraph):
    InputState = CreateCodeWithDevinSubgraphInputState
    OutputState = CreateCodeWithDevinSubgraphOutputState

    def __init__(
        self,
    ):
        check_api_key(
            devin_api_key_check=True,
            github_personal_access_token_check=True,
        )

    @push_code_timed
    def _init_state(self, state: CreateCodeWithDevinSubgraphState) -> dict[str, int]:
        logger.info("---PushCodeSubgraph---")
        return {"experiment_iteration": 1}

    @push_code_timed
    def _push_code_with_devin_node(
        self, state: CreateCodeWithDevinSubgraphState
    ) -> dict[str, str]:
        experiment_session_id, experiment_devin_url = push_code_with_devin(
            github_repository=state["github_repository"],
            branch_name=state["branch_name"],
            new_method=state["new_method"],
            experiment_code=state["experiment_code"],
            experiment_iteration=state["experiment_iteration"],
        )
        return {
            "experiment_session_id": experiment_session_id,
            "experiment_devin_url": experiment_devin_url,
        }

    @push_code_timed
    def _check_devin_completion_node(
        self, state: CreateCodeWithDevinSubgraphState
    ) -> dict[str, bool]:
        result = check_devin_completion(
            session_id=state["experiment_session_id"],
        )
        if result is None:
            return {"push_completion": False}
        return {"push_completion": True}

    def build_graph(self) -> Any:
        graph_builder = StateGraph(CreateCodeWithDevinSubgraphState)
        graph_builder.add_node("init_state", self._init_state)
        graph_builder.add_node(
            "push_code_with_devin_node", self._push_code_with_devin_node
        )
        graph_builder.add_node(
            "check_devin_completion_node", self._check_devin_completion_node
        )

        graph_builder.add_edge(START, "init_state")
        graph_builder.add_edge("init_state", "push_code_with_devin_node")
        graph_builder.add_edge(
            "push_code_with_devin_node", "check_devin_completion_node"
        )
        graph_builder.add_edge("check_devin_completion_node", END)
        return graph_builder.compile()


def main():
    input = CreateCodeWithDevinSubgraphInputState(
        new_method="example_method",
        experiment_code="print('Hello, world!')",
        github_repository="auto-res2/test-tanaka-v11",
        branch_name="develop",
    )
    result = CreateCodeWithDevinSubgraph().run(input)
    print(f"result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error running PushCodeSubgraph: {e}")
        raise
