from typing import Dict

from ..mod_data import ModNames
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...stardew_rule import StardewRule
from ...strings.artisan_good_names import ModArtisanGood
from ...strings.craftable_names import ModCraftable
from ...strings.ingredient_names import Ingredient
from ...strings.material_names import Material
from ...strings.metal_names import all_fossils, all_artifacts, Ore, ModFossil
from ...strings.monster_drop_names import Loot
from ...strings.performance_names import Performance
from ...strings.region_names import SVERegion, DeepWoodsRegion, BoardingHouseRegion
from ...strings.tool_names import Tool, ToolMaterial

display_types = [ModCraftable.wooden_display, ModCraftable.hardwood_display]
display_items = all_artifacts + all_fossils


class ModItemLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = ModItemLogic(*args, **kwargs)


class ModItemLogic(BaseLogic):

    def get_modded_item_rules(self) -> Dict[str, StardewRule]:
        items = dict()
        if self.content.is_enabled(ModNames.boarding_house):
            items.update(self.get_boarding_house_item_rules())
        return items

    def modify_vanilla_item_rules_with_mod_additions(self, item_rule: Dict[str, StardewRule]):
        if self.content.is_enabled(ModNames.sve):
            item_rule.update(self.get_modified_item_rules_for_sve(item_rule))
        if self.content.is_enabled(ModNames.deepwoods):
            item_rule.update(self.get_modified_item_rules_for_deep_woods(item_rule))
        return item_rule

    def get_modified_item_rules_for_sve(self, items: Dict[str, StardewRule]):
        return {
            Loot.void_essence: items[Loot.void_essence] | self.logic.region.can_reach(SVERegion.highlands_cavern) | self.logic.region.can_reach(
                SVERegion.crimson_badlands),
            Loot.solar_essence: items[Loot.solar_essence] | self.logic.region.can_reach(SVERegion.crimson_badlands),
            Ore.copper: items[Ore.copper] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.highlands_cavern) &
                                             self.logic.combat.can_fight_at_level(Performance.great)),
            Ore.iron: items[Ore.iron] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.highlands_cavern) &
                                         self.logic.combat.can_fight_at_level(Performance.great)),
            Ore.iridium: items[Ore.iridium] | (self.logic.tool.can_use_tool_at(Tool.pickaxe, ToolMaterial.basic, SVERegion.crimson_badlands) &
                                               self.logic.combat.can_fight_at_level(Performance.maximum)),

        }

    def get_modified_item_rules_for_deep_woods(self, items: Dict[str, StardewRule]):
        options_to_update = {
            Material.hardwood: items[Material.hardwood] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.iron, DeepWoodsRegion.floor_10),
            Ingredient.sugar: items[Ingredient.sugar] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.gold, DeepWoodsRegion.floor_50),
            # Gingerbread House
            Ingredient.wheat_flour: items[Ingredient.wheat_flour] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.gold, DeepWoodsRegion.floor_50),
            # Gingerbread House
        }

        if self.content.features.tool_progression.is_progressive:
            options_to_update.update({
                Ore.iridium: items[Ore.iridium] | self.logic.tool.can_use_tool_at(Tool.axe, ToolMaterial.iridium, DeepWoodsRegion.floor_50),  # Iridium Tree
            })

        return options_to_update

    def get_boarding_house_item_rules(self):
        can_reach_any_boarding_house_region = self.logic.region.can_reach_any(BoardingHouseRegion.lost_valley_ruins, BoardingHouseRegion.lost_valley_house_1,
                                                                              BoardingHouseRegion.lost_valley_house_2)
        can_fight_at_good_level_in_boarding_house = can_reach_any_boarding_house_region & self.logic.combat.can_fight_at_level(Performance.good)
        can_fight_at_great_level_in_boarding_house = can_reach_any_boarding_house_region & self.logic.combat.can_fight_at_level(Performance.great)
        return {
            # Mob Drops from lost valley enemies
            ModArtisanGood.pterodactyl_egg: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_claw: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_ribs: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_vertebra: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_skull: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_phalange: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_l_wing_bone: can_fight_at_good_level_in_boarding_house,
            ModFossil.pterodactyl_r_wing_bone: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_skull: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_tooth: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_femur: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_pelvis: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_ribs: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_vertebra: can_fight_at_good_level_in_boarding_house,
            ModFossil.dinosaur_claw: can_fight_at_good_level_in_boarding_house,
            ModFossil.neanderthal_skull: can_fight_at_great_level_in_boarding_house,
            ModFossil.neanderthal_ribs: can_fight_at_great_level_in_boarding_house,
            ModFossil.neanderthal_pelvis: can_fight_at_great_level_in_boarding_house,
            ModFossil.neanderthal_limb_bones: can_fight_at_great_level_in_boarding_house,
        }
