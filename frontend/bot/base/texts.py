from typing import Any

def escape_markdown_v2(text: str, symbols_to_exclude: Any = "") -> str:
        CHARS = r'[]()~`>#+-={}.!_*|'

        if not isinstance(symbols_to_exclude, set):
            symbols_to_exclude = set(symbols_to_exclude)

        escape_chars = set(CHARS) - symbols_to_exclude

        return ''.join(f"\\{char}" if char in escape_chars else char for char in text)