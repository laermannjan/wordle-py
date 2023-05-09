import os
import random
import logging

from src.guesser import Guesser, Human
from src.models import Answer, Attempt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WORDS = ["guess", "house", "bingo"]


def play(answer: Answer, guesser: Guesser):
    while True:
        attempt = Attempt(
            guess=guesser.guess(),
            answer=answer
        )

        print(attempt)
        if attempt.is_successful():
            print("You won!")
            return


def main():
    answer = Answer.from_word(random.choice(WORDS))
    guesser = Human()
    play(answer=answer, guesser=guesser)


if __name__ == "__main__":
    if os.environ.get("ENV", "dev") != "prod":
        logger.debug("fixing random seed")
        random.seed(42)
    main()
