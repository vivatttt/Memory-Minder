from frontend.bot.games.words import WordsGame


def with_game_slug(st: str) -> str:
    return f"{WordsGame.slug}_{st}"