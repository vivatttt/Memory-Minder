from typing import Any


def escape_markdown_v2(text: str, symbols_to_exclude: Any = "") -> str:
        chars = r'[]()~`>#+-={}.!_*|'

        if not isinstance(symbols_to_exclude, set):
            symbols_to_exclude = set(symbols_to_exclude)

        escape_chars = set(chars) - symbols_to_exclude

        return ''.join(f"\\{char}" if char in escape_chars else char for char in text)


def markdown(text: list[str], symbols_to_exclude: Any = "") -> str:
    chars = r'[]()~`>#+-={}.!_*|'

    if not isinstance(symbols_to_exclude, set):
        symbols_to_exclude = set(symbols_to_exclude)

    escape_chars = set(chars) - symbols_to_exclude

    escaped_text = []

    for string in text:
        escaped_string = ""
        for char in string:
            if char in escape_chars:
                escaped_string += f"\\{char}"
            elif char == "\"":
                continue
            else:
                escaped_string += char
        escaped_text.append(escaped_string)

    return '\n'.join(escaped_text)