from dataclasses import dataclass
from typing import Tuple, Mapping

from BaseClasses import CollectionState
from Options import Choice
from .base import BaseStardewRule
from .protocol import StardewRule


@dataclass(frozen=True)
class ChoiceOptionRule(BaseStardewRule):
    option: Choice
    choices: Mapping[int, StardewRule]

    def __call__(self, state: CollectionState) -> bool:
        return self.choices[self.option.value](state)

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self.choices[self.option.value].evaluate_while_simplifying(state)

    def get_difficulty(self):
        return self.choices[self.option.value].get_difficulty()

    def __hash__(self):
        return id(self.choices)
