from typing import Callable

from pysc2.lib.named_array import NamedDict
from pysc2.lib.features import FeatureUnit

from sc2_evals.agents import utils

def coords_to_string(coords) -> str:
    return " ".join([f"{coord[0]},{coord[1]}" for coord in coords])

def filter(observation: NamedDict, condition: Callable[[FeatureUnit], bool]) -> str:
    return coords_to_string(utils.filter(observation, condition))

def user_message(content: str) -> dict[str, str]:
    return {"role": "user", "content": content}

def system_message(content: str) -> dict[str, str]:
    return {"role": "system", "content": content}