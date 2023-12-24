from types import MappingProxyType
from typing import Type, Mapping, Any, Union, Optional

from BaseClasses import ItemClassification
from Options import Choice
from .base_logic import BaseLogic, BaseLogicMixin
from ..items import item_table
from ..options import StardewValleyOption
from ..stardew_rule import StardewRule, ChooseOptionRule, OptionReceived, BitwiseOptionRule


class OptionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option = OptionLogic(*args, **kwargs)


class OptionLogic(BaseLogic[None]):

    @staticmethod
    def choose(option: Union[Type[StardewValleyOption], Choice], /, *, choices: Mapping[Any, StardewRule], default: Optional[StardewRule] = None):
        if not default:
            for value_name, value_value in option.options.items():
                assert value_value in choices.keys(), \
                    f"All possible value must be supplied in 'choices' when there is no default, a choice for [{value_name}] is missing."

        return ChooseOptionRule(option.internal_name, default, MappingProxyType(choices))

    @staticmethod
    def bitwise_choice(option: Type[StardewValleyOption], /, *, value: int, match: StardewRule, no_match: StardewRule):
        return BitwiseOptionRule(option.internal_name, value, match, no_match)

    @staticmethod
    def received(option: Type[StardewValleyOption], item: str) -> StardewRule:
        assert item_table[item].classification & ItemClassification.progression, f"Item [{item}] has to be progression to be used in logic"
        return OptionReceived(option.internal_name, item)
