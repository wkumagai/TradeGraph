import json
import logging
from typing import Any

from langgraph.graph import END, START, StateGraph
# In newer langgraph, compiled graphs are returned by StateGraph.compile()
from typing_extensions import TypedDict

from tradegraph.core.base import BaseSubgraph
from tradegraph.features.analysis.analytic_subgraph.input_data import (
    analytic_subgraph_input_data,
)
from tradegraph.features.analysis.analytic_subgraph.nodes.analytic_node import analytic_node
from tradegraph.services.api_client.llm_client.llm_facade_client import LLM_MODEL
from tradegraph.utils.check_api_key import check_api_key
from tradegraph.utils.execution_timers import ExecutionTimeState, time_node
from tradegraph.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

analytic_timed = lambda f: time_node("analytic_subgraph")(f)  # noqa: E731


class AnalyticSubgraphInputState(TypedDict):
    new_method: str
    experiment_strategy: str
    experiment_code: str
    output_text_data: str


class AnalyticSubgraphHiddenState(TypedDict):
    pass


class AnalyticSubgraphOutputState(TypedDict):
    analysis_report: str


class AnalyticSubgraphState(
    AnalyticSubgraphInputState,
    AnalyticSubgraphHiddenState,
    AnalyticSubgraphOutputState,
    ExecutionTimeState,
):
    pass


class AnalyticSubgraph(BaseSubgraph):
    InputState = AnalyticSubgraphInputState
    OutputState = AnalyticSubgraphOutputState

    def __init__(
        self,
        llm_name: LLM_MODEL,
    ):
        self.llm_name = llm_name
        check_api_key(llm_api_key_check=True)

    @analytic_timed
    def _analytic_node(self, state: AnalyticSubgraphState) -> dict:
        analysis_report = analytic_node(
            llm_name=self.llm_name,
            new_method=state["new_method"],
            experiment_strategy=state["experiment_strategy"],
            experiment_code=state["experiment_code"],
            output_text_data=state["output_text_data"],
        )
        return {"analysis_report": analysis_report}

    def build_graph(self) -> Any:
        graph_builder = StateGraph(AnalyticSubgraphState)
        graph_builder.add_node("analytic_node", self._analytic_node)

        graph_builder.add_edge(START, "analytic_node")
        graph_builder.add_edge("analytic_node", END)
        return graph_builder.compile()


def main():
    llm_name = "o3-mini-2025-01-31"
    input = analytic_subgraph_input_data

    result = AnalyticSubgraph(
        llm_name=llm_name,
    ).run(input)

    print(f"result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error running AnalyticSubgraph: {e}")
        raise
