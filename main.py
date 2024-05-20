import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import time
from typing import Generator, Union

from openai import OpenAI
from pysc2.lib.actions import FUNCTIONS
from pysc2.lib.named_array import NamedDict

from logo import STARCRAFT
from sc2_evals.agents import prompt_generator
from sc2_evals.agents.models import Model, ModelInfo
from sc2_evals.agents.openai.agent import Agent, Response, ToolOutputResponse
from sc2_evals.agents.openai.logger import Logger
from sc2_evals.agents.function_description import FunctionDescription
from sc2_evals.envs.env import Env
from sc2_evals.games.game import Game
from sc2_evals.games.defeat_roaches import DefeatRoaches

from sc2_evals.games.collect_minerals_and_gas import CollectMineralsAndGas
from sc2_evals.envs.action import Action
from sc2_evals.envs.action_descriptions import ActionDescriptions


GAME = CollectMineralsAndGas
MEMORY: bool = False  # setting this to True can lead to high costs
MOCKED: bool = False
MODEL: Model = Model.GPT_35_TURBO_0125


def user_content(
    game: Game, observation: NamedDict, valid_actions: list[str], reward: int
) -> str:
    content: str = game.user_content(
        observation, available_actions=valid_actions, reward=reward
    )
    user_message: dict[str, str] = prompt_generator.user_message(content)
    return user_message["content"]


def main():
    print(STARCRAFT)
    print(f"Model: {MODEL.value}")
    action_descriptions: ActionDescriptions = ActionDescriptions(screen_size=32)
    game = GAME()
    logger: Logger = Logger(
        base_dir="data", model_info=ModelInfo(MODEL), game=game.name.lower()
    )
    env: Env = Env(game.name, mocked=MOCKED)
    system_message: dict[str, str] = prompt_generator.system_message(
        game.system_content()
    )
    observation, available_actions = env.reset()
    observation, reward, done, available_actions = env.step([FUNCTIONS.no_op()])

    def action_fn(name: Union[str, list], x1=None, y1=None, x2=None, y2=None):
        nonlocal observation
        nonlocal available_actions
        action = Action(name, x1, y1, x2, y2).function_call
        observation, reward, done, available_actions = env.step([action])
        # output is observation
        return {
            "content": user_content(
                game,
                observation,
                action_descriptions.valid_actions(available_actions),
                reward,
            ),
            "metadata": {"reward": reward, "done": done},
        }

    functions: list[FunctionDescription] = action_descriptions.descriptions(action_fn)
    logger.log_system(system_message["content"], functions)

    agent: Agent = Agent(
        client=OpenAI(),
        model=MODEL.value,
        max_completion_tokens=4096,
        memory=MEMORY,
        system_message=system_message,
    )

    for i in range(100):
        content: str = user_content(
            game,
            observation,
            action_descriptions.valid_actions(available_actions),
            reward,
        )
        logger.log_user(step=i, content=content)
        messages = [
            {
                "role": "user",
                "content": content,
            }
        ]
        responses: Generator[Response, None, None] = agent.run(
            messages, functions=functions
        )

        for response in responses:
            logger.log_assistant(step=i, response=response)
            logger.log_stats()
            if isinstance(response, ToolOutputResponse):
                metadata = response.metadata
                if metadata is not None and metadata["done"] == True:
                    print("DONE")
                    exit()


if __name__ == "__main__":
    main()
