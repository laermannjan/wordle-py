from __future__ import annotations
from enum import Enum
from pydantic import Field, BaseModel
from typing import Annotated


class Clue(str, Enum):
    correct = "!"
    misplaced = "?"
    wrong = "-"

    def __str__(self) -> str:
        return self.value


class Status(BaseModel):
    won: bool
    clue: Annotated[list[Clue], Field(max_length=5)]


class Word(BaseModel):
    letters: Annotated[str, Field(regex="[a-z]{5}")]

    @classmethod
    def from_word(cls, word: str):
        return cls(letters=word)

    def __iter__(self):
        return iter(self.letters)

    def __str__(self) -> str:
        return f"{self.__repr_name__}({''.join(self.letters)})"


class Answer(BaseModel):
    letters: Annotated[str, Field(regex="[a-z]{5}")]

    @classmethod
    def from_word(cls, word: str):
        return cls(letters=word)

    def __iter__(self):
        return iter(self.letters)

    def __str__(self) -> str:
        return f"{self.__repr_name__}({''.join(self.letters)})"

    def eval(self, guess: Guess) -> Status:
        clue = []
        for i, letter in enumerate(guess):
            if letter == self.letters[i]:
                clue.append(Clue.correct)
            elif letter in self.letters:
                clue.append(Clue.misplaced)
            else:
                clue.append(Clue.wrong)

        status = Status(
            won=all(c == Clue.correct for c in clue),
            clue=clue,
        )

        return status


class Guess(BaseModel):
    letters: Annotated[str, Field(regex="[a-z]{5}")]

    @classmethod
    def from_word(cls, word: str):
        return cls(letters=word)

    def __iter__(self):
        return iter(self.letters)

    def __str__(self) -> str:
        return f"{self.__repr_name__}({''.join(self.letters)})"
