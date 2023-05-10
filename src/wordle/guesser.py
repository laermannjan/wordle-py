from abc import ABC, abstractmethod
from wordle.models import Guess, Attempt
from pydantic import ValidationError
from typing import Sequence
import random


class Guesser(ABC):
    @abstractmethod
    def guess(self, past: Sequence[Attempt]) -> Guess:
        pass


class Human(Guesser):
    __doc__ = "Guess a word by yourself"

    def guess(self, past: Sequence[Attempt]) -> Guess:
        guess = None
        while guess is None:
            try:
                guess = Guess.from_word(input(f"Your guess [{len(past) + 1}]: "))
            except ValidationError:
                print("Invalid guess. Try again.")
                pass
        return guess


class RandomLetters(Guesser):
    __doc__ = "Creates random 5 character strings"

    def guess(self, past: Sequence[Attempt]) -> Guess:
        return Guess.from_word("".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5)))


AVAILABLE_GUESSERS = [
    Human,
    RandomLetters,
]
