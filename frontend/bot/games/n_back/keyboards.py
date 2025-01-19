from enum import Enum
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from frontend.bot.main_menu.keyboards import ReturnHomeButtons
from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games.n_back.utils import with_game_slug


class GameMenuButtons(Enum):
    play = "Начать игру"
    rules = "Правила"
    N = "Изменить N"
    stats = "Статистика"

class AfterRuleButtons(Enum):
    play = "Начать игру"
    N = "Изменить N"
    stats = "Статистика"
    
class GameEndButtons(Enum):
    results = "Просмотр ответов"
    retry = "Старт игры"

class NumbersButtons():
    key = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f"choice_{i}") for i in range(0, 5)],
            [InlineKeyboardButton(text=str(i), callback_data=f"choice_{i}") for i in range(5, 10)]
        ])

class Keyboard(BaseKeyboard):
    def game_menu(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in GameMenuButtons] + 
            [(ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name)]
        )
    
    def game_menu_after_rule(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in AfterRuleButtons] + 
            [(ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name)]
        )
    
    def end_game_menu(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in GameEndButtons] +
            [(ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name)]
        )