from abc import ABC, abstractmethod
from src.models import Guess
from pydantic import ValidationError


class Guesser(ABC):
    @abstractmethod
    def guess(self) -> Guess:
        pass


class Human(Guesser):
    def guess(self) -> Guess:
        guess = None
        while guess is None:
            try:
                guess = Guess.from_word(input("Your guess: "))
            except KeyboardInterrupt:
                print("Exiting...")
                exit(0)
            except ValidationError:
                print("Invalid guess. Try again.")
                pass
        return guess
