from aiogram.fsm.state import State, StatesGroup


class WordsForm(StatesGroup):
    game_menu = State()
    game_started = State()
    gameplay = State()
    view_statistics = State()
    theme = State()
    words = State()
