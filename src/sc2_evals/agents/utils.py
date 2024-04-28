from typing import Callable, Tuple

from pysc2.lib.named_array import NamedDict
from pysc2.lib.features import FeatureUnit

def filter(observation: NamedDict, condition: Callable[[FeatureUnit], bool]) -> list[Tuple[int, int]]:
    unit: FeatureUnit
    coordinates: list[Tuple[int, int]] = []
    for unit in observation["feature_units"]:
        if condition(unit):
            coordinates.append((unit.x, unit.y))
    return coordinates