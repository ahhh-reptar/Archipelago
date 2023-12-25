from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Mapping, Optional, Union, Set, Protocol

from BaseClasses import CollectionState
from .base import BaseStardewRule
from .protocol import StardewRule, PlayerWorldContext
from .state import Received


@dataclass(frozen=True)
class BaseOptionRule(BaseStardewRule, ABC):

    @abstractmethod
    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        ...

    def __call__(self, state: CollectionState, context: PlayerWorldContext) -> bool:
        return self.choose_rule(context)(state, context)

    def evaluate_while_simplifying(self, state: CollectionState, context: PlayerWorldContext) -> Tuple[StardewRule, bool]:
        return self.choose_rule(context).evaluate_while_simplifying(state, context)

    def get_difficulty(self, context: PlayerWorldContext):
        return self.choose_rule(context).get_difficulty(context)


@dataclass(frozen=True)
class SingleOptionRule(BaseOptionRule, ABC):
    option_name: str

    def get_option_value(self, context: PlayerWorldContext) -> Union[int, str, Set[str]]:
        return context.get_option_value(self.option_name)


@dataclass(frozen=True)
class ChooseOptionRule(SingleOptionRule):
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
class BitwiseOptionRule(SingleOptionRule):
    binary_value: int
    match: StardewRule
    no_match: StardewRule

    def choose_rule(self, context: PlayerWorldContext):
        if self.get_option_value(context) & self.binary_value:
            return self.match
        else:
            return self.no_match


class ReceivedAmountFunction(Protocol):
    def __call__(self, option_value: int) -> int:
        ...


@dataclass(frozen=True)
class OptionReceived(SingleOptionRule):
    item: str
    transform_received_amount: ReceivedAmountFunction

    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        return Received(self.item, self.compute_received_amount(context))

    def compute_received_amount(self, context):
        return self.transform_received_amount(self.get_option_value(context))

    def __repr__(self):
        return f"Received [Option {self.option_name}] {self.item}"


class RuleFactory(Protocol):
    def __call__(self, *option_values: Union[str, int, Set[str]]) -> StardewRule:
        ...


@dataclass(frozen=True)
class CustomOptionRule(BaseOptionRule):
    rule_factory: RuleFactory
    option_dependency_names: Tuple[str, ...]

    def choose_rule(self, context: PlayerWorldContext) -> StardewRule:
        # TODO add cache based on option dependencies, mods will be a problem because the option is a set and not a frozenset ...
        return self.rule_factory(*context.get_option_values(*self.option_dependency_names))
