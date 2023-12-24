from abc import ABC
from dataclasses import dataclass
from typing import Tuple, Mapping, Type

from BaseClasses import CollectionState, ItemClassification
from .base import BaseStardewRule
from .protocol import StardewRule, PlayerWorldContext
from .state import Received
from ..items import item_table
from ..options import StardewValleyOption


@dataclass(frozen=True)
class BaseOptionRule(BaseStardewRule, ABC):
    option: Type[StardewValleyOption]

    @property
    def option_name(self):
        return self.option.internal_name


@dataclass(frozen=True)
class ChoiceOptionRule(BaseOptionRule):
    choices: Mapping[int, StardewRule]

    def choose_rule(self, context: PlayerWorldContext):
        option_value = context.get_option_value(self.option_name)
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


@dataclass(frozen=True)
class OptionReceived(BaseOptionRule):
    item: str

    def __post_init__(self):
        assert item_table[self.item].classification & ItemClassification.progression, \
            f"Item [{item_table[self.item].name}] has to be progression to be used in logic"

    def __call__(self, state: CollectionState, context: PlayerWorldContext) -> bool:
        return state.has(self.item, context.player, context.get_option_value(self.option_name))

    def evaluate_while_simplifying(self, state: CollectionState, context: PlayerWorldContext) -> Tuple[StardewRule, bool]:
        simplified = Received(self.item, context.get_option_value(self.option_name))
        return simplified, simplified(state, context)

    def __repr__(self):
        return f"Received [Options {self.option.display_name}] {self.item}"

    def get_difficulty(self, context: PlayerWorldContext):
        return context.get_option_value(self.option_name)
