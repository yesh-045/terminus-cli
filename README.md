# terminus

A lightweight terminal automation system with local AI agents.

## What it does

terminus is a simple CLI tool that brings AI-powered automation to your terminal. It uses local agents to help with file operations, shell commands, and basic development tasks. Think of it as a minimal, hackable alternative to complex IDE extensions.

## Core Features

- **File Operations**: Read, write, and update files with AI assistance
- **Shell Integration**: Execute terminal commands with smart confirmation
- **Session Memory**: Maintains conversation context across interactions
- **Local Agents**: Modular agent system (filesystem, shell, custom agents)
- **Git Integration**: Basic version control operations
- **Terminal-Native**: Designed for keyboard-driven workflows

## Installation

### Option 1: Using pipx (Recommended)
Install pipx if you don't have it:
```bash
pip install pipx
```

Then install terminus globally:
```bash
pipx install terminus-cli
```

This installs terminus in an isolated environment while making it available globally from any terminal.

### Option 2: Using pip
```bash
pip install terminus-cli
```

### Option 3: Development Installation
For development or local installation:
```bash
git clone <repository-url>
cd terminus-cli
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
pip install -e .
```

## Quick Start

1. Run terminus and configure your API key:
```bash
terminus
```

2. Start automating:
```
> create a python script that lists all .py files in this directory
> fix the bug in main.py line 45
> commit these changes with a descriptive message
```


## Available Commands

### Built-in Commands
- `/help` - Show comprehensive help guide with AI tools overview
- `/yolo` - Toggle tool confirmation prompts (DANGEROUS: auto-approves actions)
- `/clear` - Clear conversation history and start fresh
- `/dump` - Show detailed message history for debugging
- `exit` - Exit the application gracefully

### AI-Powered Natural Language Interface
Instead of memorizing commands, just ask the AI naturally:
- **"what tools are available?"** → Complete command reference
- **"show git examples"** → Git workflow examples  
- **"help with file operations"** → File operation guidance
- **"analyze this project"** → Project structure analysis
- **"find large files"** → System cleanup utilities

## Enhanced Tools Available (28 total)
Tool names:
1. read_file - Read file contents  
2. write_file - Create/write files  
3. update_file - Update specific content in files  
4. run_command - Execute shell commands  
5. git_add - Stage files for commit  
6. git_commit - Commit staged changes  
7. find - Find files by name pattern  
8. grep - Search text in files  
9. list_directory - List directory contents  
10. change_directory - Navigate directories (session-aware)  
11. get_current_directory - Show current working directory  
12. run_in_directory - Execute commands in specific directories  
13. find_by_extension - Find files by extension (.gitignore aware)  
14. list_extensions - List all file extensions in project  
15. summarize_code - Analyze and summarize code files  
16. analyze_project_structure - Complete project overview  
17. system_info - Comprehensive system information  
18. quick_stats - File/directory statistics  
19. create_project_template - Generate project scaffolding  
20. find_large_files - Locate large files for cleanup  
21. clean_temp_files - Clean temporary and cache files  
22. git_status_enhanced - Enhanced visual git status  
23. package_info - Display package manifest information  
24. quick_commit - Fast git commit workflow  
25. search_todos - Find TODO/FIXME/HACK comments  
26. list_all_commands - Complete command reference with examples  
27. command_examples - Practical usage examples by category  
28. quick_help - Context-specific help and guidance  


## Example Usage

```bash
$ terminus
> analyze the code structure and suggest improvements
> create unit tests for the database module  
> refactor the config parser to use dataclasses
> /clear  # start fresh conversation
```

## Requirements

- Python 3.10+
- Google Gemini API key

## License

MIT
