import json
import logging
from typing import Any

from langgraph.graph import END, START, StateGraph
# In newer langgraph, compiled graphs are returned by StateGraph.compile()
from typing_extensions import TypedDict

from tradegraph.core.base import BaseSubgraph
from tradegraph.features.retrieve.generate_queries_subgraph.input_data import (
    generate_queries_subgraph_input_data,
)
from tradegraph.features.retrieve.generate_queries_subgraph.nodes.generate_queries import (
    generate_queries,
)
from tradegraph.features.retrieve.generate_queries_subgraph.prompt.generate_queries_prompt import (
    generate_queries_prompt,
)
from tradegraph.services.api_client.llm_client.llm_facade_client import LLM_MODEL
from tradegraph.utils.check_api_key import check_api_key
from tradegraph.utils.execution_timers import ExecutionTimeState, time_node
from tradegraph.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

generate_queries_str = "generate_queries_subgraph"
generate_queries_timed = lambda f: time_node(generate_queries_str)(f)  # noqa: E731


class GenerateQueriesInputState(TypedDict):
    research_topic: str


class GenerateQueriesHiddenState(TypedDict): ...


class GenerateQueriesOutputState(TypedDict):
    queries: list[str]  # TODO: Supporting semantic search


class GenerateQueriesState(
    GenerateQueriesInputState,
    GenerateQueriesHiddenState,
    GenerateQueriesOutputState,
    ExecutionTimeState,
): ...


class GenerateQueriesSubgraph(BaseSubgraph):
    InputState = GenerateQueriesInputState
    OutputState = GenerateQueriesOutputState

    def __init__(self, llm_name: LLM_MODEL):
        self.llm_name = llm_name
        check_api_key(llm_api_key_check=True)

    @generate_queries_timed
    def _generate_queries(self, state: GenerateQueriesState) -> dict[str, list[str]]:
        generated_queries = generate_queries(
            llm_name=self.llm_name,
            prompt_template=generate_queries_prompt,
            research_topic=state["research_topic"],
        )
        return {"queries": generated_queries}

    def build_graph(self) -> Any:
        graph_builder = StateGraph(GenerateQueriesState)
        graph_builder.add_node("generate_queries", self._generate_queries)
        graph_builder.add_edge(START, "generate_queries")
        graph_builder.add_edge("generate_queries", END)
        return graph_builder.compile()


def main():
    llm_name = "o3-mini-2025-01-31"
    input = generate_queries_subgraph_input_data
    result = GenerateQueriesSubgraph(
        llm_name=llm_name,
    ).run(input)
    print(f"result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error running GenerateQueriesSubgraph: {e}")
        raise
