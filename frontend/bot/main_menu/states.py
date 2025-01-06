from aiogram.fsm.state import StatesGroup, State

class MainMenuForm(StatesGroup):
    started = State()
    about = State()
    select_game = State()
    view_statistics = State()