from dataclasses import dataclass
from typing import Tuple, Mapping, Type, Union

from BaseClasses import CollectionState
from Options import Choice
from .base import BaseStardewRule
from .protocol import StardewRule, PlayerWorldContext
from ..options import StardewValleyOption


@dataclass(frozen=True)
class ChoiceOptionRule(BaseStardewRule):
    option: Type[Union[StardewValleyOption, Choice]]
    choices: Mapping[int, StardewRule]

    def choose_rule(self, context: PlayerWorldContext):
        option_value = context.get_option_value(self.option)
        return self.choices[option_value]

    def __call__(self, state: CollectionState, context: PlayerWorldContext) -> bool:
        return self.choose_rule(context)(state, context)

    def evaluate_while_simplifying(self, state: CollectionState, context: PlayerWorldContext) -> Tuple[StardewRule, bool]:
        return self.choose_rule(context).evaluate_while_simplifying(state, context)

    def get_difficulty(self, context: PlayerWorldContext):
        return self.choose_rule(context).get_difficulty(context)

    def __hash__(self):
        return id(self.choices)

    # TODO implement explanation
