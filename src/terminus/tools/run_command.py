import asyncio
import subprocess

from pydantic_ai import RunContext

from terminus import ui
from terminus.deps import ToolDeps
from terminus.session import session
from terminus.utils.command import extract_commands, is_command_allowed


async def run_command(ctx: RunContext[ToolDeps], command: str) -> str:
    """Run a shell command and return its output."""
    # Ignore for now, we already show panel
    #
    # if ctx.deps and ctx.deps.display_tool_status:
    #     await ctx.deps.display_tool_status("Run", command)

    if ctx.deps and ctx.deps.confirm_action:
        if not is_command_allowed(command, session.allowed_commands):
            command_display = ui.create_shell_syntax(command)

            if not await ctx.deps.confirm_action("Run Command", command_display):
                raise asyncio.CancelledError("Tool execution cancelled by user")

            commands = extract_commands(command)
            session.allowed_commands.update(commands)
        else:
            # If command is allowed, show as a status
            await ctx.deps.display_tool_status("Run", command)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = result.stdout + result.stderr
    return output if output else "(no output)"
