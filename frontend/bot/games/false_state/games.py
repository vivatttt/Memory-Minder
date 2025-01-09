from frontend.bot.games.false_state.schemas import UserGame

games_: dict[str, UserGame]  = {}

def get_games() -> dict[int, UserGame]:
    return games_

def get_user_game(user_id: int) -> UserGame:
    return games_[user_id]