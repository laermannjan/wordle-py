from src.models import Clue, Word, ClueEnum, Guess, Answer, Attempt
import pytest


@pytest.mark.parametrize("guess, answer, clue", [
    ("bingo", "bingo", Clue(letter_clues=[ClueEnum.correct] * 5)),
    ("binga", "bingo", Clue(letter_clues=[ClueEnum.correct] * 4 + [ClueEnum.wrong])),
    pytest.param("bingi", "bingo", Clue(letter_clues=[ClueEnum.correct] * 4 + [ClueEnum.wrong]), marks=pytest.mark.xfail(reason="We don't respect frequency of letters yet.")),
    ("binog", "bingo", Clue(letter_clues=[ClueEnum.correct] * 3 + [ClueEnum.misplaced] * 2)),
    ("qwert", "bingo", Clue(letter_clues=[ClueEnum.wrong] * 5)),
    ("obing", "bingo", Clue(letter_clues=[ClueEnum.misplaced] * 5)),
])
def test_word_comparison(guess, answer, clue):
    assert Word._match(guess=Word.from_word(guess), answer=Word.from_word(answer)) == clue
    
    
@pytest.mark.parametrize("guess, answer, clue", [
    ("bingo", "bingo", [ClueEnum.correct] * 5),
    ("ffffz", "affff", [ClueEnum.misplaced] + [ClueEnum.correct] * 3 + [ClueEnum.wrong]),
    ("affff", "ffffz", [ClueEnum.wrong] + [ClueEnum.correct] * 3 + [ClueEnum.misplaced]),
])
def test_match(guess, answer, clue):
    test_guess = Guess.from_word(guess)
    test_answer = Answer.from_word(answer)
    test_clue = Clue(letter_clues=clue)
    assert test_guess.match(test_answer) == test_answer.match(test_guess) == test_clue 


@pytest.mark.parametrize("guess, answer, is_success", [
    ("bingo", "bingo", True),
    ("bingi", "bingo", False),
    ("obing", "bingo", False),
])
def test_successful_attempt(guess, answer, is_success):
    test_guess = Guess.from_word(guess)
    test_answer = Answer.from_word(answer)
    assert Attempt(guess=test_guess, answer=test_answer).is_successful() == is_success
    