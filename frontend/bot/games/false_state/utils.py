from frontend.bot.games.false_state import FalseStateGame

def with_game_slug(st: str) -> str:
    return f"{FalseStateGame.slug}_{st}"