from aiogram.fsm.state import State, StatesGroup


class MainMenuForm(StatesGroup):
    started = State()
    about = State()
    select_game = State()
    view_statistics = State()
    send = State()

class AuthorizationForm(StatesGroup):
    waiting_for_name = State()
    name_filled = State()
