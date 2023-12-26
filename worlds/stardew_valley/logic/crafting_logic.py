from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .option_logic import OptionLogicMixin
from .quest_logic import QuestLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .skill_logic import SkillLogicMixin
from .special_order_logic import SpecialOrderLogicMixin
from .. import options
from ..data.craftable_data import CraftingRecipe, all_crafting_recipes_by_name
from ..data.recipe_data import StarterSource, ShopSource, SkillSource, FriendshipSource
from ..data.recipe_source import CutsceneSource, ShopTradeSource, ArchipelagoSource, LogicSource, SpecialOrderSource, \
    FestivalShopSource, QuestSource
from ..locations import locations_by_tag, LocationTags
from ..options import SpecialOrderLocations, ExcludeGingerIsland
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.region_names import Region

craftsanity_prefix = "Craft "


class CraftingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crafting = CraftingLogic(*args, **kwargs)


class CraftingLogic(BaseLogic[Union[ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, MoneyLogicMixin, RelationshipLogicMixin,
SkillLogicMixin, SpecialOrderLogicMixin, CraftingLogicMixin, QuestLogicMixin, OptionLogicMixin]]):
    @cache_self1
    def can_craft(self, recipe: CraftingRecipe = None) -> StardewRule:
        if recipe is None:
            return True_()

        learn_rule = self.logic.crafting.knows_recipe(recipe)
        ingredients_rule = And(*(self.logic.has(ingredient) for ingredient in recipe.ingredients))
        return learn_rule & ingredients_rule

    @cache_self1
    def knows_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        if isinstance(recipe.source, ArchipelagoSource):
            return self.logic.received(recipe.source.ap_item, len(recipe.source.ap_item))

        if isinstance(recipe.source, FestivalShopSource):
            return self.logic.option.choice(options.FestivalLocations,
                                            value=options.FestivalLocations.option_disabled,
                                            match=self.logic.crafting.can_learn_recipe(recipe),
                                            no_match=self.logic.crafting.received_recipe(recipe.item))

        if isinstance(recipe.source, QuestSource):
            return self.logic.option.choice(options.QuestLocations,
                                            value=options.QuestLocations.special_range_names["none"],
                                            match=self.logic.crafting.can_learn_recipe(recipe),
                                            no_match=self.logic.crafting.received_recipe(recipe.item))

        if isinstance(recipe.source, (StarterSource, ShopTradeSource, ShopSource)):
            return self.logic.option.choice(options.Craftsanity,
                                            value=options.Craftsanity.option_none,
                                            match=self.logic.crafting.can_learn_recipe(recipe),
                                            no_match=self.logic.crafting.received_recipe(recipe.item))

        if isinstance(recipe.source, SpecialOrderSource):
            def has_craftsanity_and_special_order_randomization(craftsanity, special_order_randomization):
                return craftsanity != options.Craftsanity.option_none and special_order_randomization != SpecialOrderLocations.option_disabled

            return self.logic.option.complex_choice(options.Craftsanity, options.SpecialOrderLocations,
                                                    condition=has_craftsanity_and_special_order_randomization,
                                                    match=self.logic.crafting.received_recipe(recipe.item),
                                                    no_match=self.logic.crafting.can_learn_recipe(recipe))

        return self.logic.crafting.can_learn_recipe(recipe)

    @cache_self1
    def can_learn_recipe(self, recipe: CraftingRecipe) -> StardewRule:
        if isinstance(recipe.source, StarterSource):
            return True_()

        if isinstance(recipe.source, ArchipelagoSource):
            return self.logic.received(recipe.source.ap_item, len(recipe.source.ap_item))

        if isinstance(recipe.source, ShopTradeSource):
            return self.logic.money.can_trade_at(recipe.source.region, recipe.source.currency, recipe.source.price)

        if isinstance(recipe.source, ShopSource):
            return self.logic.money.can_spend_at(recipe.source.region, recipe.source.price)

        if isinstance(recipe.source, SkillSource):
            return self.logic.skill.has_level(recipe.source.skill, recipe.source.level)

        if isinstance(recipe.source, CutsceneSource):
            return self.logic.region.can_reach(recipe.source.region) & self.logic.relationship.has_hearts(recipe.source.friend, recipe.source.hearts)

        if isinstance(recipe.source, FriendshipSource):
            return self.logic.relationship.has_hearts(recipe.source.friend, recipe.source.hearts)

        if isinstance(recipe.source, QuestSource):
            return self.logic.quest.can_complete_quest(recipe.source.quest)

        if isinstance(recipe.source, SpecialOrderSource):
            return self.logic.option.choice(options.SpecialOrderLocations,
                                            value=options.SpecialOrderLocations.option_disabled,
                                            match=self.logic.special_order.can_complete_special_order(recipe.source.special_order),
                                            no_match=self.logic.crafting.received_recipe(recipe.item))

        if isinstance(recipe.source, LogicSource):
            if recipe.source.logic_rule == "Cellar":
                return self.logic.region.can_reach(Region.cellar)

        return False_()

    @cache_self1
    def received_recipe(self, item_name: str):
        return self.logic.received(f"{item_name} Recipe")

    @cached_property
    def can_craft_everything(self) -> StardewRule:
        def create_rule(exclude_ginger_island, enabled_mods):
            all_recipes_names = []
            exclude_island = exclude_ginger_island == ExcludeGingerIsland.option_true
            for location in locations_by_tag[LocationTags.CRAFTSANITY]:
                if not location.name.startswith(craftsanity_prefix):
                    continue
                if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                    continue
                if location.mod_name and location.mod_name not in enabled_mods:
                    continue
                all_recipes_names.append(location.name[len(craftsanity_prefix):])
            all_recipes = [all_crafting_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
            return And(*(self.logic.crafting.can_craft(recipe) for recipe in all_recipes))

        return self.logic.option.custom_rule(options.ExcludeGingerIsland, options.Mods, rule_factory=create_rule)
