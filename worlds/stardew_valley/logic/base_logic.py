from __future__ import annotations

import functools
import inspect
from typing import Optional, Union
from typing import TypeVar, Generic, Dict

import Utils
from Options import Option
from .region_logic import always_regions_by_setting
from .time_logic import MONTH_COEFFICIENT, MAX_MONTHS
from ..options import StardewValleyOptions
from ..stardew_rule import StardewRule, True_, HasProgressionPercent, Received, Reach


class LogicRegistry:

    def __init__(self):
        self.item_rules: Dict[str, StardewRule] = {}
        self.sapling_rules: Dict[str, StardewRule] = {}
        self.tree_fruit_rules: Dict[str, StardewRule] = {}
        self.seed_rules: Dict[str, StardewRule] = {}
        self.cooking_rules: Dict[str, StardewRule] = {}
        self.crafting_rules: Dict[str, StardewRule] = {}
        self.crop_rules: Dict[str, StardewRule] = {}
        self.fish_rules: Dict[str, StardewRule] = {}
        self.museum_rules: Dict[str, StardewRule] = {}
        self.festival_rules: Dict[str, StardewRule] = {}
        self.quest_rules: Dict[str, StardewRule] = {}
        self.building_rules: Dict[str, StardewRule] = {}
        self.special_order_rules: Dict[str, StardewRule] = {}

        self.sve_location_rules: Dict[str, StardewRule] = {}


class BaseLogicMixin:
    def __init__(self, *args, **kwargs):
        pass


T = TypeVar("T", bound=BaseLogicMixin)


class BaseLogic(BaseLogicMixin, Generic[T]):
    player: int
    registry: LogicRegistry
    options: StardewValleyOptions
    logic: T

    def __init__(self, player: int, registry: LogicRegistry, options: StardewValleyOptions, logic: T):
        super().__init__(player, registry, options, logic)
        self.player = player
        self.registry = registry
        self.options = options
        self.logic = logic


def option_dependency(function):
    parameters_by_name = inspect.signature(function).parameters

    option_dependencies = tuple(parameter.annotation for parameter in parameters_by_name.values() if issubclass(parameter.annotation, Option))
    assert bool(option_dependencies), "You need to declare the option dependencies with type hinting on the parameters."

    def function_with_option_dependencies(*args, **kwargs):
        def rule_factory(*option_values):
            return function(*args, *option_values, **kwargs)

        return  # CustomOptionRule(tuple(option.internal_name for option in option_dependencies), rule_factory)

    return function_with_option_dependencies


def option_dependency_cached_property(function):
    return functools.cached_property(option_dependency(function))


def option_dependency_cache_self1(function):
    # All those shenanigans are needed because cache_self1 checks that the function is caches have exactly two arguments,
    #  preventing the combination of other decorators.

    dependency_declared_function = option_dependency(function)

    def function_with_2_args(arg1, arg2):
        return dependency_declared_function(arg1, arg2)

    return Utils.cache_self1(function_with_2_args)


"""
@rule could register a cache in the class when there is no option dependency, or in the instance when it depends on the option. Calling a method that requires 
option or player could return a placeholder.

"""


def rule(function):
    pass


class ReceivedLogicMixin(BaseLogic[None], BaseLogicMixin):
    # Should be cached
    @rule
    def received(self, item: str, count: Optional[int] = 1) -> StardewRule:
        assert count >= 0, "Can't receive a negative amount of item."

        return Received(item, self.player, count)


class RegionLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = RegionLogic(*args, **kwargs)


class RegionLogic(BaseLogic[Union[RegionLogicMixin]]):

    def can_reach(self, region_name: str, ) -> StardewRule:
        if region_name in always_regions_by_setting[self.options.entrance_randomization]:
            return True_()

        return Reach(region_name, "Region", self.player)


class TimeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = TimeLogic(*args, **kwargs)


class TimeLogic(BaseLogic[Union[TimeLogicMixin, ReceivedLogicMixin]]):

    def has_lived_months(self, number: int) -> StardewRule:
        if number <= 0:
            return True_()
        number = min(number, MAX_MONTHS)
        return HasProgressionPercent(self.player, number * MONTH_COEFFICIENT)
