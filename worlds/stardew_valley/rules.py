import itertools
from typing import Dict

from BaseClasses import MultiWorld
from worlds.generic import Rules as MultiWorldRules
from . import options, locations
from .bundles import Bundle
from .locations import LocationTags
from .logic import StardewLogic, And, month_end_per_skill_level, tool_prices, week_days
from worlds.stardew_valley.data.minerals_data import all_museum_items, all_mineral_items, all_artifact_items, dwarf_scrolls, skeleton_front, \
    skeleton_middle, skeleton_back


def set_rules(multi_world: MultiWorld, player: int, world_options: options.StardewOptions, logic: StardewLogic,
              current_bundles: Dict[str, Bundle]):
    all_location_names = list(location.name for location in multi_world.get_locations(player))

    for floor in range(5, 120 + 5, 5):
        MultiWorldRules.set_rule(multi_world.get_entrance(f"Dig to The Mines - Floor {floor}", player),
                                 logic.can_mine_to_floor(floor).simplify())

    MultiWorldRules.set_rule(multi_world.get_entrance("Enter Quarry", player),
                             logic.received("Bridge Repair").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance("Enter Secret Woods", player),
                             logic.has_tool("Axe", "Iron").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance("Take Bus to Desert", player),
                             logic.received("Bus Repair").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance("Enter Skull Cavern", player),
                             logic.received("Skull Key").simplify())

    MultiWorldRules.set_rule(multi_world.get_entrance("Use Desert Obelisk", player),
                             logic.received("Desert Obelisk").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance("Use Island Obelisk", player),
                             logic.received("Island Obelisk").simplify())
    MultiWorldRules.set_rule(multi_world.get_entrance("Talk to Traveling Merchant", player),
                             logic.has_traveling_merchant())
    MultiWorldRules.set_rule(multi_world.get_entrance("Enter Greenhouse", player),
                             logic.received("Greenhouse"))

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
                                     (logic.received("Month End", month_end_per_skill_level["Farming", i])).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Fishing", player),
                                     (logic.can_get_fishing_xp() &
                                      logic.received("Month End", month_end_per_skill_level["Fishing", i])).simplify())
            MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                     logic.received("Month End", month_end_per_skill_level["Foraging", i]).simplify())
            if i >= 6:
                MultiWorldRules.add_rule(multi_world.get_location(f"Level {i} Foraging", player),
                                         logic.has_tool("Axe", "Iron").simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Mining", player),
                                     logic.received("Month End", month_end_per_skill_level["Mining", i]).simplify())
            MultiWorldRules.set_rule(multi_world.get_location(f"Level {i} Combat", player),
                                     (logic.received("Month End", month_end_per_skill_level["Combat", i]) &
                                      logic.has_any_weapon()).simplify())

    # Bundles
    for bundle in current_bundles.values():
        MultiWorldRules.set_rule(multi_world.get_location(bundle.get_name_with_bundle(), player),
                                 logic.can_complete_bundle(bundle.requirements, bundle.number_required).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Crafts Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.CRAFTS_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Pantry", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.PANTRY_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Fish Tank", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.FISH_TANK_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Boiler Room", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.BOILER_ROOM_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Bulletin Board", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle
                                 in locations.locations_by_tag[LocationTags.BULLETIN_BOARD_BUNDLE]).simplify())
    MultiWorldRules.add_rule(multi_world.get_location("Complete Vault", player),
                             And(logic.can_reach_location(bundle.name)
                                 for bundle in locations.locations_by_tag[LocationTags.VAULT_BUNDLE]).simplify())

    # Buildings
    if world_options[options.BuildingProgression] != options.BuildingProgression.option_vanilla:
        for building in locations.locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
            MultiWorldRules.set_rule(multi_world.get_location(building.name, player),
                                     logic.building_rules[building.name.replace(" Blueprint", "")].simplify())

    # Story Quests
    for quest in locations.locations_by_tag[LocationTags.QUEST]:
        MultiWorldRules.set_rule(multi_world.get_location(quest.name, player),
                                 logic.quest_rules[quest.name].simplify())

    # Help Wanted Quests
    desired_number_help_wanted: int = world_options[options.HelpWantedLocations] // 7
    for i in range(1, desired_number_help_wanted + 1):
        prefix = "Help Wanted:"
        delivery = "Item Delivery"
        rule = logic.received("Month End", i - 1)
        fishing_rule = rule & logic.can_fish()
        slay_rule = rule & logic.has_any_weapon()
        for j in range(i, i + 4):
            MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} {delivery} {j}", player),
                                     rule.simplify())

        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Gathering {i}", player),
                                 rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Fishing {i}", player),
                                 fishing_rule.simplify())
        MultiWorldRules.set_rule(multi_world.get_location(f"{prefix} Slay Monsters {i}", player),
                                 slay_rule.simplify())

    set_fishsanity_rules(all_location_names, logic, multi_world, player)
    set_museumsanity_rules(all_location_names, logic, multi_world, player, world_options)
    set_backpack_rules(logic, multi_world, player, world_options)

    MultiWorldRules.set_rule(multi_world.get_location("Old Master Cannoli", player),
                             logic.has("Sweet Gem Berry").simplify())
    MultiWorldRules.set_rule(multi_world.get_location("Galaxy Sword Shrine", player),
                             logic.has("Prismatic Shard").simplify())

    set_traveling_merchant_rules(logic, multi_world, player)
    set_arcade_machine_rules(logic, multi_world, player, world_options)


def set_fishsanity_rules(all_location_names: list[str], logic: StardewLogic, multi_world: MultiWorld, player: int):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            MultiWorldRules.set_rule(multi_world.get_location(fish_location.name, player),
                                     logic.has(fish_name).simplify())


def set_museumsanity_rules(all_location_names: list[str], logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    museum_prefix = "Museumsanity: "
    if world_options[options.Museumsanity] == options.Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, multi_world, museum_milestone, museum_prefix, player)
    elif world_options[options.Museumsanity] != options.Museumsanity.option_none:
        for museum_location in locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            if museum_location.name in all_location_names:
                donation_name = museum_location.name[len(museum_prefix):]
                MultiWorldRules.set_rule(multi_world.get_location(museum_location.name, player),
                                         logic.has(donation_name).simplify())


def set_museum_milestone_rule(logic: StardewLogic, multi_world: MultiWorld, museum_milestone, museum_prefix: str, player: int):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    rule = None
    if milestone_name.endswith(donations_suffix):
        num = int(milestone_name[:len(donations_suffix)])
        rule = logic.has([item.name for item in all_museum_items], num)
    elif milestone_name.endswith(minerals_suffix):
        num = int(milestone_name[:len(minerals_suffix)])
        rule = logic.has([item.name for item in all_mineral_items], num)
    elif milestone_name.endswith(artifacts_suffix):
        num = int(milestone_name[:len(artifacts_suffix)])
        rule = logic.has([item.name for item in all_artifact_items], num)
    elif milestone_name == "Dwarf Scrolls":
        rule = logic.has([item.name for item in dwarf_scrolls])
    elif milestone_name == "Skeleton Front":
        rule = logic.has([item.name for item in skeleton_front])
    elif milestone_name == "Skeleton Middle":
        rule = logic.has([item.name for item in skeleton_middle])
    elif milestone_name == "Skeleton Back":
        rule = logic.has([item.name for item in skeleton_back])
    MultiWorldRules.set_rule(multi_world.get_location(museum_milestone.name, player), rule.simplify())


def set_backpack_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    if world_options[options.BackpackProgression] != options.BackpackProgression.option_vanilla:
        MultiWorldRules.set_rule(multi_world.get_location("Large Pack", player),
                                 logic.can_spend_money(2000).simplify())
        MultiWorldRules.set_rule(multi_world.get_location("Deluxe Pack", player),
                                 (logic.can_spend_money(10000) & logic.received("Progressive Backpack")).simplify())


def set_traveling_merchant_rules(logic: StardewLogic, multi_world: MultiWorld, player: int):
    for day in week_days:
        item_for_day = f"Traveling Merchant: {day}"
        for i in range(1, 4):
            location_name = f"Traveling Merchant {day} Item {i}"
            MultiWorldRules.set_rule(multi_world.get_location(location_name, player),
                                     logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multi_world: MultiWorld, player: int, world_options):
    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Junimo Kart", player),
                                 (logic.received("Skull Key") & logic.has("Junimo Kart Small Buff")).simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 2", player),
                                 logic.has("Junimo Kart Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach Junimo Kart 3", player),
                                 logic.has("Junimo Kart Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Junimo Kart: Sunset Speedway (Victory)", player),
                                 logic.has("Junimo Kart Max Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Play Journey of the Prairie King", player),
                                 logic.has("JotPK Small Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 2", player),
                                 logic.has("JotPK Medium Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_entrance("Reach JotPK World 3", player),
                                 logic.has("JotPK Big Buff").simplify())
        MultiWorldRules.add_rule(multi_world.get_location("Journey of the Prairie King Victory", player),
                                 logic.has("JotPK Max Buff").simplify())
