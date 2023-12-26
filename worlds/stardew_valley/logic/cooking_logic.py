from functools import cached_property
from typing import Union

from Utils import cache_self1
from .action_logic import ActionLogicMixin
from .base_logic import BaseLogicMixin, BaseLogic
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .relationship_logic import RelationshipLogicMixin
from .season_logic import SeasonLogicMixin
from .skill_logic import SkillLogicMixin
from .. import options
from ..data.recipe_data import RecipeSource, StarterSource, ShopSource, SkillSource, FriendshipSource, \
    QueenOfSauceSource, CookingRecipe, ShopFriendshipSource, \
    all_cooking_recipes_by_name
from ..data.recipe_source import CutsceneSource, ShopTradeSource
from ..locations import locations_by_tag, LocationTags
from ..stardew_rule import StardewRule, True_, False_, And
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tv_channel_names import Channel

cooksanity_prefix = "Cook "


class CookingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cooking = CookingLogic(*args, **kwargs)


class CookingLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, MoneyLogicMixin, ActionLogicMixin,
BuildingLogicMixin, RelationshipLogicMixin, SkillLogicMixin, CookingLogicMixin, OptionLogicMixin]]):
    @cached_property
    def can_cook_in_kitchen(self) -> StardewRule:
        return self.logic.building.has_house(1) | self.logic.skill.has_level(Skill.foraging, 9)

    # Should be cached
    def can_cook(self, recipe: CookingRecipe = None) -> StardewRule:
        cook_rule = self.logic.region.can_reach(Region.kitchen)
        if recipe is None:
            return cook_rule

        recipe_rule = self.logic.cooking.knows_recipe(recipe.source, recipe.meal)
        ingredients_rule = And(*(self.logic.has(ingredient) for ingredient in recipe.ingredients))
        return cook_rule & recipe_rule & ingredients_rule

    # Should be cached
    def knows_recipe(self, source: RecipeSource, meal_name: str) -> StardewRule:
        default_rule = self.logic.cooking.can_learn_recipe(source)

        if isinstance(source, (ShopTradeSource, ShopSource)):
            return self.logic.option.bitwise_choice(options.Chefsanity,
                                                    value=options.Chefsanity.option_purchases,
                                                    match=self.logic.cooking.received_recipe(meal_name),
                                                    no_match=default_rule)

        if isinstance(source, SkillSource):
            return self.logic.option.bitwise_choice(options.Chefsanity,
                                                    value=options.Chefsanity.option_skills,
                                                    match=self.logic.cooking.received_recipe(meal_name),
                                                    no_match=default_rule)

        if isinstance(source, (CutsceneSource, FriendshipSource, ShopFriendshipSource)):
            return self.logic.option.bitwise_choice(options.Chefsanity,
                                                    value=options.Chefsanity.option_friendship,
                                                    match=self.logic.cooking.received_recipe(meal_name),
                                                    no_match=default_rule)

        if isinstance(source, QueenOfSauceSource):
            return self.logic.option.bitwise_choice(options.Chefsanity,
                                                    value=options.Chefsanity.option_queen_of_sauce,
                                                    match=self.logic.cooking.received_recipe(meal_name),
                                                    no_match=default_rule)

        return default_rule

    @cache_self1
    def can_learn_recipe(self, source: RecipeSource) -> StardewRule:
        if isinstance(source, StarterSource):
            return True_()
        if isinstance(source, ShopTradeSource):
            return self.logic.money.can_trade_at(source.region, source.currency, source.price)
        if isinstance(source, ShopSource):
            return self.logic.money.can_spend_at(source.region, source.price)
        if isinstance(source, SkillSource):
            return self.logic.skill.has_level(source.skill, source.level)
        if isinstance(source, CutsceneSource):
            return self.logic.region.can_reach(source.region) & self.logic.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, FriendshipSource):
            return self.logic.relationship.has_hearts(source.friend, source.hearts)
        if isinstance(source, QueenOfSauceSource):
            return self.logic.action.can_watch(Channel.queen_of_sauce) & self.logic.season.has(source.season)
        if isinstance(source, ShopFriendshipSource):
            return self.logic.money.can_spend_at(source.region, source.price) & self.logic.relationship.has_hearts(source.friend, source.hearts)
        return False_()

    @cache_self1
    def received_recipe(self, meal_name: str):
        return self.logic.received(f"{meal_name} Recipe")

    @cached_property
    def can_cook_everything(self) -> StardewRule:
        def create_rule(exclude_ginger_island, enabled_mods):
            all_recipes_names = []
            exclude_island = exclude_ginger_island == options.ExcludeGingerIsland.option_true
            for location in locations_by_tag[LocationTags.COOKSANITY]:
                if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                    continue
                if location.mod_name and location.mod_name not in enabled_mods:
                    continue
                all_recipes_names.append(location.name[len(cooksanity_prefix):])
            all_recipes = [all_cooking_recipes_by_name[recipe_name] for recipe_name in all_recipes_names]
            return And(*(self.logic.cooking.can_cook(recipe) for recipe in all_recipes))

        return self.logic.option.custom_rule(options.ExcludeGingerIsland, options.Mods, rule_factory=create_rule)
