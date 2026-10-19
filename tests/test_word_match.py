from learning.word_scorer import answer_contains_word


def test_whole_word_matches():
    assert answer_contains_word("The symbol is Au.", "Au")


def test_does_not_match_inside_another_word():
    assert not answer_contains_word("Default output from mockllm/model", "Au")