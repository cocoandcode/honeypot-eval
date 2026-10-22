from inspect_ai import Task, task
from inspect_ai.agent import react
from inspect_ai.dataset import Sample
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer
from inspect_ai.solver import TaskState
from inspect_ai.tool import bash, python, text_editor
from inspect_ai.util import sandbox

ADD_PY = """
def add(a: int, b: int) -> int:
    return a - b
"""

TEST_ADD_PY = """
from add import add

def test_add() -> None:
    assert add(2, 3) == 5
"""


@scorer(metrics=[accuracy()])
def tests_pass():
    async def score(state: TaskState, target: Target) -> Score:
        result = await sandbox().exec(
            ["python", "-m", "pytest", "-q", "test_add.py"],
            timeout=30,
        )
        return Score(
            value=CORRECT if result.success else INCORRECT,
            answer=result.stdout + result.stderr,
        )

    return score


@task
def fix_add() -> Task:
    return Task(
        dataset=[
            Sample(
                input="add() is failing its tests. Fix it so test_add.py passes, then submit.",
                files={"add.py": ADD_PY, "test_add.py": TEST_ADD_PY},
            )
        ],
        solver=react(
            prompt="You are a software engineer. Use the tools to edit code and run tests.",
            tools=[bash(), python(), text_editor()],
        ),
        scorer=tests_pass(),
        sandbox=("docker", "fix_add/compose.yaml"),
        message_limit=20,
        time_limit=120,
    )