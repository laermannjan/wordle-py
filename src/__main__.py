import os
import random
import logging

from src.guesser import Guesser, Human
from src.models import Answer, Guess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WORDS = ["guess", "house", "bingo"]


def play(answer: Answer, guesser: Guesser):
    while True:
        guess = guesser.guess()

        print(f"{guess=}")
        status = answer.eval(guess)
        if status.won:
            print(f"You won! - {guess} == {answer}")
            break


def main():
    answer = Answer.from_word(random.choice(WORDS))
    guesser = Human()

    while True:
        play(answer=answer, guesser=guesser)


if __name__ == "__main__":
    if os.environ.get("ENV", "dev") != "prod":
        logger.debug("fixing random seed")
        random.seed(42)
    main()
