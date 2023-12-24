from __future__ import annotations

from typing import TypeVar, Generic, Dict

from ..options import StardewValleyOptions
from ..stardew_rule import StardewRule


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
    registry: LogicRegistry
    options: StardewValleyOptions
    logic: T

    def __init__(self, registry: LogicRegistry, options: StardewValleyOptions, logic: T):
        super().__init__(registry, options, logic)
        self.registry = registry
        self.options = options
        self.logic = logic
