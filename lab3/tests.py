import typing as t
from typing import TypeVar, Generic

SolutionFunction = t.Callable[[t.Pattern, str], t.Any]


class TestCase:
    def __init__(self, string: str, answer: t.Any):
        self.string = string
        self.answer = answer
        self.group: "TestGroup" = None

    def _assign_group(self, group: "TestGroup"):
        """Assigns the test to the group to which it was added"""
        self.group = group

    def _run(self) -> bool:
        """Runs test case"""
        if self.group is None:
            print('ERROR: Test is not assigned with test group')
            return False

        # Getting solution function from assigned group
        solution_function = self.group.function
        # Executing function with string from current test case
        current_answer = solution_function(self.group.pattern, self.string)
        # Comparing current answer with expected one
        result = current_answer == self.answer

        return result


class TestGroup:
    def __init__(self, name: str, pattern: t.Pattern, function: SolutionFunction):
        self.name = name

        self.pattern = pattern
        self.function = function
        self.tests: t.List[TestCase] = []

    def add_tests(self, *test_cases: TestCase):
        for test in test_cases:
            test._assign_group(self)
            self.tests.append(test)

    def run_on_users_input(self):
        print(f"\nINFO: Testing «{self.name}» with user's input, in order to stop, press ENTER")
        while True:
            string = input('Enter string - ')

            if string == '':
                print('Testing is finished')
                break

            result = self.function(self.pattern, string)
            print(f'Result: {result}')

    def run(self):
        print(f"INFO: Testing «{self.name}»")

        for i, test in enumerate(self.tests):
            result = test._run()

            if result:
                print(f'[V] Test №{i + 1} passed successfully')
            else:
                print(f'[X] Test №{i + 1} failed')
