from frontend.bot.base.keyboards import BaseKeyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from frontend.bot.main_menu.keyboards import ReturnHomeButtons
from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games.names_memory.utils import with_game_slug

from enum import Enum

class OptionsButtons(Enum):
    stats = "👔Статистика"
    rules = "📝Правила📝"

class OptionsPlay(Enum):
    play = "✨Играть"

class Continue(Enum):
    conti = "🫡Все понял!"

class Agree(Enum):
    agree = "😎Я готов!😎"



class Keyboard(BaseKeyboard):
    def options_buttons(self):
        buttons = [
            (ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name),
            (OptionsPlay.play.value, with_game_slug(OptionsPlay.play.name))
        ]
        buttons.extend((item.value, with_game_slug(item.name)) for item in OptionsButtons)

        return self.create_inline_keyboard(buttons)

    def options_buttons_first(self):
        return self.create_inline_keyboard(
            [(ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name),
            (OptionsPlay.play.value, with_game_slug(OptionsPlay.play.name))]
        )

    def continue_button(self):
        return self.create_inline_keyboard(
            [(Continue.conti.value, with_game_slug(Continue.conti.name))],
            row_width=5
        )

    def agree_button(self):
        return self.create_inline_keyboard(
            [(Agree.agree.value, with_game_slug(Agree.agree.name))],
            row_width=5
        )
