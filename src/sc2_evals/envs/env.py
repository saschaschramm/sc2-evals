import sys

from pysc2.lib.named_array import NamedDict
from pysc2.env.environment import TimeStep
from pysc2.env.sc2_env import AgentInterfaceFormat, Dimensions, SC2Env
from pysc2.env import sc2_env
from pysc2.env.mock_sc2_env import SC2TestEnv

import absl.flags

absl.flags.FLAGS(sys.argv)

SCREEN: tuple[int, int] = (32, 32)
STEP_MUL: int = 32
"""`step_mul` let's you skip observations and actions. For example a `step_mul` of
16 means that the environment gets stepped forward 16 times in between the
actions of the agent (16 steps = 1 second of game time). It is equivalent to
ignoring certain observations and not sending actions on those frames, except it
also speeds up the environment since it doesn't need to render the skipped
frames."""


class Env:

    def __init__(self, map_name: str, mocked: bool):
        dimensions: Dimensions = Dimensions(screen=SCREEN, minimap=(1, 1))
        interface_format: AgentInterfaceFormat = AgentInterfaceFormat(
            feature_dimensions=dimensions,
            use_feature_units=True,
        )
        # https://github.com/google-deepmind/pysc2/blob/master/docs/mini_games.md
        arguments = {
            "map_name": map_name,
            "agent_interface_format": interface_format,
            "step_mul": STEP_MUL,
            "random_seed": 1337,
            "players": [sc2_env.Agent(sc2_env.Race.terran)],
            "visualize": False,
        }
        if mocked:
            self.env = SC2TestEnv(**arguments)
        else:
            self.env = SC2Env(**arguments)

    def available_actions(self):
        return self.last_step.observation["available_actions"]

    def action_spec(self):
        return self.env.action_spec()

    def reset(self):
        self.last_step = self.env.reset()[0]
        observation: NamedDict = self.last_step.observation
        return observation, self.available_actions()

    def step(self, actions) -> tuple[NamedDict, int, bool, list[int]]:
        self.last_step: TimeStep = self.env.step(actions)[0]
        # done = true if step_type is last
        done: bool = self.last_step.last()
        reward: int = self.last_step.reward
        observation: NamedDict = self.last_step.observation
        available_actions: list[int] = self.last_step.observation["available_actions"]
        # last_actions = self.last_step.observation["last_actions"]
        build_queue = self.last_step.observation["build_queue"]
        return observation, reward, done, available_actions
