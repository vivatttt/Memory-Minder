from frontend.bot.games.base import BaseGame
from frontend.bot.games.words.states import WordsForm

class WordsGame(BaseGame):
    name = "Слова"
    slug = "words"
    form = WordsForm