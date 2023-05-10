import os
import random
import logging

from wordle.guesser import Guesser, AVAILABLE_GUESSERS
from wordle.models import Answer, Attempt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WORDS = ["guess", "house", "bingo"]
MAX_ATTEMPTS = 5


def play(answer: Answer, guesser: Guesser):
    attempts: list[Attempt] = []
    for attempt_id in range(MAX_ATTEMPTS):
        guess = guesser.guess(past=attempts)
        attempt = Attempt.from_answer(
            guess=guess,
            answer=answer,
        )
        print(attempt)
        attempts.append(attempt)
        if attempt.is_successful():
            print("You won!")
            return
    print("You lost!")


def choose_guesser():
    print("Available guessers:")
    print("\n".join(f"{i}: {guesser.__name__} [{guesser.__doc__}]" for i, guesser in enumerate(AVAILABLE_GUESSERS)))
    while True:
        selection = input("Choose your guesser (0): ")
        if selection == "":
            selection = 0
        try:
            return AVAILABLE_GUESSERS[int(selection)]()
        except (ValueError, IndexError):
            print("Invalid selection. Try again.")


def main():
    answer = Answer.from_word(random.choice(WORDS))
    try:
        guesser = choose_guesser()
        play(answer=answer, guesser=guesser)
    except KeyboardInterrupt:
        print("\n\nExiting...")


if __name__ == "__main__":
    if os.environ.get("ENV", "dev") != "prod":
        logger.debug("fixing random seed")
        random.seed(42)
    main()
