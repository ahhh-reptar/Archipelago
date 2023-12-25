from __future__ import annotations

from abc import abstractmethod
from typing import Tuple, Protocol, runtime_checkable, Union, Set

from BaseClasses import CollectionState
from .explanation import ExplainableRule


class PlayerWorldContext(Protocol):
    """
    Offers a read only view on the multi world, from the player perspective.
    """
    player: int

    # Maybe add starting inventory

    def get_option_value(self, option: str) -> Union[int, str, Set[str]]:
        ...

    def get_option_values(self, *options: str) -> Tuple[Union[int, str, Set[str]], ...]:
        ...


@runtime_checkable
class StardewRule(ExplainableRule, Protocol):

    @abstractmethod
    def __call__(self, state: CollectionState, context: PlayerWorldContext) -> bool:
        ...

    @abstractmethod
    def evaluate_while_simplifying(self, state: CollectionState, context: PlayerWorldContext) -> Tuple[StardewRule, bool]:
        ...

    @abstractmethod
    def get_difficulty(self, world: PlayerWorldContext):
        ...

    @abstractmethod
    def __or__(self, other) -> StardewRule:
        ...

    @abstractmethod
    def __and__(self, other) -> StardewRule:
        ...
