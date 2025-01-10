from frontend.bot.games.base import BaseGame
from frontend.bot.games.n_back.states import NBackForm


class NBackGame(BaseGame):
    name = "N-back математический"
    slug = "n_back"
    form = NBackForm
