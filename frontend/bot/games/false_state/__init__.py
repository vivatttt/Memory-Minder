from frontend.bot.games.base import BaseGame
from frontend.bot.games.false_state.states import FalseStateForm

class FalseStateGame(BaseGame):
    name = "Ложные высказывания"
    slug = "false_state"
    form = FalseStateForm