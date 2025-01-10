from aiogram.fsm.state import State, StatesGroup


class WordsForm(StatesGroup):
    game_started = State()
