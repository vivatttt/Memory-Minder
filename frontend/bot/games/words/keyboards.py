from enum import Enum

from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games.words.utils import with_game_slug
from frontend.bot.main_menu.keyboards import ReturnHomeButtons


class StartGameButtons(Enum):
    play = "Начать игру"
    description = "Описание и правила игры"
    statistics = "Статистика"


class ReturnGameButtons(Enum):
    exit = "Назад"


class Keyboard(BaseKeyboard):
    def start_menu(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in StartGameButtons])

    def return_back(self):
        return self.create_inline_keyboard(
            [(item.value, with_game_slug(item.name)) for item in ReturnGameButtons])

    def end(self):
        return self.create_inline_keyboard(
            [
                (ReturnHomeButtons.return_home.value, ReturnHomeButtons.return_home.name),
                (ReturnGameButtons.exit.value, with_game_slug(ReturnGameButtons.exit.name))
            ]
        )