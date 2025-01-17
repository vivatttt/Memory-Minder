from enum import Enum

from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games import GamesFactory


class MainMenuButtons(Enum):
    select_game = "Выбрать игру"
    about = "Подробнее"


class ReturnHomeButtons(Enum):
    return_home = "В начало"

game_started_prefix = "game_started"

class Keyboard(BaseKeyboard):
    def main_menu(self):
        return self.create_inline_keyboard([(button.value, button.name) for button in MainMenuButtons])

    def back_home(self):
        return self.create_inline_keyboard([(button.value, button.name) for button in ReturnHomeButtons])

    def game_selection(self):
        buttons = GamesFactory().names_and_slugs
        for i in range(len(buttons)):
            buttons[i][1] = game_started_prefix + "_" + buttons[i][1]
        return self.create_inline_keyboard(buttons, row_width=2)
