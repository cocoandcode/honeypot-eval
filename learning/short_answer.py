from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes, match 
from inspect_ai.solver import generate
from word_scorer import word_match

SAMPLES = [
    Sample(input="What is the capital of France?", target="Paris"),
    Sample(input="How many legs does a spider have?", target="8"),
    Sample(input="What is the chemical symbol for gold?", target="Au")
]

@task
def short_answer() -> Task:
    return Task(
        dataset=SAMPLES,
        solver=generate(),
        scorer=word_match()
    )