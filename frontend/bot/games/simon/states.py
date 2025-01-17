from aiogram.fsm.state import StatesGroup, State


class SimonForm(StatesGroup):
    game_started = State()
    get_command = State()
    description = State()
    simon_game = State()
