# your_package/core/base.py
from abc import ABC, abstractmethod
from typing import Any, TypedDict

# In newer langgraph, compiled graphs are returned by StateGraph.compile()


class BaseSubgraph(ABC):
    InputState: type[TypedDict]
    OutputState: type[TypedDict]

    def __init__(self, name: str = None):
        """Initialize the base subgraph with optional name."""
        self.name = name or self.__class__.__name__

    @abstractmethod
    def build_graph(self) -> Any: ...

    def run(self, state: dict[str, Any], config: dict | None = None) -> dict[str, Any]:
        if hasattr(self, 'InputState'):
            input_state_keys = self.InputState.__annotations__.keys()
            input_state = {k: state[k] for k in input_state_keys if k in state}
        else:
            input_state = state
            
        if config is None:
            config = {"recursion_limit": 200}
            
        result = self.build_graph().invoke(input_state, config=config)
        
        if hasattr(self, 'OutputState'):
            output_state_keys = self.OutputState.__annotations__.keys()
            output_state = {k: result[k] for k in output_state_keys if k in result}
        else:
            output_state = result

        cleaned_state = {k: v for k, v in state.items() if k != "subgraph_name"}
        return {
            "subgraph_name": self.__class__.__name__,
            **cleaned_state,
            **output_state,
        }
