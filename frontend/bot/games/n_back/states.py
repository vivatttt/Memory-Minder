from aiogram.fsm.state import StatesGroup, State

class NBackForm(StatesGroup):
    game_started = State()