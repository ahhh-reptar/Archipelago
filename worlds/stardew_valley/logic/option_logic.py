from types import MappingProxyType
from typing import Type, Mapping, Any, Union, Optional

from BaseClasses import ItemClassification
from Options import Choice, NamedRange
from .base_logic import BaseLogic, BaseLogicMixin
from ..items import item_table
from ..options import StardewValleyOption
from ..stardew_rule import StardewRule, ChooseOptionRule, OptionReceived, ReceivedAmountFunction, BitwiseOptionRule, CustomOptionRule, RuleFactory, Condition, \
    ComplexChoiceOptionRule, SimpleChoiceOptionRule, false_, true_


class OptionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option = OptionLogic(*args, **kwargs)


class OptionLogic(BaseLogic[None]):

    @staticmethod
    def choice(option: Type[StardewValleyOption], /, *, value: Any, match: StardewRule, no_match: StardewRule) -> StardewRule:
        return SimpleChoiceOptionRule(option.internal_name, value, match, no_match)

    @staticmethod
    def choice_or_true(option: Type[StardewValleyOption], /, *, value: Any, match: StardewRule) -> StardewRule:
        return OptionLogic.choice(option, value=value, match=match, no_match=true_)

    @staticmethod
    def choice_or_false(option: Type[StardewValleyOption], /, *, value: Any, match: StardewRule) -> StardewRule:
        return OptionLogic.choice(option, value=value, match=match, no_match=false_)

    @staticmethod
    def bitwise_choice(option: Type[StardewValleyOption], /, *, value: int, match: StardewRule, no_match: StardewRule):
        return BitwiseOptionRule(option.internal_name, value, match, no_match)

    @staticmethod
    def bitwise_choice_or_true(option: Type[StardewValleyOption], /, *, value: int, match: StardewRule):
        return OptionLogic.choice(option, value=value, match=match, no_match=true_)

    @staticmethod
    def choose(option: Union[Type[StardewValleyOption], Type[Choice], Type[NamedRange]], /, *,
               choices: Mapping[Any, StardewRule],
               default: Optional[StardewRule] = None):
        assert len(choices) > 1, "'choose' rules are made for multiple choices. Use 'simple choice' if you only need one choice."

        if not default:
            assert not issubclass(option, NamedRange), "A default choice is mandatory when using NamedRange options."

            for value_name, value_value in option.options.items():
                assert value_value in choices.keys(), \
                    f"All possible value must be supplied in 'choices' when there is no default, a choice for [{value_name}] is missing."

        return ChooseOptionRule(option.internal_name, default, MappingProxyType(choices))

    @staticmethod
    def complex_choice(*option_dependencies: Type[StardewValleyOption], condition: Condition, match: StardewRule, no_match: StardewRule) -> StardewRule:
        return ComplexChoiceOptionRule(tuple(option.internal_name for option in option_dependencies), condition, match, no_match)

    @staticmethod
    def received(option: Type[StardewValleyOption], item: str, received_amount_function: ReceivedAmountFunction = lambda x: x) -> StardewRule:
        assert item_table[item].classification & ItemClassification.progression, f"Item [{item}] has to be progression to be used in logic"
        return OptionReceived(option.internal_name, item, received_amount_function)

    @staticmethod
    def custom_rule(*option_dependencies: Type[StardewValleyOption], rule_factory: RuleFactory) -> StardewRule:
        return CustomOptionRule(tuple(option.internal_name for option in option_dependencies), rule_factory)
