from pysc2.lib.named_array import NamedDict
from pysc2.lib import units

from sc2_evals.agents.prompt_generator import filter
from sc2_evals.games.game import Game


SYSTEM_HARVEST = """You are an AI agent for StarCraft II.

## Rules
* Building a refinery requires 75 minerals.
* Building a SCV requires 50 minerals.

## Goal
The goal is to harvest as many minerals and vespene gas as possible."""


SYSTEM_HARVEST_GAS = """You are an AI agent for StarCraft II.

## Rules
* First harvest minerals.
* Once you have 75 minerals, build a refinery."""

SYSTEM_TRAIN = """You are an AI agent for StarCraft II.

## Rules
* Training a SCV requires 50 minerals.

## Goal
Train as many SCVs as possible."""

SYSTEM_CC = """You are an AI agent for StarCraft II.

## Rules
* A command center costs 400 minerals.

## Goal
Collect 400 minerals and build a command center."""


SYSTEM_MESSAGE_TRAIN = """You are an AI agent for StarCraft II.

For training an SCV, 50 minerals are required.

The goal ist to select the command center and train a single SCV (Train_SCV_quick). SCVs are trained at the command center."""


SYSTEM_MESSAGE_LONG = """You are an AI agent for StarCraft II.

### Map
A map with 12 SCVs, 1 Command Center, 16 Mineral Fields and 4 Vespene Geysers. 

### Rewards
Rewards are based on the total amount of Minerals and Vespene Gas collected. 
Spending Minerals and Vespene Gas to train new units does not decrease your reward tally. 
Optimal collection will require expanding your capacity to gather Minerals and Vespene 
Gas by constructing additional SCVs and an additional Command Center.

### Goal
Maximize the reward."""

SYSTEM = SYSTEM_HARVEST

USER = """## Last observation
{observation}
## Available actions
{available_actions}
## Last reward
{reward}
## Instruction
Perform the next action"""

class CollectMineralsAndGas(Game):

    name = "CollectMineralsAndGas"

    def user_content(
        self,
        observation: NamedDict,
        available_actions: list[str],
        reward: int
    ):
        minerals = observation["player"].minerals
        mineral_position = filter(
            observation, lambda unit: unit.unit_type == units.Neutral.MineralField
        )
        gas_position = filter(
            observation, lambda unit: unit.unit_type == units.Neutral.VespeneGeyser
        )
        refinery_position = filter(
            observation, lambda unit: unit.unit_type == units.Terran.Refinery
        )

        idle_workers = filter(
            observation,
            lambda unit: unit.unit_type == units.Terran.SCV and unit.order_length == 0,
        )
        idle_workers_selected = filter(
            observation,
            lambda unit: unit.is_selected
            and unit.unit_type == units.Terran.SCV
            and unit.order_length == 0,
        )
        command_center = filter(
            observation, lambda unit: unit.unit_type == units.Terran.CommandCenter
        )
        command_center_selected = filter(
            observation,
            lambda unit: unit.is_selected
            and unit.unit_type == units.Terran.CommandCenter,
        )
        worker_is_selected = filter(
            observation,
            lambda unit: unit.is_selected and unit.unit_type == units.Terran.SCV,
        )

        relevant_observation = [
            ("Available minerals", minerals),
            ("Mineral position", mineral_position),
            ("Vaspene geysers position", gas_position),
            # ("Selected workers", worker_is_selected),
            ("Idle workers", idle_workers),
            ("Selected idle workers", idle_workers_selected),
            ("Command center", command_center),
            ("Command center selected", command_center_selected),
            ("Refinery position", refinery_position),
        ]

        observation_str = [
            f"### {name}\n{value}" for name, value in relevant_observation
        ]
        refinery_position = ""
        prompt = USER.format(
            observation="\n".join(observation_str),
            available_actions="\n".join(available_actions),
            reward=reward
        )
        return prompt

    def system_content(self):
        return SYSTEM
