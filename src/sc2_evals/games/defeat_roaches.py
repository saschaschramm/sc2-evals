from pysc2.lib.named_array import NamedDict
from pysc2.lib import units
from sc2_evals.agents import prompt_generator
from sc2_evals.games.game import Game

SYSTEM = """You are an AI agent for StarCraft II.

## Rules
* You control a group of Marines
* Marines can attack Roaches

## Rewards
* Reward Roach defeated: +10
* Reward Marine defeated: -1

## Goal
The goal is to maximize the reward"""


USER = """## Last observation
{observation}
## Available actions
{available_actions}
## Last reward
{reward}
## Instruction
Perform the next action"""


class DefeatRoaches(Game):

    name = "DefeatRoaches"

    def user_content(self, observation: NamedDict, available_actions: list[str], reward: int):
        roaches = prompt_generator.filter(
            observation, lambda unit: unit.unit_type == units.Zerg.Roach
        )
        marines = prompt_generator.filter(
            observation, lambda unit: unit.unit_type == units.Terran.Marine
        )
        marines_selected = prompt_generator.filter(
            observation,
            lambda unit: unit.is_selected and unit.unit_type == units.Terran.Marine,
        )
        relevant_observation = [
            ("Marines position", marines),
            ("Marines selected", marines_selected),
            ("Roaches position", roaches),
        ]

        prompt = USER.format(
            observation="\n".join(
                [f"### {name}\n{value}" for name, value in relevant_observation]
            ),
            available_actions="\n".join(available_actions),
            reward=reward
        )
        return prompt

    def system_content(self):
        return SYSTEM
