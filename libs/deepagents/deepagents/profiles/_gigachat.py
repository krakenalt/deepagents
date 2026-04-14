"""GigaChat provider harness profile.

!!! warning

    This is an internal API subject to change without deprecation. It is not
    intended for external use or consumption.
"""

from deepagents.profiles._harness_profiles import _HarnessProfile, _register_harness_profile

_GIGACHAT_SYSTEM_PROMPT_SUFFIX = """
## GigaChat Tool Calling Constraints

- GigaChat supports a narrower tool-calling surface than some other providers.
- Never emit more than one tool call in a single assistant message.
- Prefer sequential tool use over parallel tool batches.
- When a task can be handled directly, answer directly instead of reaching for extra tools.
""".strip()

_GIGACHAT_TOOL_DESCRIPTION_OVERRIDES = {
    "ls": "List files in a directory. Use this before reading or editing files.",
    "read_file": (
        "Read a file from the filesystem. Use `offset` and `limit` for pagination "
        "on large files. Read the file before editing it."
    ),
    "write_file": "Create a new text file at the given path.",
    "edit_file": (
        "Replace exact text in a file. Read the file first and preserve the "
        "existing indentation and formatting."
    ),
    "glob": "Find files by glob pattern and return absolute paths.",
    "grep": (
        "Search for literal text across files. Use `output_mode` to control "
        "whether results return file paths, counts, or matching content."
    ),
    "execute": (
        "Run a shell command in the sandbox. Prefer built-in file tools over "
        "shell `find`, `grep`, or `cat`, and use absolute paths when possible."
    ),
}

_GIGACHAT_EXCLUDED_TOOLS = frozenset(
    {
        "ask_user",
        "compact_conversation",
        "task",
        "write_todos",
    }
)

_GIGACHAT_PROFILE = _HarnessProfile(
    init_kwargs={"allow_any_tool_choice_fallback": True},
    system_prompt_suffix=_GIGACHAT_SYSTEM_PROMPT_SUFFIX,
    tool_description_overrides=_GIGACHAT_TOOL_DESCRIPTION_OVERRIDES,
    excluded_tools=_GIGACHAT_EXCLUDED_TOOLS,
)

_register_harness_profile("gigachat", _GIGACHAT_PROFILE)
_register_harness_profile("giga", _GIGACHAT_PROFILE)
