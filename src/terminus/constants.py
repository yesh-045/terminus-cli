APP_NAME = "terminus"
APP_VERSION = "0.1.0"

# Simplified single model support
DEFAULT_MODEL = "google-gla:gemini-2.0-flash-exp"

# Non-destructive tools that should always be allowed without confirmation
ALLOWED_TOOLS = [
    "read_file",
    "find",
    "grep",
    "list_directory",
]

DEFAULT_USER_CONFIG = {
    "default_model": DEFAULT_MODEL,
    "env": {
        "GEMINI_API_KEY": "your-gemini-api-key",
    },
    "settings": {
        "allowed_commands": [
            "ls",
            "cat",
            "grep",
            "rg",
            "find",
            "pwd",
            "echo",
            "which",
            "head",
            "tail",
            "wc",
            "sort",
            "uniq",
            "diff",
            "tree",
            "file",
            "stat",
            "du",
            "df",
            "ps",
            "top",
            "env",
            "date",
            "whoami",
            "hostname",
            "uname",
            "id",
            "groups",
            "history",
        ],
    },
}
