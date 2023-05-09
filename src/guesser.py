from abc import ABC, abstractmethod
from src.models import Guess, Attempt
from pydantic import ValidationError
from typing import Sequence


class Guesser(ABC):
    @abstractmethod
    def guess(self, past: Sequence[Attempt]) -> Guess:
        pass


class Human(Guesser):
    def guess(self, past: Sequence[Attempt]) -> Guess:
        guess = None
        while guess is None:
            try:
                guess = Guess.from_word(input(f"Your guess [{len(past) + 1}]: "))
            except KeyboardInterrupt:
                print("Exiting...")
                exit(0)
            except ValidationError:
                print("Invalid guess. Try again.")
                pass
        return guess
