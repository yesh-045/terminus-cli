import logging
from pathlib import Path
from typing import Any, Optional

from pydantic_ai import Agent, CallToolsNode
from pydantic_ai.messages import (
    ModelRequest,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)

from terminus import ui
from terminus.constants import DEFAULT_MODEL
from terminus.deps import ToolDeps
from terminus.session import session
from terminus.tools import TOOLS
from terminus.utils.error import ErrorContext
from terminus.utils.guide import get_guide

log = logging.getLogger(__name__)


def _get_prompt(name: str) -> str:
    try:
        prompt_path = Path(__file__).parent / "prompts" / f"{name}.txt"
        return prompt_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return f"Error: Prompt file '{name}.txt' not found"


async def _process_node(node):
    # from rich import print
    # print('-' * 20)
    # print(node)
    # print('-' * 20)

    if isinstance(node, CallToolsNode):
        for part in node.model_response.parts:
            if isinstance(part, ToolCallPart):
                log.debug(f"Calling tool: {part.tool_name}")

            # I cant' find a definitive way to check if a text part is a "thinking" response
            # or not, but majority of the time they are accompanied by other tool calls.
            # Using that as a basis for showing "thinking" messages.
            if isinstance(part, TextPart) and len(node.model_response.parts) > 1:
                ui.stop_spinner()
                ui.thinking(part.content)
                ui.start_spinner()

    if hasattr(node, "request"):
        session.messages.append(node.request)
        log.debug("Added request to message history")

        for part in node.request.parts:
            if part.part_kind == "retry-prompt":
                if session.spinner:
                    session.spinner.stop()
                error_msg = (
                    part.content
                    if hasattr(part, "content") and isinstance(part.content, str)
                    else "Trying a different approach"
                )
                ui.muted(f"{error_msg}")
                if session.spinner:
                    session.spinner.start()

    if hasattr(node, "model_response"):
        session.messages.append(node.model_response)
        log.debug("Added model response to message history")


def get_or_create_agent():
    if "default" not in session.agents:
        base_agent = Agent(
            model=DEFAULT_MODEL,
            system_prompt=_get_prompt("system"),
            tools=TOOLS,
            deps_type=ToolDeps,
        )
        session.agents["default"] = base_agent
    return session.agents["default"]


def _create_confirmation_callback():
    async def confirm(title: str, preview: Any, footer: Optional[str] = None) -> bool:
        tool_name = title.split(":")[0].strip() if ":" in title else title

        if not session.confirmation_enabled or tool_name in session.disabled_confirmations:
            return True

        if session.spinner:
            session.spinner.stop()

        ui.display_tool_panel(preview, title, footer)

        # Display confirmation options without using a panel, but still
        # indented by two spaces so they line up with other panel content.
        options = (
            ("y", "Yes, execute this tool"),
            ("a", "Always allow this tool"),
            ("n", "No, cancel this execution"),
        )

        # Add a single blank line before options
        ui.console.print()

        for key, description in options:
            ui.console.print(f"  {key}: {description}", style=ui.colors.warning)

        while True:
            choice = ui.console.input("  Continue? (y): ").lower().strip()

            if choice == "" or choice in ["y", "yes"]:
                ui.line()
                ui.reset_output_context()  # Reset after user input
                if session.spinner:
                    session.spinner.start()
                return True
            elif choice in ["a", "always"]:
                session.disabled_confirmations.add(tool_name)
                ui.line()
                ui.reset_output_context()  # Reset after user input
                if session.spinner:
                    session.spinner.start()
                return True
            elif choice in ["n", "no"]:
                ui.reset_output_context()  # Reset after user input
                return False

    return confirm


def _create_display_tool_status_callback():
    async def display(title: str, *args: Any, **kwargs: Any) -> None:
        """
        Display the current tool status.

        Args:
            title: str
            *args: Any
            **kwargs: Any
                Keyword arguments passed to the tool. These will be rendered in the
                form ``key=value`` in the output.
        """
        if session.spinner:
            session.spinner.stop()

        parts = []
        if args:
            parts.extend(str(arg) for arg in args)
        if kwargs:
            parts.extend(f"{k}={v}" for k, v in kwargs.items())

        arg_str = ", ".join(parts)
        ui.info(f"{title}({arg_str})")

        if session.spinner:
            session.spinner.start()

    return display


def _patch_history_on_error(error_message: str):
    """
    Patches the message history with a ToolReturnPart on error.
    """
    if not session.messages:
        return

    last_message = session.messages[-1]

    if not (
        hasattr(last_message, "kind")
        and last_message.kind == "response"
        and hasattr(last_message, "parts")
    ):
        return

    last_tool_call = None
    for part in reversed(last_message.parts):
        if hasattr(part, "part_kind") and part.part_kind == "tool-call":
            last_tool_call = part
            break

    if last_tool_call:
        tool_return = ToolReturnPart(
            tool_name=last_tool_call.tool_name,
            tool_call_id=last_tool_call.tool_call_id,
            content=error_message,
        )
        session.messages.append(ModelRequest(parts=[tool_return]))


async def process_request(message: str):
    log.debug(f"Processing request: {message.replace('\n', ' ')[:100]}...")

    agent = get_or_create_agent()

    mh = session.messages.copy()
    log.debug(f"Message history size: {len(mh)}")

    project_guide = get_guide(session)
    if project_guide:
        guide_message = ModelRequest(parts=[UserPromptPart(content=project_guide)])
        mh.insert(0, guide_message)
        log.debug("Prepended project guide to message history")

    deps = ToolDeps(
        confirm_action=_create_confirmation_callback(),
        display_tool_status=_create_display_tool_status_callback(),
    )

    ctx = ErrorContext("agent", ui)
    ctx.add_cleanup(lambda e: _patch_history_on_error(str(e)))

    try:
        async with agent.iter(message, deps=deps, message_history=mh) as agent_run:
            async for node in agent_run:
                await _process_node(node)

            result = agent_run.result.output
            log.debug(f"Agent response: {result.replace('\n', ' ')[:100]}...")
            return result
    except Exception as e:
        return await ctx.handle(e)
