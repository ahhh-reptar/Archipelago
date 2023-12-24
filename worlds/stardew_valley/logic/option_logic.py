from types import MappingProxyType
from typing import Type, Mapping, Any

from .base_logic import BaseLogic, BaseLogicMixin
from ..options import StardewValleyOption
from ..stardew_rule import StardewRule, ChoiceOptionRule, OptionReceived


class OptionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option = OptionLogic(*args, **kwargs)


class OptionLogic(BaseLogic[None]):

    @staticmethod
    def choose(option: Type[StardewValleyOption], choices: Mapping[Any, StardewRule]):
        return ChoiceOptionRule(option.internal_name, MappingProxyType(choices))

    @staticmethod
    def received(item: str, option: Type[StardewValleyOption]) -> StardewRule:
        return OptionReceived(option.internal_name, item)
