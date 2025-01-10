import re


def is_valid_user_name(name: str) -> bool:
    """Имя может содержать только """
    pattern = r"^[a-zA-Z\u0400-\u04FF-]{2,20}$"
    match = re.fullmatch(pattern, name)
    return bool(match)
