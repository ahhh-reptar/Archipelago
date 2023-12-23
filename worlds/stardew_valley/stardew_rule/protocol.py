from __future__ import annotations

from abc import abstractmethod
from typing import Tuple, Protocol, runtime_checkable

from BaseClasses import CollectionState
from .explanation import ExplainableRule


class APRule(Protocol):
    @abstractmethod
    def __call__(self, state: CollectionState) -> bool:
        ...


@runtime_checkable
class StardewRule(APRule, ExplainableRule, Protocol):

    @abstractmethod
    def __or__(self, other) -> StardewRule:
        ...

    @abstractmethod
    def __and__(self, other) -> StardewRule:
        ...

    @abstractmethod
    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        ...

    @abstractmethod
    def get_difficulty(self):
        ...
