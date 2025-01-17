"""Module defining a more flexible BaseTool."""
from __future__ import annotations

from typing import Any, Optional

from langchain.tools.base import BaseTool


class ZBaseTool(BaseTool):
    """A Tool wrapper class that allows for colors to be saved on init."""

    base_tool: Optional[BaseTool] = None
    """The actual tool that this class wraps around.

    If None, then this class is assumed to be overridden.
    """
    color: str = "blue"
    """The default color this tool will use for logging."""

    @classmethod
    def from_tool(cls, base_tool: BaseTool, **kwargs: Any) -> ZBaseTool:
        """Initialize from a base tool."""
        return cls(
            base_tool=base_tool,
            name=base_tool.name,
            description=base_tool.description,
            **kwargs,
        )

    def _run(self, tool_input: str) -> str:
        """Run the base tool."""
        assert self.base_tool is not None, "Either override _run or supply a base tool"
        return self.base_tool._run(tool_input)

    async def _arun(self, tool_input: str) -> str:
        """Asynchronously run the base tool."""
        assert self.base_tool is not None, "Either override _arun or supply a base tool"
        return await self.base_tool._arun(tool_input)

    def run(
        self,
        tool_input: str,
        verbose: Optional[bool] = None,
        start_color: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Run with the color specified at init if no colors specified now."""
        if start_color is None:
            start_color = self.color
        if color is None:
            color = self.color
        if verbose is None:
            verbose = self.verbose

        if self.base_tool:
            return self.base_tool.run(tool_input, verbose, start_color, color, **kwargs)
        else:
            return super().run(tool_input, verbose, start_color, color, **kwargs)

    async def arun(
        self,
        tool_input: str,
        verbose: Optional[bool] = None,
        start_color: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Run with the color specified at init if no colors specified now."""
        if start_color is None:
            start_color = self.color
        if color is None:
            color = self.color
        if verbose is None:
            verbose = self.verbose

        if self.base_tool:
            return await self.base_tool.arun(
                tool_input, verbose, start_color, color, **kwargs
            )
        else:
            return await super().arun(tool_input, verbose, start_color, color, **kwargs)
