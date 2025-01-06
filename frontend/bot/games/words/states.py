from aiogram.fsm.state import StatesGroup, State

class WordsForm(StatesGroup):
    game_started = State()