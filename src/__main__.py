import os
import random
import logging

from src.guesser import Guesser, Human
from src.models import Answer, Attempt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WORDS = ["guess", "house", "bingo"]
MAX_ATTEMPTS = 5


def play(answer: Answer, guesser: Guesser):
    for attempt_id in range(MAX_ATTEMPTS):
        guess = guesser.guess([])
        attempt = Attempt.from_answer(
            guess=guess,
            answer=answer,
        )

        print(attempt)
        if attempt.is_successful():
            print("You won!")
            return
    print("You lost!")


def main():
    answer = Answer.from_word(random.choice(WORDS))
    guesser = Human()
    play(answer=answer, guesser=guesser)


if __name__ == "__main__":
    if os.environ.get("ENV", "dev") != "prod":
        logger.debug("fixing random seed")
        random.seed(42)
    main()
