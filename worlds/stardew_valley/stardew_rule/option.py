from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Mapping, Optional, Union, Set

from BaseClasses import CollectionState
from .base import BaseStardewRule
from .protocol import StardewRule, PlayerWorldContext
from .state import Received


@dataclass(frozen=True)
class BaseOptionRule(BaseStardewRule, ABC):
    option_name: str

    def get_option_value(self, context: PlayerWorldContext) -> Union[int, str, Set[str]]:
        return context.get_option_value(self.option_name)

    @abstractmethod
    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        ...

    def __call__(self, state: CollectionState, context: PlayerWorldContext) -> bool:
        return self.choose_rule(context)(state, context)

    def evaluate_while_simplifying(self, state: CollectionState, context: PlayerWorldContext) -> Tuple[StardewRule, bool]:
        return self.choose_rule(context).evaluate_while_simplifying(state, context)

    def get_difficulty(self, context: PlayerWorldContext):
        return self.choose_rule(context).get_difficulty(context)

    # TODO implement explanation


@dataclass(frozen=True)
class ChooseOptionRule(BaseOptionRule):
    default: Optional[StardewRule]
    choices: Mapping[int, StardewRule]

    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        try:
            return self.choices[self.get_option_value(context)]
        except KeyError:
            return self.default

    def __hash__(self):
        return hash((self.option_name, self.default, id(self.choices)))


@dataclass(frozen=True)
class BitwiseOptionRule(BaseOptionRule):
    binary_value: int
    match: StardewRule
    no_match: StardewRule

    def choose_rule(self, context: PlayerWorldContext):
        if self.get_option_value(context) & self.binary_value:
            return self.match
        else:
            return self.no_match


@dataclass(frozen=True)
class OptionReceived(BaseOptionRule):
    item: str

    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        return Received(self.item, context.get_option_value(self.option_name))

    def __repr__(self):
        return f"Received [Option {self.option_name}] {self.item}"
