"""Test MRKL agent decision making for string prompts."""

from typing import Dict

import pytest
from langchain.agents import load_tools
from langchain.llms import OpenAI

import langchain_contrib.tools  # noqa: F401
from langchain_contrib.chains.mrkl import MrklPickActionChain
from langchain_contrib.utils import current_directory

vcr = pytest.importorskip("vcr_langchain")


@vcr.use_cassette()
async def test_string_prompt() -> Dict[str, str]:
    """Check that the string MRKL prompt gets the LLM to pick an action as expected."""
    with current_directory():
        llm = OpenAI(temperature=0)  # type: ignore
        tools = load_tools(["persistent_terminal"], llm=llm)
        picker = MrklPickActionChain.from_tools(llm=llm, tools=tools)
        result = picker(
            {
                "input": (
                    "List the folders in the current directory. Enter into one of "
                    "them. List folders again."
                ),
                "agent_scratchpad": "",
            },
            return_only_outputs=True,
        )
        assert result["action_input"] == "ls"
        return result


if __name__ == "__main__":
    from langchain_visualizer import visualize

    visualize(test_string_prompt)
