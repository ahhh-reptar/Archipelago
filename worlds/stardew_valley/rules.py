import itertools
from typing import List

from . import locations
from .bundles.bundle_room import BundleRoom
from .data.craftable_data import all_crafting_recipes_by_name
from .data.monster_data import all_monsters_by_category, all_monsters_by_name
from .data.museum_data import all_museum_items, dwarf_scrolls, skeleton_front, skeleton_middle, skeleton_back, all_museum_items_by_name, all_museum_minerals, \
    all_museum_artifacts, Artifact
from .data.recipe_data import all_cooking_recipes_by_name
from .locations import LocationTags
from .logic.logic import StardewLogic
from .logic.tool_logic import tool_upgrade_prices
from .mods.mod_data import ModNames
from .multi_world_adapter import PlayerMultiWorldAdapter
from .options import Friendsanity
from .options import ToolProgression, BuildingProgression, ExcludeGingerIsland, SpecialOrderLocations, Museumsanity, BackpackProgression, Shipsanity, \
    Monstersanity, Chefsanity, Craftsanity, ArcadeMachineLocations, Cooksanity, Cropsanity, SkillProgression
from .stardew_rule import And, true_
from .strings.ap_names.event_names import Event
from .strings.ap_names.mods.mod_items import SVELocation
from .strings.ap_names.mods.mod_items import SVEQuestItem
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.building_names import Building
from .strings.bundle_names import CCRoom
from .strings.calendar_names import Weekday
from .strings.craftable_names import Bomb
from .strings.crop_names import Fruit
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, DeepWoodsEntrance, AlecEntrance, MagicEntrance, \
    SVEEntrance
from .strings.generic_names import Generic
from .strings.material_names import Material
from .strings.metal_names import MetalBar
from .strings.quest_names import Quest, ModQuest
from .strings.region_names import Region, SVERegion
from .strings.season_names import Season
from .strings.skill_names import ModSkill, Skill
from .strings.tool_names import Tool, ToolMaterial
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet


def set_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter, bundle_rooms: List[BundleRoom]):
    all_location_names = [location.name for location in world.get_all_locations()]

    # FIXME it's ridiculous how we pass there parameters of every single function. This should be in a class.
    set_entrance_rules(logic, world)
    set_ginger_island_rules(logic, world)

    set_tool_rules(logic, world)
    set_skills_rules(logic, world)
    set_bundle_rules(bundle_rooms, logic, world)
    set_building_rules(logic, world)
    set_cropsanity_rules(all_location_names, logic, world)
    set_story_quests_rules(all_location_names, logic, world)
    set_special_order_rules(all_location_names, logic, world)
    set_help_wanted_quests_rules(logic, world)
    set_fishsanity_rules(all_location_names, logic, world)
    set_museumsanity_rules(all_location_names, logic, world)

    set_friendsanity_rules(all_location_names, logic, world)
    set_backpack_rules(logic, world)
    set_festival_rules(all_location_names, logic, world)
    set_monstersanity_rules(all_location_names, logic, world)
    set_shipsanity_rules(all_location_names, logic, world)
    set_cooksanity_rules(all_location_names, logic, world)
    set_chefsanity_rules(all_location_names, logic, world)
    set_craftsanity_rules(all_location_names, logic, world)
    set_isolated_locations_rules(logic, world)
    set_traveling_merchant_day_rules(logic, world)
    set_arcade_machine_rules(logic, world)

    set_deepwoods_rules(logic, world)
    set_magic_spell_rules(logic, world)
    set_sve_rules(logic, world)


def set_isolated_locations_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.add_location_rule("Old Master Cannoli", logic.has(Fruit.sweet_gem_berry))
    world.add_location_rule("Galaxy Sword Shrine", logic.has("Prismatic Shard"))
    world.add_location_rule("Krobus Stardrop", logic.money.can_spend(20000))
    world.add_location_rule("Demetrius's Breakthrough", logic.money.can_have_earned_total(25000))


def set_tool_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if not world.options.tool_progression & ToolProgression.option_progressive:
        return

    world.add_location_rule("Purchase Fiberglass Rod", (logic.skill.has_level(Skill.fishing, 2) & logic.money.can_spend(1800)))
    world.add_location_rule("Purchase Iridium Rod", (logic.skill.has_level(Skill.fishing, 6) & logic.money.can_spend(7500)))

    materials = [None, "Copper", "Iron", "Gold", "Iridium"]
    tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.watering_can, Tool.trash_can]
    for (previous, material), tool in itertools.product(zip(materials[:4], materials[1:]), tool):
        if previous is None:
            continue
        world.set_location_rule(f"{material} {tool} Upgrade", logic.tool.has_tool(tool, previous))


def set_building_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if not world.options.building_progression & BuildingProgression.option_progressive:
        return

    for building in locations.locations_by_tag[LocationTags.BUILDING_BLUEPRINT]:
        if building.mod_name is not None and not world.has_mod(building.mod_name):
            continue

        world.set_location_rule(building.name, logic.registry.building_rules[building.name.replace(" Blueprint", "")])


def set_bundle_rules(bundle_rooms: List[BundleRoom], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    for bundle_room in bundle_rooms:
        room_rules = []
        for bundle in bundle_room.bundles:
            bundle_rules = logic.bundle.can_complete_bundle(bundle)
            room_rules.append(bundle_rules)
            world.set_location_rule(bundle.name, bundle_rules)

        if bundle_room.name == CCRoom.abandoned_joja_mart:
            continue

        room_location = f"Complete {bundle_room.name}"
        world.add_location_rule(room_location, And(*room_rules))


def set_skills_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    mods = world.options.mods
    if world.options.skill_progression == SkillProgression.option_vanilla:
        return
    for i in range(1, 11):
        set_vanilla_skill_rule_for_level(logic, world, i)
        set_modded_skill_rule_for_level(logic, world, mods, i)


def set_vanilla_skill_rule_for_level(logic: StardewLogic, world: PlayerMultiWorldAdapter, level: int):
    set_vanilla_skill_rule(logic, world, Skill.farming, level)
    set_vanilla_skill_rule(logic, world, Skill.fishing, level)
    set_vanilla_skill_rule(logic, world, Skill.foraging, level)
    set_vanilla_skill_rule(logic, world, Skill.mining, level)
    set_vanilla_skill_rule(logic, world, Skill.combat, level)


def set_modded_skill_rule_for_level(logic: StardewLogic, world: PlayerMultiWorldAdapter, mods, level: int):
    if ModNames.luck_skill in mods:
        set_modded_skill_rule(logic, world, ModSkill.luck, level)
    if ModNames.magic in mods:
        set_modded_skill_rule(logic, world, ModSkill.magic, level)
    if ModNames.binning_skill in mods:
        set_modded_skill_rule(logic, world, ModSkill.binning, level)
    if ModNames.cooking_skill in mods:
        set_modded_skill_rule(logic, world, ModSkill.cooking, level)
    if ModNames.socializing_skill in mods:
        set_modded_skill_rule(logic, world, ModSkill.socializing, level)
    if ModNames.archaeology in mods:
        set_modded_skill_rule(logic, world, ModSkill.archaeology, level)


def get_skill_level_location(skill: str, level: int) -> str:
    return f"Level {level} {skill}"


def set_vanilla_skill_rule(logic: StardewLogic, world: PlayerMultiWorldAdapter, skill: str, level: int):
    rule = logic.skill.can_earn_level(skill, level)
    world.set_location_rule(get_skill_level_location(skill, level), rule)


def set_modded_skill_rule(logic: StardewLogic, world: PlayerMultiWorldAdapter, skill: str, level: int):
    rule = logic.mod.skill.can_earn_mod_skill_level(skill, level)
    world.set_location_rule(get_skill_level_location(skill, level), rule)


def set_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    set_mines_floor_entrance_rules(logic, world)
    set_skull_cavern_floor_entrance_rules(logic, world)
    set_blacksmith_entrance_rules(logic, world)
    set_skill_entrance_rules(logic, world)
    set_traveling_merchant_day_rules(logic, world)

    dangerous_mine_rule = logic.mine.has_mine_elevator_to_floor(120) & logic.region.can_reach(Region.qi_walnut_room)
    world.set_entrance_rule(Entrance.dig_to_dangerous_mines_20, dangerous_mine_rule)
    world.set_entrance_rule(Entrance.dig_to_dangerous_mines_60, dangerous_mine_rule)
    world.set_entrance_rule(Entrance.dig_to_dangerous_mines_100, dangerous_mine_rule)

    world.set_entrance_rule(Entrance.enter_tide_pools, logic.received("Beach Bridge") | (logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.enter_quarry, logic.received("Bridge Repair") | (logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.enter_secret_woods, logic.tool.has_tool(Tool.axe, "Iron") | (logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.forest_to_sewer, logic.wallet.has_rusty_key())
    world.set_entrance_rule(Entrance.town_to_sewer, logic.wallet.has_rusty_key())
    world.set_entrance_rule(Entrance.enter_abandoned_jojamart, logic.has_abandoned_jojamart())
    movie_theater_rule = logic.has_movie_theater()
    world.set_entrance_rule(Entrance.enter_movie_theater, movie_theater_rule)
    world.set_entrance_rule(Entrance.purchase_movie_ticket, movie_theater_rule)
    world.set_entrance_rule(Entrance.take_bus_to_desert, logic.received("Bus Repair"))
    world.set_entrance_rule(Entrance.enter_skull_cavern, logic.received(Wallet.skull_key))
    world.set_entrance_rule(Entrance.enter_dangerous_skull_cavern, (logic.received(Wallet.skull_key) & logic.region.can_reach(Region.qi_walnut_room)))
    world.set_entrance_rule(Entrance.talk_to_mines_dwarf, logic.wallet.can_speak_dwarf() & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron))
    world.set_entrance_rule(Entrance.buy_from_traveling_merchant, logic.traveling_merchant.has_days())

    set_farm_buildings_entrance_rules(logic, world)

    world.set_entrance_rule(Entrance.mountain_to_railroad, logic.received("Railroad Boulder Removed"))
    world.set_entrance_rule(Entrance.enter_witch_warp_cave, logic.quest.has_dark_talisman() | (logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.enter_witch_hut, (logic.has(ArtisanGood.void_mayonnaise) | logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.enter_mutant_bug_lair,
                            (logic.received(Event.start_dark_talisman_quest) & logic.relationship.can_meet(NPC.krobus)) | logic.mod.magic.can_blink())
    world.set_entrance_rule(Entrance.enter_casino, logic.quest.has_club_card())

    set_bedroom_entrance_rules(logic, world)
    set_festival_entrance_rules(logic, world)
    world.set_entrance_rule(Entrance.island_cooking, logic.cooking.can_cook_in_kitchen)
    world.set_entrance_rule(Entrance.farmhouse_cooking, logic.cooking.can_cook_in_kitchen)
    world.set_entrance_rule(Entrance.shipping, logic.shipping.can_use_shipping_bin)
    world.set_entrance_rule(Entrance.watch_queen_of_sauce, logic.action.can_watch(Channel.queen_of_sauce))


def set_farm_buildings_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.set_entrance_rule(Entrance.use_desert_obelisk, logic.can_use_obelisk(Transportation.desert_obelisk))
    world.set_entrance_rule(Entrance.use_island_obelisk, logic.can_use_obelisk(Transportation.island_obelisk))
    world.set_entrance_rule(Entrance.use_farm_obelisk, logic.can_use_obelisk(Transportation.farm_obelisk))
    world.set_entrance_rule(Entrance.enter_greenhouse, logic.received("Greenhouse"))
    world.set_entrance_rule(Entrance.enter_coop, logic.building.has_building(Building.coop))
    world.set_entrance_rule(Entrance.enter_barn, logic.building.has_building(Building.barn))
    world.set_entrance_rule(Entrance.enter_shed, logic.building.has_building(Building.shed))
    world.set_entrance_rule(Entrance.enter_slime_hutch, logic.building.has_building(Building.slime_hutch))


def set_bedroom_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.set_entrance_rule(Entrance.enter_harvey_room, logic.relationship.has_hearts(NPC.harvey, 2))
    world.set_entrance_rule(Entrance.mountain_to_maru_room, logic.relationship.has_hearts(NPC.maru, 2))
    world.set_entrance_rule(Entrance.enter_sebastian_room, (logic.relationship.has_hearts(NPC.sebastian, 2) | logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.forest_to_leah_cottage, logic.relationship.has_hearts(NPC.leah, 2))
    world.set_entrance_rule(Entrance.enter_elliott_house, logic.relationship.has_hearts(NPC.elliott, 2))
    world.set_entrance_rule(Entrance.enter_sunroom, logic.relationship.has_hearts(NPC.caroline, 2))
    world.set_entrance_rule(Entrance.enter_wizard_basement, logic.relationship.has_hearts(NPC.wizard, 4))
    world.set_entrance_rule(Entrance.mountain_to_leo_treehouse, logic.received("Treehouse"))
    if world.has_mod(ModNames.alec):
        world.set_entrance_rule(AlecEntrance.petshop_to_bedroom, (logic.relationship.has_hearts(ModNPC.alec, 2) | logic.mod.magic.can_blink()))


def set_mines_floor_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    elevator_distance = 5
    max_elevator_floor = 120
    amount_of_floor_per_day = 10
    floors_to_check_tier = {5, 45, 85}

    for floor in range(elevator_distance, max_elevator_floor + elevator_distance, elevator_distance):
        # In the first levels accessible from the top of the mine, we only check that the player can progress.
        rule = logic.mine.has_mine_elevator_to_floor(floor - amount_of_floor_per_day) if floor > amount_of_floor_per_day else true_
        if floor in floors_to_check_tier:
            rule = rule & logic.mine.can_progress_in_the_mines_from_floor(floor)

        world.set_entrance_rule(dig_to_mines_floor(floor), rule)


def set_skull_cavern_floor_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    elevator_distance = 25
    max_elevator_floor = 200
    amount_of_floor_per_day = 25
    floors_to_check_tier = {25, 75, 125}

    for floor in range(elevator_distance, max_elevator_floor + elevator_distance, elevator_distance):
        # In the first levels accessible from the top of the mine, we only check that the player can progress.
        rule = logic.mod.elevator.has_skull_cavern_elevator_to_floor(floor - amount_of_floor_per_day) if floor > amount_of_floor_per_day else true_
        if floor in floors_to_check_tier:
            rule = rule & logic.mine.can_progress_in_the_skull_cavern_from_floor(floor)

        world.set_entrance_rule(dig_to_skull_floor(floor), rule)


def set_blacksmith_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    set_blacksmith_upgrade_rule(logic, world, Entrance.blacksmith_copper, MetalBar.copper, ToolMaterial.copper)
    set_blacksmith_upgrade_rule(logic, world, Entrance.blacksmith_iron, MetalBar.iron, ToolMaterial.iron)
    set_blacksmith_upgrade_rule(logic, world, Entrance.blacksmith_gold, MetalBar.gold, ToolMaterial.gold)
    set_blacksmith_upgrade_rule(logic, world, Entrance.blacksmith_iridium, MetalBar.iridium, ToolMaterial.iridium)


def set_skill_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.set_entrance_rule(Entrance.farming, logic.skill.can_get_farming_xp)
    world.set_entrance_rule(Entrance.fishing, logic.skill.can_get_fishing_xp)


def set_blacksmith_upgrade_rule(logic: StardewLogic, world: PlayerMultiWorldAdapter, entrance_name: str, item_name: str, tool_material: str):
    upgrade_rule = logic.has(item_name) & logic.money.can_spend(tool_upgrade_prices[tool_material])
    world.set_entrance_rule(entrance_name, upgrade_rule)


def set_festival_entrance_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.set_entrance_rule(Entrance.attend_egg_festival, logic.season.has(Season.spring))
    world.set_entrance_rule(Entrance.attend_flower_dance, logic.season.has(Season.spring))

    world.set_entrance_rule(Entrance.attend_luau, logic.season.has(Season.summer))
    world.set_entrance_rule(Entrance.attend_moonlight_jellies, logic.season.has(Season.summer))

    world.set_entrance_rule(Entrance.attend_fair, logic.season.has(Season.fall))
    world.set_entrance_rule(Entrance.attend_spirit_eve, logic.season.has(Season.fall))

    world.set_entrance_rule(Entrance.attend_festival_of_ice, logic.season.has(Season.winter))
    world.set_entrance_rule(Entrance.attend_night_market, logic.season.has(Season.winter))
    world.set_entrance_rule(Entrance.attend_winter_star, logic.season.has(Season.winter))


def set_ginger_island_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    set_island_entrances_rules(logic, world)
    if world.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    set_boat_repair_rules(logic, world)
    set_island_parrot_rules(logic, world)
    world.add_location_rule("Open Professor Snail Cave", logic.has(Bomb.cherry_bomb))
    world.add_location_rule("Complete Island Field Office", logic.can_complete_field_office())


def set_boat_repair_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.add_location_rule("Repair Boat Hull", logic.has(Material.hardwood))
    world.add_location_rule("Repair Boat Anchor", logic.has(MetalBar.iridium))
    world.add_location_rule("Repair Ticket Machine", logic.has(ArtisanGood.battery_pack))


def set_island_entrances_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    boat_repaired = logic.received(Transportation.boat_repair)
    world.set_entrance_rule(Entrance.fish_shop_to_boat_tunnel, boat_repaired)
    world.set_entrance_rule(Entrance.boat_to_ginger_island, boat_repaired)
    world.set_entrance_rule(Entrance.island_south_to_west, logic.received("Island West Turtle"))
    world.set_entrance_rule(Entrance.island_south_to_north, logic.received("Island North Turtle"))
    world.set_entrance_rule(Entrance.island_west_to_islandfarmhouse, logic.received("Island Farmhouse"))
    world.set_entrance_rule(Entrance.island_west_to_gourmand_cave, logic.received("Island Farmhouse"))
    dig_site_rule = logic.received("Dig Site Bridge")
    world.set_entrance_rule(Entrance.island_north_to_dig_site, dig_site_rule)
    world.set_entrance_rule(Entrance.dig_site_to_professor_snail_cave, logic.received("Open Professor Snail Cave"))
    world.set_entrance_rule(Entrance.talk_to_island_trader, logic.received("Island Trader"))
    world.set_entrance_rule(Entrance.island_south_to_southeast, logic.received("Island Resort"))
    world.set_entrance_rule(Entrance.use_island_resort, logic.received("Island Resort"))
    world.set_entrance_rule(Entrance.island_west_to_qi_walnut_room, logic.received("Qi Walnut Room"))
    world.set_entrance_rule(Entrance.island_north_to_volcano, (logic.tool.can_water(0) | logic.received("Volcano Bridge") |
                                                               logic.mod.magic.can_blink()))
    world.set_entrance_rule(Entrance.volcano_to_secret_beach, logic.tool.can_water(2))
    world.set_entrance_rule(Entrance.climb_to_volcano_5, (logic.ability.can_mine_perfectly() & logic.tool.can_water(1)))
    world.set_entrance_rule(Entrance.talk_to_volcano_dwarf, logic.wallet.can_speak_dwarf())
    world.set_entrance_rule(Entrance.climb_to_volcano_10, (logic.ability.can_mine_perfectly() & logic.tool.can_water(1)))
    parrots = [Entrance.parrot_express_docks_to_volcano, Entrance.parrot_express_jungle_to_volcano,
               Entrance.parrot_express_dig_site_to_volcano, Entrance.parrot_express_docks_to_dig_site,
               Entrance.parrot_express_jungle_to_dig_site, Entrance.parrot_express_volcano_to_dig_site,
               Entrance.parrot_express_docks_to_jungle, Entrance.parrot_express_dig_site_to_jungle,
               Entrance.parrot_express_volcano_to_jungle, Entrance.parrot_express_jungle_to_docks,
               Entrance.parrot_express_dig_site_to_docks, Entrance.parrot_express_volcano_to_docks]
    parrot_express_rule = logic.received(Transportation.parrot_express)
    parrot_express_to_dig_site_rule = dig_site_rule & parrot_express_rule
    for parrot in parrots:
        if "Dig Site" in parrot:
            world.set_entrance_rule(parrot, parrot_express_to_dig_site_rule)
        else:
            world.set_entrance_rule(parrot, parrot_express_rule)


def set_island_parrot_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    has_walnut = logic.has_walnut(1)
    has_5_walnut = logic.has_walnut(5)
    has_10_walnut = logic.has_walnut(10)
    has_20_walnut = logic.has_walnut(20)
    world.add_location_rule("Leo's Parrot", has_walnut)
    world.add_location_rule("Island West Turtle", has_10_walnut & logic.received("Island North Turtle"))
    world.add_location_rule("Island Farmhouse", has_20_walnut)
    world.add_location_rule("Island Mailbox", has_5_walnut & logic.received("Island Farmhouse"))
    world.add_location_rule(Transportation.farm_obelisk, has_20_walnut & logic.received("Island Mailbox"))
    world.add_location_rule("Dig Site Bridge", has_10_walnut & logic.received("Island West Turtle"))
    world.add_location_rule("Island Trader", has_10_walnut & logic.received("Island Farmhouse"))
    world.add_location_rule("Volcano Bridge", has_5_walnut & logic.received("Island West Turtle") &
                            logic.region.can_reach(Region.volcano_floor_10))
    world.add_location_rule("Volcano Exit Shortcut", has_5_walnut & logic.received("Island West Turtle"))
    world.add_location_rule("Island Resort", has_20_walnut & logic.received("Island Farmhouse"))
    world.add_location_rule(Transportation.parrot_express, has_10_walnut)


def set_cropsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.cropsanity == Cropsanity.option_disabled:
        return

    harvest_prefix = "Harvest "
    harvest_prefix_length = len(harvest_prefix)
    for harvest_location in locations.locations_by_tag[LocationTags.CROPSANITY]:
        if harvest_location.name in all_location_names and (harvest_location.mod_name is None or harvest_location.mod_name in world.options.mods):
            crop_name = harvest_location.name[harvest_prefix_length:]
            world.set_location_rule(harvest_location.name, logic.has(crop_name))


def set_story_quests_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.quest_locations < 0:
        return
    for quest in locations.locations_by_tag[LocationTags.STORY_QUEST]:
        if quest.name in all_location_names and (quest.mod_name is None or quest.mod_name in world.options.mods):
            world.set_location_rule(quest.name, logic.registry.quest_rules[quest.name])


def set_special_order_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.special_order_locations == SpecialOrderLocations.option_disabled:
        return
    board_rule = logic.received("Special Order Board") & logic.time.has_lived_months(4)
    for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
        if board_order.name in all_location_names:
            order_rule = board_rule & logic.registry.special_order_rules[board_order.name]
            world.set_location_rule(board_order.name, order_rule)

    if world.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return
    if world.options.special_order_locations == SpecialOrderLocations.option_board_only:
        return
    qi_rule = logic.region.can_reach(Region.qi_walnut_room) & logic.time.has_lived_months(8)
    for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
        if qi_order.name in all_location_names:
            order_rule = qi_rule & logic.registry.special_order_rules[qi_order.name]
            world.set_location_rule(qi_order.name, order_rule)


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    help_wanted_number = world.options.quest_locations.value
    if help_wanted_number < 0:
        return
    for i in range(0, help_wanted_number):
        set_number = i // 7
        month_rule = logic.time.has_lived_months(set_number)
        quest_number = set_number + 1
        quest_number_in_set = i % 7
        if quest_number_in_set < 4:
            quest_number = set_number * 4 + quest_number_in_set + 1
            set_help_wanted_delivery_rule(world, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(world, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(world, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(world, month_rule, quest_number)


def set_help_wanted_delivery_rule(world, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    world.set_location_rule(location_name, month_rule)


def set_help_wanted_gathering_rule(world, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    world.set_location_rule(location_name, month_rule)


def set_help_wanted_fishing_rule(world, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    world.set_location_rule(location_name, month_rule)


def set_help_wanted_slay_monsters_rule(world, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    world.set_location_rule(location_name, month_rule)


def set_fishsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            world.set_location_rule(fish_location.name, logic.has(fish_name))


def set_museumsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    museum_prefix = "Museumsanity: "
    if world.options.museumsanity == Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, world, museum_milestone, museum_prefix)
    elif world.options.museumsanity != Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, world, museum_prefix)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, world: PlayerMultiWorldAdapter, museum_prefix: str):
    all_donations = sorted(locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 5 // number_donations
            rule = logic.museum.can_find_museum_item(all_museum_items_by_name[donation_name]) & logic.received("Traveling Merchant Metal Detector",
                                                                                                               required_detectors)
            world.set_location_rule(museum_location.name, rule)
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, world: PlayerMultiWorldAdapter, museum_milestone, museum_prefix: str):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    metal_detector = "Traveling Merchant Metal Detector"
    rule = None
    if milestone_name.endswith(donations_suffix):
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items, logic.museum.can_find_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_museum_minerals, logic.museum.can_find_museum_minerals)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_museum_artifacts, logic.museum.can_find_museum_artifacts)
    elif milestone_name == "Dwarf Scrolls":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in dwarf_scrolls)) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Front":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_front)) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Middle":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_middle)) & logic.received(metal_detector, 4)
    elif milestone_name == "Skeleton Back":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_back)) & logic.received(metal_detector, 4)
    elif milestone_name == "Ancient Seed":
        rule = logic.museum.can_find_museum_item(Artifact.ancient_seed) & logic.received(metal_detector, 4)
    if rule is None:
        return
    world.set_location_rule(museum_milestone.name, rule)


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = "Traveling Merchant Metal Detector"
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 5 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.backpack_progression != BackpackProgression.option_vanilla:
        world.set_location_rule("Large Pack", logic.money.can_spend(2000))
        world.set_location_rule("Deluxe Pack", (logic.money.can_spend(10000) & logic.received("Progressive Backpack")))
        if ModNames.big_backpack in world.options.mods:
            world.set_location_rule("Premium Pack", (logic.money.can_spend(150000) &
                                                     logic.received("Progressive Backpack", 2)))


def set_festival_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    festival_locations = []
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            world.set_location_rule(festival.name, logic.registry.festival_rules[festival.name])


monster_eradication_prefix = "Monster Eradication: "


def set_monstersanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    monstersanity_option = world.options.monstersanity
    if monstersanity_option == Monstersanity.option_none:
        return

    if monstersanity_option == Monstersanity.option_one_per_monster or monstersanity_option == Monstersanity.option_split_goals:
        set_monstersanity_monster_rules(all_location_names, logic, world)
        return

    if monstersanity_option == Monstersanity.option_progressive_goals:
        set_monstersanity_progressive_category_rules(all_location_names, logic, world)
        return

    set_monstersanity_category_rules(all_location_names, logic, world)


def set_monstersanity_monster_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    for monster_name in all_monsters_by_name:
        location_name = f"{monster_eradication_prefix}{monster_name}"
        if location_name not in all_location_names:
            continue
        if world.options.monstersanity == Monstersanity.option_split_goals:
            rule = logic.monster.can_kill_many(all_monsters_by_name[monster_name])
        else:
            rule = logic.monster.can_kill(all_monsters_by_name[monster_name])
        world.set_location_rule(location_name, rule)


def set_monstersanity_progressive_category_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    for monster_category in all_monsters_by_category:
        set_monstersanity_progressive_single_category_rules(all_location_names, logic, world, monster_category)


def set_monstersanity_progressive_single_category_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter,
                                                        monster_category: str):
    location_names = [name for name in all_location_names if name.startswith(monster_eradication_prefix) and name.endswith(monster_category)]
    if not location_names:
        return
    location_names = sorted(location_names, key=lambda name: get_monster_eradication_number(name, monster_category))
    for i in range(5):
        location_name = location_names[i]
        set_monstersanity_progressive_category_rule(all_location_names, logic, world, monster_category, location_name, i)


def set_monstersanity_progressive_category_rule(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter,
                                                monster_category: str, location_name: str, goal_index):
    if location_name not in all_location_names:
        return
    if goal_index < 3:
        rule = logic.monster.can_kill_any(all_monsters_by_category[monster_category], goal_index + 1)
    else:
        rule = logic.monster.can_kill_all(all_monsters_by_category[monster_category], goal_index * 2)
    world.set_location_rule(location_name, rule)


def get_monster_eradication_number(location_name, monster_category) -> int:
    number = location_name[len(monster_eradication_prefix):-len(monster_category)]
    number = number.strip()
    if number.isdigit():
        return int(number)
    return 1000


def set_monstersanity_category_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    for monster_category in all_monsters_by_category:
        location_name = f"{monster_eradication_prefix}{monster_category}"
        if location_name not in all_location_names:
            continue
        if world.options.monstersanity == Monstersanity.option_one_per_category:
            rule = logic.monster.can_kill_any(all_monsters_by_category[monster_category])
        else:
            rule = logic.monster.can_kill_all(all_monsters_by_category[monster_category], 4)
        world.set_location_rule(location_name, rule)


def set_shipsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    shipsanity_option = world.options.shipsanity
    if shipsanity_option == Shipsanity.option_none:
        return

    shipsanity_prefix = "Shipsanity: "
    for location in locations.locations_by_tag[LocationTags.SHIPSANITY]:
        if location.name not in all_location_names:
            continue
        item_to_ship = location.name[len(shipsanity_prefix):]
        world.set_location_rule(location.name, logic.shipping.can_ship(item_to_ship))


def set_cooksanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    cooksanity_option = world.options.cooksanity
    if cooksanity_option == Cooksanity.option_none:
        return

    cooksanity_prefix = "Cook "
    for location in locations.locations_by_tag[LocationTags.COOKSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[len(cooksanity_prefix):]
        recipe = all_cooking_recipes_by_name[recipe_name]
        cook_rule = logic.cooking.can_cook(recipe)
        world.set_location_rule(location.name, cook_rule)


def set_chefsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    chefsanity_option = world.options.chefsanity
    if chefsanity_option == Chefsanity.option_none:
        return

    chefsanity_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CHEFSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[:-len(chefsanity_suffix)]
        recipe = all_cooking_recipes_by_name[recipe_name]
        learn_rule = logic.cooking.can_learn_recipe(recipe.source)
        world.set_location_rule(location.name, learn_rule)


def set_craftsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    craftsanity_option = world.options.craftsanity
    if craftsanity_option == Craftsanity.option_none:
        return

    craft_prefix = "Craft "
    craft_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CRAFTSANITY]:
        if location.name not in all_location_names:
            continue
        if location.name.endswith(craft_suffix):
            recipe_name = location.name[:-len(craft_suffix)]
            recipe = all_crafting_recipes_by_name[recipe_name]
            craft_rule = logic.crafting.can_learn_recipe(recipe)
        else:
            recipe_name = location.name[len(craft_prefix):]
            recipe = all_crafting_recipes_by_name[recipe_name]
            craft_rule = logic.crafting.can_craft(recipe)
        world.set_location_rule(location.name, craft_rule)


def set_traveling_merchant_day_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        entrance_name = f"Buy from Traveling Merchant {day}"
        world.set_entrance_rule(entrance_name, logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    world.add_entrance_rule(Entrance.play_junimo_kart, logic.received(Wallet.skull_key))
    if world.options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
        return

    world.add_entrance_rule(Entrance.play_junimo_kart, logic.has("Junimo Kart Small Buff"))
    world.add_entrance_rule(Entrance.reach_junimo_kart_2, logic.has("Junimo Kart Medium Buff"))
    world.add_entrance_rule(Entrance.reach_junimo_kart_3, logic.has("Junimo Kart Big Buff"))
    world.add_location_rule("Junimo Kart: Sunset Speedway (Victory)", logic.has("Junimo Kart Max Buff"))
    world.add_entrance_rule(Entrance.play_journey_of_the_prairie_king, logic.has("JotPK Small Buff"))
    world.add_entrance_rule(Entrance.reach_jotpk_world_2, logic.has("JotPK Medium Buff"))
    world.add_entrance_rule(Entrance.reach_jotpk_world_3, logic.has("JotPK Big Buff"))
    world.add_location_rule("Journey of the Prairie King Victory", logic.has("JotPK Max Buff"))


def set_friendsanity_rules(all_location_names: List[str], logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.friendsanity == Friendsanity.option_none:
        return
    world.add_location_rule("Spouse Stardrop", logic.relationship.has_hearts(Generic.bachelor, 13))
    world.add_location_rule("Have a Baby", logic.relationship.can_reproduce(1))
    world.add_location_rule("Have Another Baby", logic.relationship.can_reproduce(2))

    friend_prefix = "Friendsanity: "
    friend_suffix = " <3"
    for friend_location in locations.locations_by_tag[LocationTags.FRIENDSANITY]:
        if not friend_location.name in all_location_names:
            continue
        friend_location_without_prefix = friend_location.name[len(friend_prefix):]
        friend_location_trimmed = friend_location_without_prefix[:friend_location_without_prefix.index(friend_suffix)]
        split_index = friend_location_trimmed.rindex(" ")
        friend_name = friend_location_trimmed[:split_index]
        num_hearts = int(friend_location_trimmed[split_index + 1:])
        world.set_location_rule(friend_location.name, logic.relationship.can_earn_relationship(friend_name, num_hearts))


def set_deepwoods_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.has_mod(ModNames.deepwoods):
        world.add_location_rule("Breaking Up Deep Woods Gingerbread House", logic.tool.has_tool(Tool.axe, "Gold"))
        world.add_location_rule("Chop Down a Deep Woods Iridium Tree", logic.tool.has_tool(Tool.axe, "Iridium"))
        world.set_entrance_rule(DeepWoodsEntrance.use_woods_obelisk, logic.received("Woods Obelisk"))
        for depth in range(10, 100 + 10, 10):
            world.set_entrance_rule(move_to_woods_depth(depth), logic.mod.deepwoods.can_chop_to_depth(depth))
        world.add_location_rule("The Sword in the Stone", logic.mod.deepwoods.can_pull_sword() & logic.mod.deepwoods.can_chop_to_depth(100))


def set_magic_spell_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if not world.has_mod(ModNames.magic):
        return

    world.set_entrance_rule(MagicEntrance.store_to_altar, (logic.relationship.has_hearts(NPC.wizard, 3) &
                                                           logic.region.can_reach(Region.wizard_tower)))
    world.add_location_rule("Analyze: Clear Debris", (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")))
    world.add_location_rule("Analyze: Till", logic.tool.has_tool("Hoe", "Basic"))
    world.add_location_rule("Analyze: Water", logic.tool.has_tool("Watering Can", "Basic"))
    world.add_location_rule("Analyze All Toil School Locations", (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
                                                                  & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic"))))
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    world.add_location_rule("Analyze: Evac", logic.ability.can_mine_perfectly())
    world.add_location_rule("Analyze: Haste", logic.has("Coffee"))
    world.add_location_rule("Analyze: Heal", logic.has("Life Elixir"))
    world.add_location_rule("Analyze All Life School Locations", (logic.has("Coffee") & logic.has("Life Elixir")
                                                                  & logic.ability.can_mine_perfectly()))
    world.add_location_rule("Analyze: Descend", logic.region.can_reach(Region.mines))
    world.add_location_rule("Analyze: Fireball", logic.has("Fire Quartz"))
    world.add_location_rule("Analyze: Frostbolt", logic.region.can_reach(Region.mines_floor_60) & logic.skill.can_fish(difficulty=85))
    world.add_location_rule("Analyze All Elemental School Locations",
                            logic.has("Fire Quartz") & logic.region.can_reach(Region.mines_floor_60) & logic.skill.can_fish(difficulty=85))
    # MultiWorldRules.add_rule(multiworld.get_location("Analyze: Lantern", player),)
    world.add_location_rule("Analyze: Tendrils", logic.region.can_reach(Region.farm))
    world.add_location_rule("Analyze: Shockwave", logic.has("Earth Crystal"))
    world.add_location_rule("Analyze All Nature School Locations", (logic.has("Earth Crystal") & logic.region.can_reach("Farm"))),
    world.add_location_rule("Analyze: Meteor", (logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12))),
    world.add_location_rule("Analyze: Lucksteal", logic.region.can_reach(Region.witch_hut))
    world.add_location_rule("Analyze: Bloodmana", logic.region.can_reach(Region.mines_floor_100))
    world.add_location_rule("Analyze All Eldritch School Locations", (logic.region.can_reach(Region.witch_hut) &
                                                                      logic.region.can_reach(Region.mines_floor_100) &
                                                                      logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)))
    world.add_location_rule("Analyze Every Magic School Location", (logic.tool.has_tool("Watering Can", "Basic") & logic.tool.has_tool("Hoe", "Basic")
                                                                    & (logic.tool.has_tool("Axe", "Basic") | logic.tool.has_tool("Pickaxe", "Basic")) &
                                                                    logic.has("Coffee") & logic.has("Life Elixir")
                                                                    & logic.ability.can_mine_perfectly() & logic.has("Earth Crystal") &
                                                                    logic.has("Fire Quartz") & logic.skill.can_fish(difficulty=85) &
                                                                    logic.region.can_reach(Region.witch_hut) &
                                                                    logic.region.can_reach(Region.mines_floor_100) &
                                                                    logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)))


def set_sve_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if not world.has_mod(ModNames.sve):
        return

    world.set_entrance_rule(SVEEntrance.forest_to_lost_woods, logic.bundle.can_complete_community_center)
    world.set_entrance_rule(SVEEntrance.enter_summit, logic.mod.sve.has_iridium_bomb())
    world.set_entrance_rule(SVEEntrance.backwoods_to_grove, logic.mod.sve.has_any_rune())
    world.set_entrance_rule(SVEEntrance.badlands_to_cave, logic.has("Aegis Elixir"))
    world.set_entrance_rule(SVEEntrance.forest_west_to_spring, logic.quest.can_complete_quest(Quest.magic_ink))
    world.set_entrance_rule(SVEEntrance.secret_woods_to_west, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    world.set_entrance_rule(SVEEntrance.grandpa_shed_to_interior, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    world.set_entrance_rule(SVEEntrance.aurora_warp_to_aurora, logic.received("Nexus: Aurora Vineyard Runes"))
    world.set_entrance_rule(SVEEntrance.farm_warp_to_farm, logic.received("Nexus: Farm and Wizard Runes"))
    world.set_entrance_rule(SVEEntrance.guild_warp_to_guild, logic.received("Nexus: Adventurer's Guild Runes"))
    world.set_entrance_rule(SVEEntrance.junimo_warp_to_junimo, logic.received("Nexus: Junimo and Outpost Runes"))
    world.set_entrance_rule(SVEEntrance.spring_warp_to_spring, logic.received("Nexus: Sprite Spring Runes"))
    world.set_entrance_rule(SVEEntrance.outpost_warp_to_outpost, logic.received("Nexus: Junimo and Outpost Runes"))
    world.set_entrance_rule(SVEEntrance.wizard_warp_to_wizard, logic.received("Nexus: Farm and Wizard Runes"))
    world.set_entrance_rule(SVEEntrance.use_purple_junimo, logic.relationship.has_hearts(ModNPC.apples, 10))
    world.set_entrance_rule(SVEEntrance.grandpa_interior_to_upstairs, logic.quest.can_complete_quest(ModQuest.GrandpasShed))
    world.set_entrance_rule(SVEEntrance.use_bear_shop, (logic.quest.can_complete_quest(Quest.strange_note) & logic.tool.has_tool(Tool.axe, ToolMaterial.basic) &
                                                        logic.tool.has_tool(Tool.pickaxe, ToolMaterial.basic)))
    world.set_entrance_rule(SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    logic.mod.sve.initialize_rules()
    for location in logic.registry.sve_location_rules:
        world.set_location_rule(location, logic.registry.sve_location_rules[location])
    set_sve_ginger_island_rules(logic, world)


def set_sve_ginger_island_rules(logic: StardewLogic, world: PlayerMultiWorldAdapter):
    if world.options.exclude_ginger_island == ExcludeGingerIsland.option_true:
        return

    world.set_entrance_rule(SVEEntrance.summit_to_highlands, logic.received("Marlon's Boat Paddle"))
    world.set_entrance_rule(SVEEntrance.wizard_to_fable_reef, logic.received("Fable Reef Portal"))
    world.set_location_rule(SVELocation.diamond_wand, logic.quest.can_complete_quest(ModQuest.MonsterCrops) & logic.region.can_reach(SVERegion.lances_house))
    world.set_entrance_rule(SVEEntrance.highlands_to_cave,
                            logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron) & logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
