from frontend.bot.games.names_memory import NamesMemoryGame

def with_game_slug(st: str) -> str:
    return f"{NamesMemoryGame.slug}_{st}"