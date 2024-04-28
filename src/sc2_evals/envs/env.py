import sys

from pysc2.lib.named_array import NamedDict
from pysc2.env.environment import TimeStep
from pysc2.env.sc2_env import SC2Env
from pysc2.env.sc2_env import AgentInterfaceFormat
from pysc2.env.sc2_env import Dimensions
from pysc2.env import sc2_env
from pysc2.env.mock_sc2_env import SC2TestEnv

import absl.flags
absl.flags.FLAGS(sys.argv)
SCREEN = ((32, 32), 32)

class Env:

    def __init__(self, map_name: str, mocked: bool):
        dimensions: Dimensions = Dimensions(screen=SCREEN[0], minimap=(1,1))
        interface_format: AgentInterfaceFormat = AgentInterfaceFormat(
            feature_dimensions=dimensions,
            use_feature_units=True,
        )
        # https://github.com/google-deepmind/pysc2/blob/master/docs/mini_games.md
        arguments = {
            "map_name": map_name,
            "agent_interface_format": interface_format,
            "step_mul": SCREEN[1],
            "random_seed": 1337,
            "players": [sc2_env.Agent(sc2_env.Race.terran)],
            "visualize": False 
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
    
    def step(self, actions):
        self.last_step: TimeStep =  self.env.step(actions)[0]
        # done = true if step_type is last
        done: bool = self.last_step.last()
        reward = self.last_step.reward
        observation: NamedDict = self.last_step.observation
        available_actions: list[int] = self.last_step.observation["available_actions"]
        #action_result = self.last_step.observation["action_result"]
        #print("action_result", action_result)

        #alerts = self.last_step.observation["alerts"]
        #print("alerts", alerts)

        #last_actions = self.last_step.observation["last_actions"]
        #print("last_actions", last_actions)

        #build_queue = self.last_step.observation["build_queue"]
        #print("build_queue", build_queue)

        #print(self.env.game_info)
        #self.env.send_chat_messages([f"reward: {reward}"])
        return observation, reward, done, available_actions
   
