from aiogram.fsm.state import State, StatesGroup


class NamesMemoryForm(StatesGroup):
    game_started = State()
    waiting_for_answer = State()
