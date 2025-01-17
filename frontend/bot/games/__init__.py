from frontend.bot.games.base import BaseGame
from frontend.bot.games.false_state import FalseStateGame
from frontend.bot.games.n_back import NBackGame
from frontend.bot.games.names_memory import NamesMemoryGame
from frontend.bot.games.simon import SimonGame
from frontend.bot.games.words import WordsGame


class GamesFactory:
    _map: dict[str, BaseGame] = {
        "false_state": FalseStateGame,
        "n_back": NBackGame,
        "names_memory": NamesMemoryGame,
        "simon": SimonGame,
        "words": WordsGame,
    }

    @property
    def slugs(self):
        return list(self._map.keys())

    @property
    def names_and_slugs(self) -> list[dict[str]]:
        return [[config.name, config.slug] for config in self._map.values()]

    def names(self, slug: str) -> list[str]:
        return [config.name for config in self._map.get(slug, [])]

    def get(self, slug: str) -> BaseGame | None:
        return self._map.get(slug)


