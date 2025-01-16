from aiogram.fsm.state import State, StatesGroup


class FalseStateForm(StatesGroup):
    game_started = State()
