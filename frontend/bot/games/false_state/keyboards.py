from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from frontend.bot.main_menu.keyboards import ReturnHomeButtons
from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games.false_state.utils import with_game_slug
from frontend.bot.games.false_state.schemas import UserGame

from enum import Enum

class GameMenuButtons(Enum):
    play = "Играть"
    stats = "Статистика"
    rules = "Правила"

class StatementsButtons(Enum):
    change_statement = "Изменить"
    send_statement = "Отправить"

class GameEndButtons(Enum):
    retry = "Попробовать еще раз"
    
class Keyboard(BaseKeyboard):
    def game_menu(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in GameMenuButtons]
        )
    def statements(self, user_game: UserGame):
  
        pref = StatementsButtons.change_statement.name
        buttons = [
            (f"✅{i}", with_game_slug(f"{pref}:{i}")) 
            if i in user_game.choosen_wrong_inds 
            else (f"{i}", with_game_slug(f"{pref}:{i}"))
            for i in range(1, user_game.data.statements.num + 1) 
        ]
    
        row_width = 2
        keyboard = [
            [InlineKeyboardButton(text=text, callback_data=data) for text, data in buttons[i:i + row_width]]
            for i in range(0, len(buttons), row_width)
        ]
        keyboard.append([InlineKeyboardButton(text=StatementsButtons.send_statement.value, callback_data=with_game_slug(StatementsButtons.send_statement.name))])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    def end(self):
        return self.create_inline_keyboard(
            [
                (GameEndButtons.retry.value, with_game_slug(GameEndButtons.retry.name)),
                (ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name)
            ]
        )