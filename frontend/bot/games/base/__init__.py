from dataclasses import dataclass
from typing import Type

from aiogram.fsm.state import StatesGroup


@dataclass
class BaseGame:
    name: str
    slug: str
    form: Type[StatesGroup]