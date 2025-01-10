import random

from backend.app.services.games.false_state import generate_game_data
from frontend.bot.games.false_state.schemas import GameData, GameDataExternalModel, Statements, UserGame


def shuffle_statements(wrong: list[str], correct: list[str]) -> tuple[set[int], str]:
    combined = wrong + correct
    random.shuffle(combined)
    wrong_statements_set = set(wrong)
    statements_string = ""
    wrong_inds = set()
    for i, statement in enumerate(combined):
        statements_string += f"{i + 1}. {statement}\n"
        if statement in wrong_statements_set:
            wrong_inds.add(i + 1)
    return {
        "wrong_inds": wrong_inds,
        "text": statements_string,
        "num": len(wrong) + len(correct)
    }

def prepare_game_data(data: GameDataExternalModel) -> GameData:
    print(*shuffle_statements(data.statements.wrong, data.statements.correct))
    return GameData(
        text=data.text,
        statements=Statements(
            **shuffle_statements(data.statements.wrong, data.statements.correct)
        )
    )

def get_new_user_game(*args, **kwargs) -> UserGame:
    game_data = GameDataExternalModel.model_validate(generate_game_data(*args, **kwargs))
    return UserGame(
        data=prepare_game_data(game_data)
    )
