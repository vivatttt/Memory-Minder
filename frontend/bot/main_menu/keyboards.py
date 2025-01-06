from enum import Enum

from frontend.bot.base.keyboards import BaseKeyboard
from frontend.bot.games import GamesFactory

class MainMenuButtons(Enum):
    select_game = "Выбрать игру"
    view_statistics = "Посмотреть статистику"
    about = "Подробнее"

class StartGameButtons(Enum):
    play = "Играть"

class Keyboard(BaseKeyboard):
    def main_menu(self):
        return self.create_reply_keyboard([button.value for button in MainMenuButtons])

    def play(self):
        return self.create_reply_keyboard([StartGameButtons.play.value])
    
    def game_selection(self):   
        return self.create_inline_keyboard(GamesFactory().names_and_slugs, row_width=2)