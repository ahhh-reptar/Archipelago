from typing import Union

from .magic_logic import MagicLogicMixin
from ... import options
from ...data.villagers_data import all_villagers
from ...logic.action_logic import ActionLogicMixin
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.building_logic import BuildingLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.fishing_logic import FishingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.option_logic import OptionLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.region_logic import RegionLogicMixin
from ...logic.relationship_logic import RelationshipLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...mods.mod_data import ModNames
from ...stardew_rule import Count, StardewRule, False_, True_
from ...strings.building_names import Building
from ...strings.geode_names import Geode
from ...strings.machine_names import Machine
from ...strings.region_names import Region
from ...strings.skill_names import ModSkill
from ...strings.spells import MagicSpell
from ...strings.tool_names import Tool, ToolMaterial


class ModSkillLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = ModSkillLogic(*args, **kwargs)


class ModSkillLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, ActionLogicMixin, RelationshipLogicMixin, BuildingLogicMixin,
ToolLogicMixin, FishingLogicMixin, CookingLogicMixin, MagicLogicMixin, OptionLogicMixin]]):
    def has_mod_level(self, skill: str, level: int) -> StardewRule:
        assert level >= 0, "Can't have a negative skill level."
        if level <= 0:
            return True_()

        return self.logic.option.choice(options.SkillProgression,
                                        value=options.SkillProgression.option_progressive,
                                        match=self.logic.received(f"{skill} Level", level),
                                        no_match=self.can_earn_mod_skill_level(skill, level))

    def can_earn_mod_skill_level(self, skill: str, level: int) -> StardewRule:
        if skill == ModSkill.luck:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.luck_skill,
                                                              match=self.can_earn_luck_skill_level(level))
        if skill == ModSkill.magic:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.magic,
                                                              match=self.can_earn_magic_skill_level(level))
        if skill == ModSkill.socializing:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.socializing_skill,
                                                              match=self.can_earn_socializing_skill_level(level))
        if skill == ModSkill.archaeology:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.archaeology,
                                                              match=self.can_earn_archaeology_skill_level(level))
        if skill == ModSkill.cooking:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.cooking_skill,
                                                              match=self.can_earn_cooking_skill_level(level))
        if skill == ModSkill.binning:
            return self.logic.option.contains_choice_or_false(options.Mods,
                                                              value=ModNames.binning_skill,
                                                              match=self.can_earn_binning_skill_level(level))
        return False_()

    def can_earn_luck_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.fishing.can_fish_chests() | self.logic.action.can_open_geode(Geode.magma)
        else:
            return self.logic.fishing.can_fish_chests() | self.logic.action.can_open_geode(Geode.geode)

    def can_earn_magic_skill_level(self, level: int) -> StardewRule:
        spell_count = [self.logic.received(MagicSpell.clear_debris), self.logic.received(MagicSpell.water),
                       self.logic.received(MagicSpell.blink), self.logic.received(MagicSpell.fireball),
                       self.logic.received(MagicSpell.frostbite),
                       self.logic.received(MagicSpell.descend), self.logic.received(MagicSpell.tendrils),
                       self.logic.received(MagicSpell.shockwave),
                       self.logic.received(MagicSpell.meteor),
                       self.logic.received(MagicSpell.spirit)]
        return Count(level, spell_count)

    def can_earn_socializing_skill_level(self, level: int) -> StardewRule:
        def create_rule(enabled_mods):
            villager_count = []
            for villager in all_villagers:
                if villager.mod_name in enabled_mods or villager.mod_name is None:
                    villager_count.append(self.logic.relationship.can_earn_relationship(villager.name, level))
            return Count(level * 2, villager_count)

        return self.logic.option.custom_rule(options.Mods, rule_factory=create_rule)

    def can_earn_archaeology_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.action.can_pan() | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.gold)
        else:
            return self.logic.action.can_pan() | self.logic.tool.has_tool(Tool.hoe, ToolMaterial.basic)

    def can_earn_cooking_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.cooking.can_cook() & self.logic.region.can_reach(Region.saloon) & \
                self.logic.building.has_building(Building.coop) & self.logic.building.has_building(Building.barn)
        else:
            return self.logic.cooking.can_cook()

    def can_earn_binning_skill_level(self, level: int) -> StardewRule:
        if level >= 6:
            return self.logic.has(Machine.recycling_machine)
        else:
            return True_()  # You can always earn levels 1-5 with trash cans
