from typing import Union

from ... import options
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.combat_logic import CombatLogicMixin
from ...logic.cooking_logic import CookingLogicMixin
from ...logic.has_logic import HasLogicMixin
from ...logic.option_logic import OptionLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...logic.skill_logic import SkillLogicMixin
from ...logic.tool_logic import ToolLogicMixin
from ...mods.mod_data import ModNames
from ...stardew_rule import StardewRule, And, true_
from ...strings.ap_names.mods.mod_items import DeepWoodsItem, SkillItem
from ...strings.ap_names.transport_names import ModTransportation
from ...strings.craftable_names import Bomb
from ...strings.food_names import Meal
from ...strings.performance_names import Performance
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool, ToolMaterial


class DeepWoodsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deepwoods = DeepWoodsLogic(*args, **kwargs)


class DeepWoodsLogic(BaseLogic[Union[SkillLogicMixin, ReceivedLogicMixin, HasLogicMixin, CombatLogicMixin, ToolLogicMixin, SkillLogicMixin, OptionLogicMixin,
CookingLogicMixin]]):

    def can_reach_woods_depth(self, depth: int) -> StardewRule:
        def create_rule(skill_progression):
            tier = int(depth / 25) + 1
            rules = []
            if depth > 10:
                rules.append(self.logic.has(Bomb.bomb) | self.logic.tool.has_tool(Tool.axe, ToolMaterial.iridium))
            if depth > 30:
                rules.append(self.logic.received(ModTransportation.woods_obelisk))
            if depth > 50:
                rules.append(self.logic.combat.can_fight_at_level(Performance.great) & self.logic.cooking.can_cook() &
                             self.logic.received(ModTransportation.woods_obelisk))
            if skill_progression == options.SkillProgression.option_progressive:
                combat_tier = min(10, max(0, tier + 5))
                rules.append(self.logic.skill.has_level(Skill.combat, combat_tier))
            return And(*rules)

        return self.logic.option.custom_rule(options.SkillProgression, rule_factory=create_rule)

    def has_woods_rune_to_depth(self, floor: int) -> StardewRule:
        return self.logic.option.choice(options.ElevatorProgression,
                                        value=options.ElevatorProgression.option_vanilla,
                                        match=true_,
                                        no_match=self.logic.received(DeepWoodsItem.obelisk_sigil, int(floor / 10)))

    def can_chop_to_depth(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 10, 0)
        return (self.has_woods_rune_to_depth(previous_elevator) &
                self.can_reach_woods_depth(previous_elevator))

    def can_pull_sword(self) -> StardewRule:
        def create_rule(enabled_mods):
            rules = [self.logic.received(DeepWoodsItem.pendant_depths) & self.logic.received(DeepWoodsItem.pendant_community) &
                     self.logic.received(DeepWoodsItem.pendant_elder),
                     self.logic.skill.has_total_level(40)]
            if ModNames.luck_skill in enabled_mods:
                rules.append(self.logic.received(SkillItem.luck_skill, 7))
            else:
                # You need more luck than this, but it'll push the logic down a ways; you can get the rest there.
                rules.append(self.logic.has(Meal.magic_rock_candy))
            return And(*rules)

        return self.logic.option.custom_rule(options.Mods, rule_factory=create_rule)
