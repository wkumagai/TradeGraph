import json
import logging
from typing import cast, Any

from langgraph.graph import END, START, StateGraph
# In newer langgraph, compiled graphs are returned by StateGraph.compile()
from typing_extensions import TypedDict

from tradegraph.core.base import BaseSubgraph
from tradegraph.features.write.writer_subgraph.input_data import (
    writer_subgraph_input_data,
)
from tradegraph.features.write.writer_subgraph.nodes.generate_note import generate_note
from tradegraph.features.write.writer_subgraph.nodes.paper_writing import WritingNode
from tradegraph.services.api_client.llm_client.llm_facade_client import LLM_MODEL
from tradegraph.utils.check_api_key import check_api_key
from tradegraph.utils.execution_timers import ExecutionTimeState, time_node
from tradegraph.utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
writer_timed = lambda f: time_node("writer_subgraph")(f)  # noqa: E731


class WriterSubgraphInputState(TypedDict):
    new_method: str
    experiment_strategy: str
    experiment_specification: str
    experiment_code: str
    output_text_data: str
    analysis_report: str
    image_file_name_list: list[str]


class WriterSubgraphHiddenState(TypedDict):
    note: str


class WriterSubgraphOutputState(TypedDict):
    paper_content: dict[str, str]


class WriterSubgraphState(
    WriterSubgraphInputState,
    WriterSubgraphHiddenState,
    WriterSubgraphOutputState,
    ExecutionTimeState,
):
    pass


class WriterSubgraph(BaseSubgraph):
    InputState = WriterSubgraphInputState
    OutputState = WriterSubgraphOutputState

    def __init__(
        self,
        llm_name: str,
        refine_round: int = 2,
    ):
        self.llm_name = llm_name
        self.refine_round = refine_round
        check_api_key(llm_api_key_check=True)

    @writer_timed
    def _generate_note(self, state: WriterSubgraphState) -> dict:
        note = generate_note(state=dict(state))
        return {"note": note}

    @writer_timed
    def _writeup(self, state: WriterSubgraphState) -> dict:
        paper_content = WritingNode(
            llm_name=cast(LLM_MODEL, self.llm_name),
            refine_round=self.refine_round,
        ).execute(
            note=state["note"],
        )
        return {"paper_content": paper_content}

    def build_graph(self) -> Any:
        graph_builder = StateGraph(WriterSubgraphState)
        graph_builder.add_node("generate_note", self._generate_note)
        graph_builder.add_node("writeup", self._writeup)

        graph_builder.add_edge(START, "generate_note")
        graph_builder.add_edge("generate_note", "writeup")
        graph_builder.add_edge("writeup", END)

        return graph_builder.compile()


def main():
    llm_name = "o3-mini-2025-01-31"
    refine_round = 1
    input = writer_subgraph_input_data

    result = WriterSubgraph(
        llm_name=llm_name,
        refine_round=refine_round,
    ).run(input)
    print(f"result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error running WriterSubgraph: {e}")
        raise
