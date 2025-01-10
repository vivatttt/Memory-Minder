from frontend.bot.games.base import BaseGame
from frontend.bot.games.simon.states import SimonForm


class SimonGame(BaseGame):
    name = "Саймон"
    slug = "simon"
    form = SimonForm
