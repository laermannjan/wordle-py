from __future__ import annotations
from enum import Enum

from pydantic import Field, BaseModel
from typing import Annotated


class ClueEnum(str, Enum):
    correct = "!"
    misplaced = "?"
    wrong = "-"

    def __str__(self) -> str:
        return self.value


class Clue(BaseModel):
    letter_clues: Annotated[list[ClueEnum], Field(default_factory=list, min_items=5, max_items=5)]

    def __iter__(self):
        return iter(self.letter_clues)

    def __str__(self):
        return f"{self.__class__.__name__}: {''.join(self.letter_clues)}"


class Word(BaseModel):
    letters: Annotated[str, Field(regex="^[a-z]{5}$")]

    @classmethod
    def from_word(cls, word: str):
        return cls(letters=word)

    def __iter__(self):
        return iter(self.letters)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {''.join(self.letters)}"

    def __getitem__(self, item):
        return self.letters[item]

    @classmethod
    def _match(cls, guess: Word, answer: Word) -> Clue:
        # TODO: number of occurances matter. If a letter is once in the answer,
        #  but twice in the guess, only one should be misplace/correct, the other wrong
        letter_clues = []
        for i, letter in enumerate(guess.letters):
            if letter == answer.letters[i]:
                letter_clues.append(ClueEnum.correct)
            elif letter in answer.letters:
                letter_clues.append(ClueEnum.misplaced)
            else:
                letter_clues.append(ClueEnum.wrong)

        return Clue(letter_clues=letter_clues)


class Guess(Word):
    def match(self, other: Answer) -> Clue:
        return Word._match(guess=self, answer=other)


class Answer(Word):
    def match(self, other: Guess):
        return Word._match(guess=other, answer=self)


class Attempt(BaseModel):
    guess: Guess
    clue: Clue

    @classmethod
    def from_answer(cls, guess: Guess, answer: Answer):
        return cls(guess=guess, clue=answer.match(guess))

    def is_successful(self) -> bool:
        return all(c == ClueEnum.correct for c in self.clue)

    def __str__(self):
        guess = f" {self.guess}"
        clues = f"  {self.clue}"
        return "\n".join([guess, clues, ""])
