from common.game_models import parse_yes_no, parse_llm_guess


def test_parse_yes_no_basic():
    assert parse_yes_no("yes") == "yes"
    assert parse_yes_no("no") == "no"
    assert parse_yes_no("maybe") is None


def test_parse_llm_guess():
    assert parse_llm_guess("GUESS: cat") == "cat"
    assert parse_llm_guess("guess: apple") == "apple"
    assert parse_llm_guess("not a guess") is None
