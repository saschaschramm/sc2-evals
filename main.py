import asyncio
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from typing import AsyncGenerator, Union

from openai import AsyncOpenAI
from pysc2.lib import actions

from logger import Logger
from logo import STARCRAFT
from models import Model, ModelInfo
from sc2_evals.agents.openai.agent import Agent, FunctionSchema, Response
from sc2_evals.agents import prompt_generator
from sc2_evals.envs.env import Env
from sc2_evals.games.game import Game
from sc2_evals.games.defeat_roaches import DefeatRoaches
from sc2_evals.games.collect_minerals_and_gas import CollectMineralsAndGas
from sc2_evals.envs.schema import Schema


GAME = DefeatRoaches
MEMORY: bool = False # setting this to True can lead to high costs
MOCKED: bool = False
MODEL: Model = Model.GPT4_TURBO_2024_04_09


def _available_action_names(available_actions: list[int]) -> list[str]:
    names: list[str] = []
    for action in available_actions:
        name = actions.FUNCTIONS[action].name
        names.append(name)
    return names


def _valid_actions(available_actions: list[int]) -> list[str]:
    names: list[str] = _available_action_names(available_actions)
    return list(set(Schema.actions()) & set(names))


def _functions(action_fn) -> list[FunctionSchema]:
    function_descriptions = Schema.descriptions(screen_size=32)
    schemas: list[FunctionSchema] = []
    for function_description in function_descriptions:
        schemas.append(
            FunctionSchema(
                name=function_description["name"],
                description=function_description["description"],
                parameters=function_description["parameters"],
                function=action_fn,
                extra=None,
            )
        )
    return schemas


def user_content(
    game: Game, observation: str, available_actions: list[int], reward: int
) -> str:
    content: str = game.user_content(
        observation, available_actions=_valid_actions(available_actions), reward=reward
    )
    user_message: dict[str, str] = prompt_generator.user_message(content)
    return user_message["content"]


async def main():
    print(STARCRAFT)
    print(f"Model: {MODEL.value}")
    game = GAME()
    logger: Logger = Logger(
        dir="data", model_info=ModelInfo(MODEL), game=game.name.lower()
    )
    env: Env = Env(game.name, mocked=MOCKED)
    system_message: dict[str, str] = prompt_generator.system_message(game.system_content())
    observation, available_actions = env.reset()
    observation, reward, done, available_actions = env.step([actions.FUNCTIONS.no_op()])

    async def call_function(name: Union[str, list], x1=None, y1=None, x2=None, y2=None):
        nonlocal observation
        nonlocal available_actions
        # not possible to update assistant tools during run (!)
        try:
            action = Schema.action_from_function_call(name, x1, y1, x2, y2)
            # only do a step if the action can be parsed into a function call
            observation, reward, done, available_actions = env.step([action])
            if done:
                print("DONE")
                exit()
            # output is observation
            return {
                "content": user_content(game, observation, available_actions, reward),
                "metadata": {"reward": reward},
            }
        except Exception as e:
            # the property output of 'submit_tool_outputs' expects a string!
            return f"Error: {e}"

    functions = _functions(call_function)
    await logger.log_system(system_message["content"], functions)

    agent: Agent = Agent(
        client=AsyncOpenAI(), model=MODEL.value, max_completion_tokens=4096, memory=MEMORY, system_message=system_message
    )

    for i in range(100):
        content = user_content(game, observation, available_actions, reward)
        await logger.log_user(step=i, content=content)
        messages = [
            {
                "role": "user",
                "content": content,
            }
        ]
        responses: AsyncGenerator[Response, None] = agent.run(
            messages, functions=functions
        )
        await logger.log_assistant(step=i, responses=responses)


if __name__ == "__main__":
    asyncio.run(main())
