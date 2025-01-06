from aiogram.fsm.state import StatesGroup, State

class NamesMemoryForm(StatesGroup):
    game_started = State()