from pydantic import BaseModel, Field


class StatementsExternalModel(BaseModel):
    correct: list[str]
    wrong: list[str]

class GameDataExternalModel(BaseModel):
    text: str
    statements: StatementsExternalModel

class Statements(BaseModel):
    wrong_inds: set[int]
    text: str
    num: int

class GameData(BaseModel):
    text: str
    statements: Statements

class UserGame(BaseModel):
    data: GameData
    choosen_wrong_inds: set[int] = Field(default_factory=set)
