import itertools
from typing import Dict

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from . import options, locations
from .bundles import Bundle
from .logic import StardewLogic, _And, season_per_skill_level, tool_prices

help_wanted_per_season = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter",
    5: "Year Two",
}


def set_rules(multi_world: MultiWorld, player: int, world_options: options.StardewOptions, logic: StardewLogic,
              current_bundles: Dict[str, Bundle]):
    summer = multi_world.get_location("Summer", player)

    for floor in range(5, 120 + 5, 5):
        MultiWorldRules.add_rule(multi_world.get_entrance(f"Dig to The Mines - Floor {floor}", player),
                                 logic.can_mine_to_floor(floor).simplify())

    MultiWorldRules.add_rule(multi_world.get_entrance("Enter the Quarry", player),
                             logic.received("Bridge Repair").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Enter the Secret Woods", player),
                             logic.has_tool("Axe", "Iron").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Take the Bus to the Desert", player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Enter the Skull Cavern", player),
                             logic.received("Skull Key").simplify())

    MultiWorldRules.add_rule(multi_world.get_entrance("Use the Desert Obelisk", player),
                             logic.received("Desert Obelisk").simplify())
    MultiWorldRules.add_rule(multi_world.get_entrance("Use the Island Obelisk", player),
                             logic.received("Island Obelisk").simplify())

    # Those checks do not exist if ToolProgression is vanilla
    if world_options[options.ToolProgression] != options.ToolProgression.option_vanilla:
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Fiberglass Rod", player),
                                 (logic.has_skill_level("Fishing", 2) & logic.can_spend_money(1800)).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Purchase Iridium Rod", player),
                                 (logic.has_skill_level("Fishing", 6) & logic.can_spend_money(7500)).simplify())

        materials = [None, "Copper", "Iron", "Gold", "Iridium"]
        tool = ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]
        for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
            if previous is None:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") &
                                          logic.can_spend_money(tool_prices[material])).simplify())
            else:
                MultiWorldRules.add_rule(multi_world.get_location(f"{material} {tool} Upgrade", player),
                                         (logic.has(f"{material} Ore") & logic.has_tool(tool, previous) &
                                          logic.can_spend_money(tool_prices[material])).simplify())

    # Skills
    if world_options[options.SkillProgression] != options.SkillProgression.option_vanilla:
        for i in range(1, 11):
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Farming", player),
                                     (logic.received(season_per_skill_level["Farming", i])).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Fishing", player),
                                     (logic.can_get_fishing_xp() &
                                      logic.received(season_per_skill_level["Fishing", i])).simplify())
            MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                     logic.received(season_per_skill_level["Foraging", i]).simplify())
            if i >= 6:
                MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                         logic.has_tool("Axe", "Iron").simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Mining", player),
                                     logic.received(season_per_skill_level["Mining", i]).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Combat", player),
                                     (logic.received(season_per_skill_level["Combat", i]) &
                                      logic.has_any_weapon()).simplify())

    # Bundles
    for bundle in current_bundles.values():
        MultiWorldRules.set_rule(multi_world.get_location(bundle.get_name_with_bundle(), player),
                                 logic.can_complete_bundle(bundle.requirements, bundle.number_required).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Crafts Room", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.crafts_room_bundle).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Pantry", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.pantry_bundles).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Fish Tank", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.fish_tank_bundles).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Boiler Room", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.boiler_room_bundles).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Bulletin Board", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.bulletin_board_bundles).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Vault", player),
                             _And(logic.can_reach_location(bundle.name)
                                  for bundle in locations.vault_bundles).simplify())

    # Buildings
    if world_options[options.BuildingProgression] != options.BuildingProgression.option_vanilla:
        for building in locations.buildings:
            MultiWorldRules.set_rule(multi_world.get_location(building.name, player),
                                     logic.building_rules[building.name.removesuffix(" Blueprint")].simplify())

    # Story Quests
    for quest in locations.story_quests:
        MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                 logic.quest_rules[quest.name].simplify())

    # Story Quests
    for quest in locations.help_wanted_quests:
        prefix = "Help Wanted: "
        words = quest.name.split(" ")
        level = int(words[-1])
        type_of_quest = quest.name[len(prefix):-(1 + len(words[-1]))]
        if type_of_quest == "Item Delivery":
            level = int((level + 1) / 2)
        rule = logic.received(help_wanted_per_season[min(5, level)])
        if type_of_quest == "Fishing":
            rule = rule & logic.can_fish()
        if type_of_quest == "Slay Monsters":
            rule = rule & logic.has_any_weapon()

        MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                 rule.simplify())

    if world_options[options.BuildingProgression] == options.BuildingProgression.option_progressive_early_shipping_bin:
        summer.access_rule = summer.access_rule & logic.received("Building: Shipping Bin")

    # Backpacks
    if world_options[options.BackpackProgression] != options.BackpackProgression.option_vanilla:
        MultiWorldRules.add_rule(multi_world.get_location("Large Pack", player),
                                 logic.can_spend_money(2000).simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Deluxe Pack", player),
                                 logic.can_spend_money(10000).simplify())

    if world_options[options.BackpackProgression] == options.BackpackProgression.option_early_progressive:
        summer.access_rule = summer.access_rule & logic.received("Progressive Backpack")
        MultiWorldRules.add_rule(multi_world.get_location("Winter", player),
                                 logic.received("Progressive Backpack", 2).simplify())

    MultiWorldRules.add_rule(multi_world.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())

    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Junimo Kart", player),
                                 (logic.received("Skull Key") & logic.has("Junimo Kart Small Buff")).simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 2", player),
                                 logic.has("Junimo Kart Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 3", player),
                                 logic.has("Junimo Kart Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Junimo Kart Victory", player),
                                 logic.has("Junimo Kart Max Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Journey of the Prairie King", player),
                                 logic.has("JotPK Small Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 2", player),
                                 logic.has("JotPK Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 3", player),
                                 logic.has("JotPK Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Journey of the Prairie King Victory", player),
                                 logic.has("JotPK Max Buff").simplify())
