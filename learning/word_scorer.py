from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer
from inspect_ai.solver import TaskState


import re


def answer_contains_word(answer: str, word: str) -> bool:
    pattern = rf"\b{re.escape(word)}\b"
    return re.search(pattern, answer, re.IGNORECASE) is not None


@scorer(metrics=[accuracy()])
def word_match():
    async def score(state: TaskState, target: Target) -> Score:
        answer = state.output.completion
        expected = target.text
        correct = answer_contains_word(answer, expected)
        return Score(
            value=CORRECT if correct else INCORRECT,
            answer=answer,
            explanation=f"looked for the whole word {expected!r}",
        )

    return score