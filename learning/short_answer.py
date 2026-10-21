from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message
from word_scorer import word_match
from prompts import PROMPTS

SAMPLES = [
    Sample(input="What is the capital of France?", target="Paris"),
    Sample(input="How many legs does a spider have?", target="8"),
    Sample(input="What is the chemical symbol for gold?", target="Au")
]

@task
def short_answer(condition: str = "none") -> Task:

    solvers = []
    if condition != "none":
        solvers.append(system_message(PROMPTS[condition]))
    solvers.append(generate())
    return Task(
        dataset=SAMPLES,
        solver=solvers,
        scorer=word_match()
    )