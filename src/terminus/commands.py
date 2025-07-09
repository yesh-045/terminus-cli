"""Command handlers for terminus CLI slash commands."""

import asyncio
import logging

from terminus import ui
from terminus.session import session

log = logging.getLogger(__name__)


async def handle_dump():
    """Handle /dump command - show message history."""
    ui.dump(session.messages)


async def handle_yolo():
    """Handle /yolo command - toggle confirmation mode."""
    session.confirmation_enabled = not session.confirmation_enabled

    # Clear disabled confirmations when toggling
    if session.confirmation_enabled:
        session.disabled_confirmations.clear()

    status = "disabled (YOLO mode)" if not session.confirmation_enabled else "enabled"
    ui.info(f"Tool confirmations {status}")


async def handle_clear():
    """Handle /clear command - clear conversation history and screen."""
    # Clear the conversation history
    session.messages.clear()

    # Clear the screen and redisplay the banner
    ui.banner()

    # Show success message
    ui.success("Conversation history cleared")


async def handle_help():
    """Handle /help command - show available commands."""
    ui.help()


async def handle_debug_test(args: list[str]):
    """Handle /test command - trigger various UI states for testing (debug mode only)."""
    if not args:
        ui.info("Available test triggers:")
        ui.bullet("error - Trigger an error panel")
        ui.bullet("warning - Show a warning message")
        ui.bullet("success - Show a success message")
        ui.bullet("spinner - Test spinner behavior")
        ui.bullet("panel - Show various panel types")
        ui.bullet("confirm - Show confirmation dialog")
        return

    test_type = args[0].lower()

    if test_type == "error":
        try:
            raise ValueError("This is a test error to demonstrate error handling")
        except Exception as e:
            from terminus.utils.error import handle_error
            await handle_error(e, ui.display_error_panel)

    elif test_type == "warning":
        ui.warning("This is a test warning message")

    elif test_type == "success":
        ui.success("This is a test success message!")

    elif test_type == "spinner":
        ui.start_spinner("Testing spinner...", ui.SpinnerStyle.DEFAULT)
        await asyncio.sleep(2)
        ui.stop_spinner()
        ui.info("Spinner test completed")

    elif test_type == "panel":
        ui.display_info_panel("This is an info panel", "Information")
        ui.line()
        ui.display_tool_panel("Tool output goes here", "Test Tool", "Footer text")
        ui.line()
        ui.display_confirmation_panel("Are you sure you want to proceed?")

    elif test_type == "confirm":
        from terminus.agent import _create_confirmation_callback
        confirm = _create_confirmation_callback()
        result = await confirm(
            "Test Action: Delete File", "This would delete important.txt", "File: important.txt"
        )
        ui.info(f"Confirmation result: {result}")

    else:
        ui.warning(f"Unknown test type: {test_type}")


async def handle_command(user_input: str) -> bool:
    """Handle slash commands. Returns True if command was handled."""
    if not user_input.startswith("/"):
        return False

    parts = user_input.split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    handlers = {
        "/dump": handle_dump,
        "/yolo": handle_yolo,
        "/clear": handle_clear,
        "/help": handle_help,
    }

    if session.debug_enabled:
        handlers["/test"] = lambda: handle_debug_test(args)

    handler = handlers.get(command)
    if handler:
        await handler()
        return True

    return False
