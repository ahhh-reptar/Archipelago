from functools import cached_property

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from ..content.vanilla.base import base_game
from ..data.harvest import HarvestCropSource
from ..stardew_rule import StardewRule, true_, True_, False_
from ..strings.ap_names.ap_option_names import EatsanityOptionName
from ..strings.currency_names import Currency
from ..strings.food_names import Meal
from ..strings.ingredient_names import Ingredient
from ..strings.metal_names import Mineral
from ..strings.performance_names import Performance
from ..strings.quality_names import ForageQuality
from ..strings.region_names import Region, LogicRegion
from ..strings.skill_names import Skill, all_mod_skills, all_vanilla_skills
from ..strings.tool_names import ToolMaterial, Tool, FishingRod
from ..strings.wallet_item_names import Wallet


class SkillLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = SkillLogic(*args, **kwargs)


class SkillLogic(BaseLogic):

    # Should be cached
    def can_earn_level(self, skill: str, level: int) -> StardewRule:
        assert level > 0, "There is no level before level 0."

        tool_level = min(5, (level + 1) // 2)
        tool_material = ToolMaterial.tiers[tool_level]

        previous_level_rule = self.logic.skill.has_previous_level(skill, level)

        if skill == Skill.fishing:
            # Not checking crab pot as this is used for not randomized skills logic, for which players need a fishing rod to start gaining xp.
            # We want to cap the tool level at 4, because the advanced iridium rod is excluded from logic.
            tool_level = min(4, tool_level)
            xp_rule = self.logic.tool.has_fishing_rod(FishingRod.tiers[tool_level]) & self.logic.fishing.can_fish_anywhere()
        elif skill == Skill.farming:
            xp_rule = self.can_get_farming_xp & self.logic.tool.has_tool(Tool.hoe, tool_material) & self.logic.tool.can_water(tool_level)
        elif skill == Skill.foraging:
            xp_rule = (self.can_get_foraging_xp & self.logic.tool.has_tool(Tool.axe, tool_material)) | \
                      self.logic.magic.can_use_clear_debris_instead_of_tool_level(tool_level)
        elif skill == Skill.mining:
            xp_rule = self.logic.tool.has_tool(Tool.pickaxe, tool_material) | \
                      self.logic.magic.can_use_clear_debris_instead_of_tool_level(tool_level)
            xp_rule = xp_rule & self.logic.region.can_reach(Region.mines_floor_5)
        elif skill == Skill.combat:
            # Tool level starts at 1, so we need to subtract 1 to get the correct performance tier.
            combat_tier = Performance.tiers[tool_level - 1]
            xp_rule = self.logic.combat.can_fight_at_level(combat_tier)
            xp_rule = xp_rule & self.logic.region.can_reach(Region.mines_floor_5)
        elif skill in all_mod_skills:
            # Ideal solution would be to add a logic registry, but I'm too lazy.
            return previous_level_rule & self.logic.mod.skill.can_earn_mod_skill_level(skill, level)
        else:
            raise Exception(f"Unknown skill: {skill}")

        return previous_level_rule & xp_rule

    # Should be cached
    def has_level(self, skill: str, level: int) -> StardewRule:
        assert level >= 0, "There is no level before level 0."
        if level == 0:
            return true_

        if self.content.features.skill_progression.is_progressive:
            if level > 10:
                if skill == Skill.fishing:
                    return self.logic.received(f"{skill} Level", 10) & self.has_fishing_buffs_available(level - 10)
                raise f"Cannot reach level {level} {skill}"
            return self.logic.received(f"{skill} Level", level)

        return self.logic.skill.can_earn_level(skill, level)

    def has_fishing_buffs_available(self, buff_levels: int) -> StardewRule:

        eat_rule = self.can_eat_fishing_buff(buff_levels)
        rod_rule = self.logic.tool.has_fishing_rod(FishingRod.advanced_iridium)
        enchant_rule = self.logic.region.can_reach(Region.volcano_floor_10) & self.logic.has(Mineral.prismatic_shard) & self.logic.has(
            Currency.cinder_shard) & self.can_eat_fishing_buff(buff_levels - 1)
        chef_rule = self.logic.region.can_reach(LogicRegion.desert_festival) & self.can_eat_fishing_buff(buff_levels - 3)

        return eat_rule | (rod_rule & enchant_rule) | chef_rule

    def can_eat_fishing_buff(self, buff_levels: int) -> StardewRule:
        enzyme_rule = self.logic.true_
        food_rule = self.logic.true_

        if buff_levels <= 0:
            return self.logic.true_
        elif buff_levels >= 6:
            return self.logic.false_

        potential_foods = {
            1: [Meal.maple_bar, Meal.chowder, Meal.trout_soup, Meal.shrimp_cocktail],
            2: [Meal.escargot, Meal.fish_taco],
            3: [Meal.dish_o_the_sea, Meal.fish_stew, Meal.lobster_bisque],
            4: [Meal.seafoam_pudding],
        }

        foods_correct_level = []
        foods_only_with_seasoning_level = []
        for level in potential_foods:
            if level >= buff_levels:
                foods_correct_level.extend(potential_foods[level])
            if level == buff_levels-1:
                foods_only_with_seasoning_level.extend(potential_foods[level])

        normal_food_rule = self.logic.or_(*[self.logic.has(food) for food in foods_correct_level], allow_empty=True)
        qi_seasoning_food_rule = self.logic.has(Ingredient.qi_seasoning) &\
                                 self.logic.or_(*[self.logic.cooking.can_cook(food) for food in foods_only_with_seasoning_level], allow_empty=True)
        food_rule = normal_food_rule | qi_seasoning_food_rule

        if EatsanityOptionName.lock_effects in self.options.eatsanity:
            enzyme_rule = self.logic.received("Fishing Enzyme", buff_levels)
        return food_rule & enzyme_rule

    def has_previous_level(self, skill: str, level: int) -> StardewRule:
        assert level > 0, "There is no level before level 0."
        if level == 1:
            return true_

        if self.content.features.skill_progression.is_progressive:
            return self.logic.received(f"{skill} Level", level - 1)

        months = max(1, level - 1)
        return self.logic.time.has_lived_months(months)

    @cache_self1
    def has_farming_level(self, level: int) -> StardewRule:
        return self.logic.skill.has_level(Skill.farming, level)

    # Should be cached
    def has_total_level(self, level: int, allow_modded_skills: bool = False) -> StardewRule:
        if level <= 0:
            return True_()

        if self.content.features.skill_progression.is_progressive:
            skills = base_game.skills
            if allow_modded_skills:
                skills = self.content.skills.values()
            skill_items = [skill.level_name for skill in skills]

            return self.logic.received_n(*skill_items, count=level)

        months_with_4_skills = max(1, (level // 4) - 1)
        months_with_5_skills = max(1, (level // 5) - 1)
        rule_with_fishing = self.logic.time.has_lived_months(months_with_5_skills) & self.logic.skill.can_get_fishing_xp
        if level > 40:
            return rule_with_fishing
        return self.logic.time.has_lived_months(months_with_4_skills) | rule_with_fishing

    def has_any_skills_maxed(self, included_modded_skills: bool = True) -> StardewRule:
        skills = self.content.skills.keys() if included_modded_skills else sorted(all_vanilla_skills)
        return self.logic.or_(*(self.logic.skill.has_level(skill, 10) for skill in skills))

    @cached_property
    def can_get_farming_xp(self) -> StardewRule:
        sources = self.content.find_sources_of_type(HarvestCropSource)
        crop_rules = []
        for crop_source in sources:
            crop_rules.append(self.logic.harvesting.can_harvest_crop_from(crop_source))
        return self.logic.or_(*crop_rules)

    @cached_property
    def can_get_foraging_xp(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.axe)
        tree_rule = self.logic.region.can_reach(Region.forest) & self.logic.season.has_any_not_winter()
        stump_rule = self.logic.region.can_reach(Region.secret_woods) & self.logic.tool.has_tool(Tool.axe, ToolMaterial.copper)
        return tool_rule & (tree_rule | stump_rule)

    @cached_property
    def can_get_mining_xp(self) -> StardewRule:
        tool_rule = self.logic.tool.has_tool(Tool.pickaxe)
        stone_rule = self.logic.region.can_reach_any(Region.mines_floor_5, Region.quarry, Region.skull_cavern_25, Region.volcano_floor_5)
        return tool_rule & stone_rule

    @cached_property
    def can_get_combat_xp(self) -> StardewRule:
        tool_rule = self.logic.combat.has_any_weapon()
        enemy_rule = self.logic.region.can_reach_any(Region.mines_floor_5, Region.skull_cavern_25, Region.volcano_floor_5)
        return tool_rule & enemy_rule

    @cached_property
    def can_get_fishing_xp(self) -> StardewRule:
        if self.content.features.skill_progression.is_progressive:
            return self.logic.fishing.can_fish_anywhere() | self.logic.fishing.can_crab_pot_anywhere

        return self.logic.fishing.can_fish_anywhere()

    def can_forage_quality(self, quality: str) -> StardewRule:
        if quality == ForageQuality.basic:
            return True_()
        if quality == ForageQuality.silver:
            return self.has_level(Skill.foraging, 5)
        if quality == ForageQuality.gold:
            return self.has_level(Skill.foraging, 9)
        return False_()

    def can_earn_mastery(self, skill: str) -> StardewRule:
        # Checking for level 11, so it includes having level 10 and being able to earn xp.
        return self.logic.skill.can_earn_level(skill, 11) & self.logic.region.can_reach(Region.mastery_cave)

    def has_mastery(self, skill: str) -> StardewRule:
        if self.content.features.skill_progression.are_masteries_shuffled:
            return self.logic.received(f"{skill} Mastery")

        return self.logic.skill.can_earn_mastery(skill)

    @cached_property
    def can_enter_mastery_cave(self) -> StardewRule:
        if self.content.features.skill_progression.are_masteries_shuffled:
            return self.logic.received(Wallet.mastery_of_the_five_ways)

        return self.has_any_skills_maxed(included_modded_skills=False)
