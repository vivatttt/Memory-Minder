from frontend.bot.games.n_back import NBackGame

def with_game_slug(st: str) -> str:
    return f"{NBackGame.slug}_{st}"
