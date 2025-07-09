from pydantic_ai import Tool

from terminus.tools.find import find
from terminus.tools.git import git_add, git_commit
from terminus.tools.grep import grep
from terminus.tools.list import list_directory
from terminus.tools.read_file import read_file
from terminus.tools.run_command import run_command
from terminus.tools.update_file import update_file
from terminus.tools.write_file import write_file

# Import new tools
from terminus.tools.directory import change_directory, get_current_directory, run_in_directory
from terminus.tools.file_discovery import find_by_extension, list_extensions
from terminus.tools.code_analysis import summarize_code, analyze_project_structure

from terminus.tools.system_utilities import (
    system_info,
    quick_stats,
    create_project_template,
    find_large_files,
    clean_temp_files,
)
from terminus.tools.dev_workflow import (
    git_status_enhanced,
    package_info,
    quick_commit,
    search_todos,
)
from terminus.tools.help_system import (
    list_all_commands,
    command_examples,
    quick_help,
)


def create_tools():
    """Create Tool instances for all tools."""
    return [
        Tool(read_file),
        Tool(write_file),
        Tool(update_file),
        Tool(run_command),
        Tool(git_add),
        Tool(git_commit),
        Tool(find),
        Tool(grep),
        Tool(list_directory),
        # New session-aware tools
        Tool(change_directory),
        Tool(get_current_directory),
        Tool(run_in_directory),
        Tool(find_by_extension),
        Tool(list_extensions),
        Tool(summarize_code),
        Tool(analyze_project_structure),
        # System utilities
        Tool(system_info),
        Tool(quick_stats),
        Tool(create_project_template),
        Tool(find_large_files),
        Tool(clean_temp_files),
        # Development workflow
        Tool(git_status_enhanced),
        Tool(package_info),
        Tool(quick_commit),
        Tool(search_todos),
        # Help and documentation
        Tool(list_all_commands),
        Tool(command_examples),
        Tool(quick_help),
    ]
