from frontend.bot.games.base import BaseGame
from frontend.bot.games.names_memory.states import NamesMemoryForm


class NamesMemoryGame(BaseGame):
    name = "Названия из памяти"
    slug = "names_memory"
    form = NamesMemoryForm
