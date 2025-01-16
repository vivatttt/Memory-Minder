from aiogram.fsm.state import State, StatesGroup


class SimonForm(StatesGroup):
    game_started = State()
