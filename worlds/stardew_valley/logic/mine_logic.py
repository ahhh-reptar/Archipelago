from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .combat_logic import CombatLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .skill_logic import SkillLogicMixin
from .tool_logic import ToolLogicMixin
from .. import options
from ..stardew_rule import StardewRule, And, true_
from ..strings.performance_names import Performance
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import Tool, ToolMaterial


class MineLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mine = MineLogic(*args, **kwargs)


class MineLogic(BaseLogic[Union[MineLogicMixin, RegionLogicMixin, ReceivedLogicMixin, CombatLogicMixin, ToolLogicMixin, SkillLogicMixin, OptionLogicMixin]]):
    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_5)

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_45)

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.logic.region.can_reach(Region.mines_floor_85)

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.logic.mine.can_progress_in_the_mines_from_floor(120) &
                self.logic.region.can_reach(Region.skull_cavern))

    @cache_self1
    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.logic.combat.can_fight_at_level(Performance.galaxy)
        if tier >= 3:
            return self.logic.combat.can_fight_at_level(Performance.great)
        if tier >= 2:
            return self.logic.combat.can_fight_at_level(Performance.good)
        if tier >= 1:
            return self.logic.combat.can_fight_at_level(Performance.decent)
        return self.logic.combat.can_fight_at_level(Performance.basic)

    @cache_self1
    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        assert floor >= 0, "Can't use elevator to go to a negative floor."
        mine_tier = floor // 40

        has_weapon_to_progress = self.logic.mine.get_weapon_rule_for_floor_tier(mine_tier)

        required_tool_tier = mine_tier
        has_tools_to_progress = self.logic.option.bitwise_choice_or_true(options.ToolProgression,
                                                                         value=options.ToolProgression.option_progressive,
                                                                         match=self.logic.tool.has_tool(Tool.pickaxe, ToolMaterial.tiers[required_tool_tier]))

        required_skill_tier = min(10, max(0, mine_tier * 2))
        progressive_skill_rule = self.logic.skill.has_level(Skill.combat, required_skill_tier) & self.logic.skill.has_level(Skill.mining, required_skill_tier)
        has_skills_to_progress = self.logic.option.choice_or_true(options.SkillProgression,
                                                                  value=options.SkillProgression.option_progressive,
                                                                  match=progressive_skill_rule)

        return And(has_weapon_to_progress, has_tools_to_progress, has_skills_to_progress)

    @cache_self1
    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        assert floor >= 0, "Can't use elevator to go to a negative floor."

        return self.logic.option.choice(options.ElevatorProgression,
                                        value=options.ElevatorProgression.option_vanilla,
                                        match=true_,
                                        no_match=self.logic.received("Progressive Mine Elevator", floor // 5))

    @cache_self1
    def can_progress_in_the_skull_cavern_from_floor(self, floor: int) -> StardewRule:
        assert floor >= 0, "Can't use elevator to go to a negative floor."
        skull_cavern_tier = floor // 50

        has_weapon_to_progress = self.logic.combat.has_great_weapon

        required_tool_tier = min(4, max(0, skull_cavern_tier + 2))
        has_tools_to_progress = (self.logic.option.bitwise_choice_or_true(options.ToolProgression,
                                                                          value=options.ToolProgression.option_progressive,
                                                                          match=self.logic.tool.has_tool(Tool.pickaxe, ToolMaterial.tiers[required_tool_tier])))

        required_skill_tier = min(10, max(0, skull_cavern_tier * 2 + 6))
        progressive_skill_rule = self.logic.skill.has_level(Skill.combat, required_skill_tier) & self.logic.skill.has_level(Skill.mining, required_skill_tier)
        has_skills_to_progress = self.logic.option.choice_or_true(options.SkillProgression,
                                                                  value=options.SkillProgression.option_progressive,
                                                                  match=progressive_skill_rule)

        return And(has_weapon_to_progress, has_tools_to_progress, has_skills_to_progress)
