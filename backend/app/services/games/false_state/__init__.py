from backend.app.services.games.false_state.generate_data import GenerateData

def generate_game_data(*args, **kwargs) -> dict[str, dict | str]:
    gd = GenerateData()
    return gd.get_game_data(*args, **kwargs)