from aiogram.fsm.state import State, StatesGroup


class NBackForm(StatesGroup):
    game_started = State()

class ChangeNState(StatesGroup):
    waiting_for_n = State()
