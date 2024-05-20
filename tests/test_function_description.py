import json
import unittest

from sc2_evals.envs.env import Env
from sc2_evals.envs.action import Action
from sc2_evals.envs.action_description import ActionDescription
from sc2_evals.envs.action_descriptions import ActionDescriptions


class TestFunctionDescription(unittest.TestCase):

    def test_action(self):
        arguments = {"name": ["select_army"], "x1": 1, "y1": 2, "x2": 3, "y2": 4}
        action = Action(**arguments).function_call
        self.assertEqual(action.function.name, "select_army")

    def test_action_description(self):
        arguments = {"name": ["select_army"], "x1": 1, "y1": 2, "x2": 3, "y2": 4}
        action = Action(**arguments).function_call
        self.assertEqual(action.function.name, "select_army")

        description = ActionDescription.no_screen()
        self.assertEqual(description["name"], "act")
        print(json.dumps(description, indent=2))
        print("description", description)

    def test_action_descriptions(self):
        action_descriptions: ActionDescriptions = ActionDescriptions(screen_size=32)

        def _function(name: str, x1: int, y1: int, x2: int, y2: int) -> str:
            return "test"

        descriptions = action_descriptions.descriptions(action_fn=_function)
        self.assertEqual(len(descriptions), 2)

    def test_descriptions(self):
        def _function(name: str, x1: int, y1: int, x2: int, y2: int) -> str:
            return "test"

        action_descriptions: ActionDescriptions = ActionDescriptions(screen_size=32)
        descriptions = action_descriptions.descriptions(action_fn=_function)
        function = descriptions[0]

        # test "Attack_screen"
        arguments = json.dumps(
            {"name": "Attack_screen", "x1": 1, "y1": 2, "x2": 3, "y2": 4}
        )
        output = function(arguments)
        self.assertEqual(output, "test")

        # test ["Attack_screen"]
        arguments = json.dumps(
            {"name": ["Attack_screen"], "x1": 1, "y1": 2, "x2": 3, "y2": 4}
        )
        output = function(arguments)
        self.assertEqual(output, "test")

    #@unittest.skip("")
    def test_step(self):
        arguments = {
            "name": ["Build_CommandCenter_screen"],
            "x1": 24,
            "y1": 4,
            "x2": 3,
            "y2": 4,
        }
        action = Action(**arguments).function_call
        env: Env = Env("DefeatRoaches", mocked=False)
        env.reset()
        try:
            env.step([action])
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(
                str(e),
                "Function _Functions.Build_CommandCenter_screen/Build_CommandCenter_screen is currently not available",
            )
            self.assertEqual(
                repr(e),
                "ValueError('Function _Functions.Build_CommandCenter_screen/Build_CommandCenter_screen is currently not available')",
            )


if __name__ == "__main__":
    unittest.main()
