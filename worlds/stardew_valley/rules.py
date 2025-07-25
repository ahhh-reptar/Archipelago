import itertools
import logging
from typing import List, Dict, Set

from BaseClasses import MultiWorld, CollectionState
from worlds.generic.Rules import set_rule
from . import locations
from .bundles.bundle_room import BundleRoom
from .content import StardewContent
from .content.feature import friendsanity
from .content.vanilla.ginger_island import ginger_island_content_pack
from .content.vanilla.qi_board import qi_board_content_pack
from .data.craftable_data import all_crafting_recipes_by_name
from .data.game_item import ItemTag
from .data.harvest import HarvestCropSource, HarvestFruitTreeSource
from .data.hats_data import wear_prefix, hat_clarifier
from .data.museum_data import all_museum_items, dwarf_scrolls, skeleton_front, skeleton_middle, skeleton_back, \
    all_museum_items_by_name, all_museum_minerals, \
    all_museum_artifacts, Artifact
from .data.recipe_data import all_cooking_recipes_by_name
from .data.secret_note_data import gift_requirements, SecretNote
from .locations import LocationTags
from .logic.logic import StardewLogic
from .logic.time_logic import MAX_MONTHS
from .logic.tool_logic import tool_upgrade_prices
from .mods.mod_data import ModNames
from .options import SpecialOrderLocations, Museumsanity, BackpackProgression, Shipsanity, \
    Monstersanity, Chefsanity, Craftsanity, ArcadeMachineLocations, Cooksanity, StardewValleyOptions, Walnutsanity
from .options.options import FarmType, Moviesanity, Eatsanity, Friendsanity, ExcludeGingerIsland, \
    IncludeEndgameLocations, ToolProgression
from .stardew_rule import And, StardewRule, true_
from .stardew_rule.indirect_connection import look_for_indirect_connection
from .stardew_rule.rule_explain import explain
from .strings.animal_product_names import AnimalProduct
from .strings.ap_names.ap_option_names import WalnutsanityOptionName, SecretsanityOptionName
from .strings.ap_names.community_upgrade_names import CommunityUpgrade
from .strings.ap_names.mods.mod_items import SVEQuestItem, SVERunes
from .strings.ap_names.transport_names import Transportation
from .strings.artisan_good_names import ArtisanGood
from .strings.backpack_tiers import Backpack
from .strings.building_names import Building, WizardBuilding
from .strings.bundle_names import CCRoom
from .strings.calendar_names import Weekday
from .strings.craftable_names import Bomb, Furniture, Consumable, Craftable
from .strings.crop_names import Fruit, Vegetable
from .strings.currency_names import Currency
from .strings.entrance_names import dig_to_mines_floor, dig_to_skull_floor, Entrance, move_to_woods_depth, \
    DeepWoodsEntrance, AlecEntrance, \
    SVEEntrance, LaceyEntrance, BoardingHouseEntrance, LogicEntrance
from .strings.fish_names import Fish
from .strings.food_names import Meal
from .strings.forageable_names import Forageable
from .strings.generic_names import Generic
from .strings.geode_names import Geode
from .strings.gift_names import Gift
from .strings.machine_names import Machine
from .strings.material_names import Material
from .strings.metal_names import Artifact as ArtifactName, MetalBar, Mineral
from .strings.monster_names import Monster
from .strings.performance_names import Performance
from .strings.quest_names import Quest
from .strings.region_names import Region, LogicRegion
from .strings.season_names import Season
from .strings.skill_names import Skill
from .strings.special_item_names import SpecialItem
from .strings.tool_names import Tool, ToolMaterial, FishingRod
from .strings.tv_channel_names import Channel
from .strings.villager_names import NPC, ModNPC
from .strings.wallet_item_names import Wallet

logger = logging.getLogger(__name__)


def set_rules(world):
    multiworld = world.multiworld
    world_options = world.options
    world_content = world.content
    player = world.player
    logic = world.logic
    bundle_rooms: List[BundleRoom] = world.modified_bundles
    trash_bear_requests: Dict[str, List[str]] = world.trash_bear_requests

    all_location_names = set(location.name for location in multiworld.get_locations(player))

    set_entrance_rules(logic, multiworld, player, world_options, world_content)
    set_ginger_island_rules(logic, multiworld, player, world_options, world_content)

    set_tool_rules(logic, multiworld, player, world_content)
    set_skills_rules(logic, multiworld, player, world_content)
    set_bundle_rules(bundle_rooms, logic, multiworld, player, world_options)
    set_building_rules(logic, multiworld, player, world_content)
    set_cropsanity_rules(logic, multiworld, player, world_content)
    set_story_quests_rules(all_location_names, logic, multiworld, player, world_options)
    set_special_order_rules(all_location_names, logic, multiworld, player, world_options, world_content)
    set_help_wanted_quests_rules(logic, multiworld, player, world_options)
    set_fishsanity_rules(all_location_names, logic, multiworld, player)
    set_museumsanity_rules(all_location_names, logic, multiworld, player, world_options)

    set_friendsanity_rules(logic, multiworld, player, world_content)
    set_backpack_rules(logic, multiworld, player, world_options, world_content)
    set_festival_rules(all_location_names, logic, multiworld, player)
    set_monstersanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_shipsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_cooksanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_chefsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_craftsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_booksanity_rules(logic, multiworld, player, world_content)
    set_isolated_locations_rules(logic, multiworld, player, trash_bear_requests)
    set_traveling_merchant_day_rules(logic, multiworld, player)
    set_arcade_machine_rules(logic, multiworld, player, world_options)
    set_movie_rules(logic, multiworld, player, world_options, world_content)
    set_secrets_rules(logic, multiworld, player, world_options, world_content)
    set_hatsanity_rules(all_location_names, logic, multiworld, player, world_options, world_content)
    set_eatsanity_rules(all_location_names, logic, multiworld, player, world_options)
    set_endgame_locations_rules(logic, multiworld, player, world_options)

    set_deepwoods_rules(logic, multiworld, player, world_content)
    set_magic_spell_rules(logic, multiworld, player, world_content)
    set_sve_rules(logic, multiworld, player, world_content)


def set_isolated_locations_rules(logic: StardewLogic, multiworld, player, trash_bear_requests: Dict[str, List[str]]):
    set_location_rule(multiworld, player, "Beach Bridge Repair", logic.grind.can_grind_item(300, "Wood"))
    set_location_rule(multiworld, player, "Grim Reaper statue", logic.combat.can_fight_at_level(Performance.basic) & logic.tool.has_tool(Tool.pickaxe))
    set_location_rule(multiworld, player, "Galaxy Sword Shrine", logic.has("Prismatic Shard"))
    set_location_rule(multiworld, player, "Krobus Stardrop", logic.money.can_spend(20000))
    set_location_rule(multiworld, player, "Demetrius's Breakthrough", logic.money.can_have_earned_total(25000))
    for request_type in trash_bear_requests:
        location = f"Trash Bear {request_type}"
        items = trash_bear_requests[request_type]
        set_location_rule(multiworld, player, location, logic.bundle.can_feed_trash_bear(*items))


def set_tool_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    tool_progression = content.features.tool_progression
    if not tool_progression.is_progressive:
        return

    set_location_rule(multiworld, player, "Purchase Fiberglass Rod", (logic.skill.has_level(Skill.fishing, 2) & logic.money.can_spend(1800)))
    set_location_rule(multiworld, player, "Purchase Iridium Rod", (logic.skill.has_level(Skill.fishing, 6) & logic.money.can_spend(7500)))

    set_location_rule(multiworld, player, "Copper Pan Cutscene", logic.received("Glittering Boulder Removed"))

    # Pan has no basic tier, so it is removed from materials.
    pan_materials = ToolMaterial.materials[1:]
    for previous, material in itertools.product(pan_materials[:-1], pan_materials[1:]):
        location_name = tool_progression.to_upgrade_location_name(Tool.pan, material)
        tool_upgrade_location = multiworld.get_location(location_name, player)
        # You need to receive the previous tool to be able to upgrade it.
        set_rule(tool_upgrade_location, logic.tool.has_pan(previous))

    materials = ToolMaterial.materials
    tool = [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.trash_can]
    for (previous, material), tool in itertools.product(zip(materials[:-1], materials[1:]), tool):
        location_name = tool_progression.to_upgrade_location_name(tool, material)
        tool_upgrade_location = multiworld.get_location(location_name, player)
        # You need to receive the previous tool to be able to upgrade it.
        set_rule(tool_upgrade_location, logic.tool.has_tool(tool, previous))


def set_building_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    building_progression = content.features.building_progression
    if not building_progression.is_progressive:
        return

    for building in content.farm_buildings.values():
        if building.name in building_progression.starting_buildings:
            continue

        location_name = building_progression.to_location_name(building.name)

        set_rule(multiworld.get_location(location_name, player),
                 logic.building.can_build(building.name))


def set_bundle_rules(bundle_rooms: List[BundleRoom], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    for bundle_room in bundle_rooms:
        room_rules = []
        for bundle in bundle_room.bundles:
            location = multiworld.get_location(bundle.name, player)
            bundle_rules = logic.bundle.can_complete_bundle(bundle)
            if bundle_room.name == CCRoom.raccoon_requests:
                num = int(bundle.name[-1])
                extra_raccoons = 1 if world_options.quest_locations.has_story_quests() else 0
                extra_raccoons = extra_raccoons + num
                bundle_rules = logic.received(CommunityUpgrade.raccoon, extra_raccoons) & bundle_rules
                if num > 1:
                    previous_bundle_name = f"Raccoon Request {num - 1}"
                    bundle_rules = bundle_rules & logic.region.can_reach_location(previous_bundle_name)
            room_rules.append(bundle_rules)
            set_rule(location, bundle_rules)
        if bundle_room.name == CCRoom.abandoned_joja_mart or bundle_room.name == CCRoom.raccoon_requests:
            continue
        room_location = f"Complete {bundle_room.name}"
        set_location_rule(multiworld, player, room_location, And(*room_rules))


def set_skills_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    skill_progression = content.features.skill_progression
    if not skill_progression.is_progressive:
        return

    for skill in content.skills.values():
        for level, level_name in skill_progression.get_randomized_level_names_by_level(skill):
            rule = logic.skill.can_earn_level(skill.name, level)
            location = multiworld.get_location(level_name, player)
            set_rule(location, rule)

        if skill_progression.is_mastery_randomized(skill):
            rule = logic.skill.can_earn_mastery(skill.name)
            location = multiworld.get_location(skill.mastery_name, player)
            set_rule(location, rule)


def set_entrance_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions, content: StardewContent):
    set_mines_floor_entrance_rules(logic, multiworld, player)
    set_skull_cavern_floor_entrance_rules(logic, multiworld, player)
    set_blacksmith_entrance_rules(logic, multiworld, player)
    set_skill_entrance_rules(logic, multiworld, player, content)
    set_traveling_merchant_day_rules(logic, multiworld, player)
    set_dangerous_mine_rules(logic, multiworld, player, content)

    set_entrance_rule(multiworld, player, Entrance.enter_tide_pools, logic.received("Beach Bridge") | logic.mod.magic.can_blink())
    set_entrance_rule(multiworld, player, Entrance.mountain_to_outside_adventure_guild, logic.received("Landslide Removed"))
    set_entrance_rule(multiworld, player, Entrance.enter_quarry,
                      (logic.received("Bridge Repair") | logic.mod.magic.can_blink()) & logic.tool.has_tool(Tool.pickaxe))
    set_entrance_rule(multiworld, player, Entrance.enter_secret_woods, logic.tool.has_tool(Tool.axe, ToolMaterial.iron) | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.town_to_community_center, logic.received("Community Center Key"))
    set_entrance_rule(multiworld, player, Entrance.forest_to_wizard_tower, logic.received("Wizard Invitation"))
    set_entrance_rule(multiworld, player, Entrance.forest_to_sewer, logic.wallet.has_rusty_key())
    set_entrance_rule(multiworld, player, Entrance.town_to_sewer, logic.wallet.has_rusty_key())
    # The money requirement is just in case Joja got replaced by a theater, you need to buy a ticket.
    # We do not put directly a ticket requirement, because we don't want to place an indirect theater requirement only
    # for the safeguard "in case you get a theater"
    set_entrance_rule(multiworld, player, Entrance.town_to_jojamart, logic.money.can_spend(1000))
    set_entrance_rule(multiworld, player, Entrance.enter_abandoned_jojamart, logic.has_abandoned_jojamart())
    movie_theater_rule = logic.has_movie_theater()
    set_entrance_rule(multiworld, player, Entrance.purchase_movie_ticket, movie_theater_rule)
    set_entrance_rule(multiworld, player, Entrance.enter_movie_theater, movie_theater_rule & logic.has(Gift.movie_ticket))
    set_entrance_rule(multiworld, player, Entrance.take_bus_to_desert, logic.received(Transportation.bus_repair) & logic.money.can_spend(500))
    set_entrance_rule(multiworld, player, Entrance.enter_skull_cavern, logic.received(Wallet.skull_key))
    set_entrance_rule(multiworld, player, LogicEntrance.talk_to_mines_dwarf,
                      logic.wallet.can_speak_dwarf() & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, LogicEntrance.buy_from_traveling_merchant, logic.traveling_merchant.has_days())
    set_entrance_rule(multiworld, player, LogicEntrance.buy_from_raccoon, logic.quest.has_raccoon_shop())
    set_entrance_rule(multiworld, player, LogicEntrance.fish_in_waterfall,
                      logic.skill.has_level(Skill.fishing, 5) & logic.tool.has_fishing_rod(FishingRod.bamboo))

    set_farm_buildings_entrance_rules(logic, multiworld, player)

    set_entrance_rule(multiworld, player, Entrance.mountain_to_railroad, logic.received("Railroad Boulder Removed"))
    set_entrance_rule(multiworld, player, Entrance.enter_witch_warp_cave, logic.quest.has_dark_talisman() | (logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_witch_hut, (logic.quest.can_complete_quest(Quest.goblin_problem) | logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.enter_mutant_bug_lair,
                      (logic.wallet.has_rusty_key() & logic.region.can_reach(Region.railroad) & logic.relationship.can_meet(
                          NPC.krobus)) | logic.mod.magic.can_blink())
    set_entrance_rule(multiworld, player, Entrance.enter_casino, logic.quest.has_club_card())

    set_bedroom_entrance_rules(logic, multiworld, player, content)
    set_festival_entrance_rules(logic, multiworld, player)
    set_island_entrance_rule(multiworld, player, LogicEntrance.island_cooking, logic.cooking.can_cook_in_kitchen, content)
    set_entrance_rule(multiworld, player, LogicEntrance.farmhouse_cooking, logic.cooking.can_cook_in_kitchen)
    set_entrance_rule(multiworld, player, LogicEntrance.shipping, logic.shipping.can_use_shipping_bin)
    set_entrance_rule(multiworld, player, LogicEntrance.find_secret_notes,
                      logic.quest.has_magnifying_glass() & (logic.ability.can_chop_trees() | logic.mine.can_mine_in_the_mines_floor_1_40()))
    set_entrance_rule(multiworld, player, LogicEntrance.watch_queen_of_sauce, logic.action.can_watch(Channel.queen_of_sauce))
    set_entrance_rule(multiworld, player, Entrance.forest_to_mastery_cave, logic.skill.can_enter_mastery_cave)
    set_entrance_rule(multiworld, player, LogicEntrance.buy_experience_books, logic.time.has_lived_months(2))
    set_entrance_rule(multiworld, player, LogicEntrance.buy_year1_books, logic.time.has_year_two)
    set_entrance_rule(multiworld, player, LogicEntrance.buy_year3_books, logic.time.has_year_three)
    set_entrance_rule(multiworld, player, Entrance.adventurer_guild_to_bedroom, logic.monster.can_kill_max(Generic.any))
    if world_options.include_endgame_locations == IncludeEndgameLocations.option_true:
        set_entrance_rule(multiworld, player, LogicEntrance.purchase_wizard_blueprints, logic.quest.has_magic_ink())
    set_entrance_rule(multiworld, player, LogicEntrance.search_garbage_cans, logic.time.has_lived_months(MAX_MONTHS/2))

    set_entrance_rule(multiworld, player, Entrance.forest_beach_shortcut, logic.received("Forest To Beach Shortcut"))
    set_entrance_rule(multiworld, player, Entrance.mountain_jojamart_shortcut, logic.received("Mountain Shortcuts"))
    set_entrance_rule(multiworld, player, Entrance.mountain_town_shortcut, logic.received("Mountain Shortcuts"))
    set_entrance_rule(multiworld, player, Entrance.town_tidepools_shortcut, logic.received("Town To Tide Pools Shortcut"))
    set_entrance_rule(multiworld, player, Entrance.tunnel_backwoods_shortcut, logic.received("Tunnel To Backwoods Shortcut"))
    set_entrance_rule(multiworld, player, Entrance.mountain_lake_to_outside_adventure_guild_shortcut, logic.received("Mountain Shortcuts"))

    set_entrance_rule(multiworld, player, Entrance.feed_trash_bear, logic.received("Trash Bear Arrival"))
    set_entrance_rule(multiworld, player, Entrance.enter_shorts_maze, logic.has(Craftable.staircase))


def set_dangerous_mine_rules(logic, multiworld, player, content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    dangerous_mine_rule = logic.mine.has_mine_elevator_to_floor(120) & logic.region.can_reach(Region.qi_walnut_room)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_20, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_60, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.dig_to_dangerous_mines_100, dangerous_mine_rule)
    set_entrance_rule(multiworld, player, Entrance.enter_dangerous_skull_cavern,
                      (logic.received(Wallet.skull_key) & logic.region.can_reach(Region.qi_walnut_room)))


def set_farm_buildings_entrance_rules(logic, multiworld, player):
    set_entrance_rule(multiworld, player, Entrance.downstairs_to_cellar, logic.building.has_building(Building.cellar))
    set_entrance_rule(multiworld, player, Entrance.use_desert_obelisk, logic.can_use_obelisk(Transportation.desert_obelisk))
    set_entrance_rule(multiworld, player, Entrance.enter_greenhouse, logic.received("Greenhouse"))
    set_entrance_rule(multiworld, player, Entrance.enter_coop, logic.building.has_building(Building.coop))
    set_entrance_rule(multiworld, player, Entrance.enter_barn, logic.building.has_building(Building.barn))
    set_entrance_rule(multiworld, player, Entrance.enter_shed, logic.building.has_building(Building.shed))
    set_entrance_rule(multiworld, player, Entrance.enter_slime_hutch, logic.building.has_building(Building.slime_hutch))


def set_bedroom_entrance_rules(logic, multiworld, player, content: StardewContent):
    set_entrance_rule(multiworld, player, Entrance.enter_harvey_room, logic.relationship.has_hearts(NPC.harvey, 2))
    set_entrance_rule(multiworld, player, Entrance.mountain_to_maru_room, logic.relationship.has_hearts(NPC.maru, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_sebastian_room, (logic.relationship.has_hearts(NPC.sebastian, 2) | logic.mod.magic.can_blink()))
    set_entrance_rule(multiworld, player, Entrance.forest_to_leah_cottage, logic.relationship.has_hearts(NPC.leah, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_elliott_house, logic.relationship.has_hearts(NPC.elliott, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_sunroom, logic.relationship.has_hearts(NPC.caroline, 2))
    set_entrance_rule(multiworld, player, Entrance.enter_wizard_basement, logic.relationship.has_hearts(NPC.wizard, 4))
    set_entrance_rule(multiworld, player, Entrance.enter_lewis_bedroom, logic.relationship.has_hearts(NPC.lewis, 4))
    if content.is_enabled(ModNames.alec):
        set_entrance_rule(multiworld, player, AlecEntrance.petshop_to_bedroom, (logic.relationship.has_hearts(ModNPC.alec, 2) | logic.mod.magic.can_blink()))
    if content.is_enabled(ModNames.lacey):
        set_entrance_rule(multiworld, player, LaceyEntrance.forest_to_hat_house, logic.relationship.has_hearts(ModNPC.lacey, 2))


def set_mines_floor_entrance_rules(logic, multiworld, player):
    for floor in range(5, 120 + 5, 5):
        rule = logic.mine.has_mine_elevator_to_floor(floor - 10)
        if floor == 5 or floor == 45 or floor == 85:
            rule = rule & logic.mine.can_progress_in_the_mines_from_floor(floor)
        set_entrance_rule(multiworld, player, dig_to_mines_floor(floor), rule)


def set_skull_cavern_floor_entrance_rules(logic, multiworld, player):
    for floor in range(25, 200 + 25, 25):
        rule = logic.mod.elevator.has_skull_cavern_elevator_to_floor(floor - 25)
        if floor == 25 or floor == 75 or floor == 125:
            rule = rule & logic.mine.can_progress_in_the_skull_cavern_from_floor(floor)
        set_entrance_rule(multiworld, player, dig_to_skull_floor(floor), rule)


def set_skill_entrance_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    set_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops, logic.farming.has_farming_tools & logic.season.has_spring)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops, logic.farming.has_farming_tools & logic.season.has_summer)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops, logic.farming.has_farming_tools & logic.season.has_fall)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_winter_crops, logic.farming.has_farming_tools & logic.season.has_winter)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_winter_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_indoor_crops_in_greenhouse, logic.farming.has_farming_tools)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_spring_crops_on_island, logic.farming.has_farming_tools, content)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_summer_crops_on_island, logic.farming.has_farming_tools, content)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_fall_crops_on_island, logic.farming.has_farming_tools, content)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_winter_crops_on_island, logic.farming.has_farming_tools, content)
    set_island_entrance_rule(multiworld, player, LogicEntrance.grow_indoor_crops_on_island, logic.farming.has_farming_tools, content)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_fall_crops_in_summer, true_)
    set_entrance_rule(multiworld, player, LogicEntrance.grow_summer_fall_crops_in_fall, true_)

    set_entrance_rule(multiworld, player, LogicEntrance.fishing, logic.fishing.can_fish_anywhere())


def set_blacksmith_entrance_rules(logic, multiworld, player):
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_copper, MetalBar.copper, ToolMaterial.copper)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_iron, MetalBar.iron, ToolMaterial.iron)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_gold, MetalBar.gold, ToolMaterial.gold)
    set_blacksmith_upgrade_rule(logic, multiworld, player, LogicEntrance.blacksmith_iridium, MetalBar.iridium, ToolMaterial.iridium)


def set_blacksmith_upgrade_rule(logic, multiworld, player, entrance_name: str, item_name: str, tool_material: str):
    upgrade_rule = logic.has(item_name) & logic.money.can_spend(tool_upgrade_prices[tool_material])
    set_entrance_rule(multiworld, player, entrance_name, upgrade_rule)


def set_festival_entrance_rules(logic, multiworld, player):
    set_entrance_rule(multiworld, player, LogicEntrance.attend_egg_festival, logic.season.has(Season.spring))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_desert_festival, logic.season.has(Season.spring) & logic.received(Transportation.bus_repair))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_flower_dance, logic.season.has(Season.spring))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_luau, logic.season.has(Season.summer))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_trout_derby, logic.season.has(Season.summer))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_moonlight_jellies, logic.season.has(Season.summer))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_fair, logic.season.has(Season.fall))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_spirit_eve, logic.season.has(Season.fall))

    set_entrance_rule(multiworld, player, LogicEntrance.attend_festival_of_ice, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_squidfest, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_night_market, logic.season.has(Season.winter))
    set_entrance_rule(multiworld, player, LogicEntrance.attend_winter_star, logic.season.has(Season.winter))


def set_ginger_island_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions, content: StardewContent):
    set_island_entrances_rules(logic, multiworld, player, content)
    if not content.is_enabled(ginger_island_content_pack):
        return

    set_boat_repair_rules(logic, multiworld, player)
    set_island_parrot_rules(logic, multiworld, player)
    set_location_rule(multiworld, player, "Open Professor Snail Cave", logic.has(Bomb.cherry_bomb))
    set_location_rule(multiworld, player, "Complete Island Field Office", logic.walnut.can_complete_field_office())
    set_walnut_rules(logic, multiworld, player, world_options)


def set_boat_repair_rules(logic: StardewLogic, multiworld, player):
    set_location_rule(multiworld, player, "Repair Boat Hull", logic.has(Material.hardwood))
    set_location_rule(multiworld, player, "Repair Boat Anchor", logic.has(MetalBar.iridium))
    set_location_rule(multiworld, player, "Repair Ticket Machine", logic.has(ArtisanGood.battery_pack))


def set_island_entrances_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    boat_repaired = logic.received(Transportation.boat_repair)
    dig_site_rule = logic.received("Dig Site Bridge")
    entrance_rules = {
        Entrance.use_island_obelisk: logic.can_use_obelisk(Transportation.island_obelisk),
        Entrance.use_farm_obelisk: logic.can_use_obelisk(Transportation.farm_obelisk),
        Entrance.fish_shop_to_boat_tunnel: boat_repaired,
        Entrance.boat_to_ginger_island: boat_repaired & logic.money.can_spend(1000),
        Entrance.island_south_to_west: logic.received("Island West Turtle"),
        Entrance.island_south_to_north: logic.received("Island North Turtle"),
        Entrance.island_west_to_islandfarmhouse: logic.received("Island Farmhouse"),
        Entrance.island_west_to_gourmand_cave: logic.received("Island Farmhouse"),
        Entrance.island_north_to_dig_site: dig_site_rule,
        Entrance.dig_site_to_professor_snail_cave: logic.received("Open Professor Snail Cave"),
        Entrance.talk_to_island_trader: logic.received("Island Trader"),
        Entrance.island_south_to_southeast: logic.received("Island Resort"),
        Entrance.use_island_resort: logic.received("Island Resort"),
        Entrance.island_west_to_qi_walnut_room: logic.received("Qi Walnut Room"),
        Entrance.island_north_to_volcano: logic.tool.can_water() | logic.received("Volcano Bridge") | logic.mod.magic.can_blink(),
        Entrance.volcano_to_secret_beach: logic.tool.can_water(3),
        Entrance.climb_to_volcano_5: logic.ability.can_mine_perfectly() & logic.tool.can_water(2),
        Entrance.talk_to_volcano_dwarf: logic.wallet.can_speak_dwarf(),
        Entrance.climb_to_volcano_10: logic.ability.can_mine_perfectly() & logic.tool.can_water(2),
        Entrance.mountain_to_leo_treehouse: logic.received("Treehouse"),
    }
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
            entrance_rules[parrot] = parrot_express_to_dig_site_rule
        else:
            entrance_rules[parrot] = parrot_express_rule

    set_many_island_entrances_rules(multiworld, player, entrance_rules, content)


def set_island_parrot_rules(logic: StardewLogic, multiworld, player):
    # Logic rules require more walnuts than in reality, to allow the player to spend them "wrong"
    has_walnut = logic.walnut.has_walnut(5)
    has_5_walnut = logic.walnut.has_walnut(15)
    has_10_walnut = logic.walnut.has_walnut(40)
    has_20_walnut = logic.walnut.has_walnut(60)
    set_location_rule(multiworld, player, "Leo's Parrot", has_walnut)
    set_location_rule(multiworld, player, "Island West Turtle", has_10_walnut & logic.received("Island North Turtle"))
    set_location_rule(multiworld, player, "Island Farmhouse", has_20_walnut)
    set_location_rule(multiworld, player, "Island Mailbox", has_5_walnut & logic.received("Island Farmhouse"))
    set_location_rule(multiworld, player, Transportation.farm_obelisk, has_20_walnut & logic.received("Island Mailbox"))
    set_location_rule(multiworld, player, "Dig Site Bridge", has_10_walnut & logic.received("Island West Turtle"))
    set_location_rule(multiworld, player, "Island Trader", has_10_walnut & logic.received("Island Farmhouse"))
    set_location_rule(multiworld, player, "Volcano Bridge",
                      has_5_walnut & logic.received("Island West Turtle") & logic.region.can_reach(Region.volcano_floor_10))
    set_location_rule(multiworld, player, "Volcano Exit Shortcut", has_5_walnut & logic.received("Island West Turtle"))
    set_location_rule(multiworld, player, "Island Resort", has_20_walnut & logic.received("Island Farmhouse"))
    set_location_rule(multiworld, player, Transportation.parrot_express, has_10_walnut)


def set_walnut_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.walnutsanity == Walnutsanity.preset_none:
        return

    set_walnut_puzzle_rules(logic, multiworld, player, world_options)
    set_walnut_bushes_rules(logic, multiworld, player, world_options)
    set_walnut_dig_spot_rules(logic, multiworld, player, world_options)
    set_walnut_repeatable_rules(logic, multiworld, player, world_options)


def set_walnut_puzzle_rules(logic: StardewLogic, multiworld, player, world_options):
    if WalnutsanityOptionName.puzzles not in world_options.walnutsanity:
        return

    set_location_rule(multiworld, player, "Walnutsanity: Open Golden Coconut", logic.has(Geode.golden_coconut))
    set_location_rule(multiworld, player, "Walnutsanity: Banana Altar", logic.has(Fruit.banana))
    set_location_rule(multiworld, player, "Walnutsanity: Leo's Tree", logic.tool.has_tool(Tool.axe))
    set_location_rule(multiworld, player, "Walnutsanity: Gem Birds Shrine",
                      logic.has_all(Mineral.amethyst, Mineral.aquamarine, Mineral.emerald, Mineral.ruby, Mineral.topaz)
                      & logic.region.can_reach_all(Region.island_north, Region.island_west, Region.island_east, Region.island_south))
    set_location_rule(multiworld, player, "Walnutsanity: Gourmand Frog Melon", logic.has(Fruit.melon) & logic.region.can_reach(Region.island_west))
    set_location_rule(multiworld, player, "Walnutsanity: Gourmand Frog Wheat",
                      logic.has(Vegetable.wheat) & logic.region.can_reach(Region.island_west) & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Melon"))
    set_location_rule(multiworld, player, "Walnutsanity: Gourmand Frog Garlic",
                      logic.has(Vegetable.garlic) & logic.region.can_reach(Region.island_west) & logic.region.can_reach_location("Walnutsanity: Gourmand Frog Wheat"))
    set_location_rule(multiworld, player, "Walnutsanity: Whack A Mole", logic.tool.has_tool(Tool.watering_can, ToolMaterial.iridium))
    set_location_rule(multiworld, player, "Walnutsanity: Complete Large Animal Collection", logic.walnut.can_complete_large_animal_collection())
    set_location_rule(multiworld, player, "Walnutsanity: Complete Snake Collection", logic.walnut.can_complete_snake_collection())
    set_location_rule(multiworld, player, "Walnutsanity: Complete Mummified Frog Collection", logic.walnut.can_complete_frog_collection())
    set_location_rule(multiworld, player, "Walnutsanity: Complete Mummified Bat Collection", logic.walnut.can_complete_bat_collection())
    set_location_rule(multiworld, player, "Walnutsanity: Purple Flowers Island Survey", logic.walnut.can_start_field_office)
    set_location_rule(multiworld, player, "Walnutsanity: Purple Starfish Island Survey", logic.walnut.can_start_field_office)
    set_location_rule(multiworld, player, "Walnutsanity: Protruding Tree Walnut", logic.combat.has_slingshot)
    set_location_rule(multiworld, player, "Walnutsanity: Starfish Tide Pool", logic.tool.has_fishing_rod())
    set_location_rule(multiworld, player, "Walnutsanity: Mermaid Song", logic.has(Furniture.flute_block))


def set_walnut_bushes_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.bushes not in world_options.walnutsanity:
        return
    # I don't think any of the bushes require something special, but that might change with ER
    return


def set_walnut_dig_spot_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.dig_spots not in world_options.walnutsanity:
        return

    for dig_spot_walnut in locations.locations_by_tag[LocationTags.WALNUTSANITY_DIG]:
        rule = logic.tool.has_tool(Tool.hoe)
        if "Journal Scrap" in dig_spot_walnut.name:
            rule = rule & logic.has(Forageable.journal_scrap)
        if "Starfish Diamond" in dig_spot_walnut.name:
            rule = rule & logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron)
        set_rule(multiworld.get_location(dig_spot_walnut.name, player), rule)


def set_walnut_repeatable_rules(logic, multiworld, player, world_options):
    if WalnutsanityOptionName.repeatables not in world_options.walnutsanity:
        return
    for i in range(1, 6):
        set_rule(multiworld.get_location(f"Walnutsanity: Fishing Walnut {i}", player), logic.tool.has_fishing_rod())
        set_rule(multiworld.get_location(f"Walnutsanity: Harvesting Walnut {i}", player), logic.skill.can_get_farming_xp)
        set_rule(multiworld.get_location(f"Walnutsanity: Mussel Node Walnut {i}", player), logic.tool.has_tool(Tool.pickaxe))
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Rocks Walnut {i}", player), logic.tool.has_tool(Tool.pickaxe))
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Monsters Walnut {i}", player), logic.combat.has_galaxy_weapon)
        set_rule(multiworld.get_location(f"Walnutsanity: Volcano Crates Walnut {i}", player), logic.combat.has_any_weapon)
    set_rule(multiworld.get_location(f"Walnutsanity: Tiger Slime Walnut", player), logic.monster.can_kill(Monster.tiger_slime))


def set_cropsanity_rules(logic: StardewLogic, multiworld, player, world_content: StardewContent):
    if not world_content.features.cropsanity.is_enabled:
        return

    for item in world_content.find_tagged_items(ItemTag.CROPSANITY):
        location = world_content.features.cropsanity.to_location_name(item.name)
        harvest_sources = (source for source in item.sources if isinstance(source, (HarvestFruitTreeSource, HarvestCropSource)))
        set_rule(multiworld.get_location(location, player), logic.source.has_access_to_any(harvest_sources))


def set_story_quests_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.quest_locations.has_no_story_quests():
        return
    for quest_location in locations.locations_by_tag[LocationTags.STORY_QUEST]:
        quest_location_name = quest_location.name
        if quest_location_name in all_location_names:
            quest_prefix = "Quest: "
            quest_name = quest_location_name[len(quest_prefix):]
            set_rule(multiworld.get_location(quest_location_name, player),
                     logic.registry.quest_rules[quest_name])


def set_special_order_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player,
                            world_options: StardewValleyOptions, content: StardewContent):
    if world_options.special_order_locations & SpecialOrderLocations.option_board:
        board_rule = logic.received("Special Order Board") & logic.time.has_lived_months(4)
        for board_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_BOARD]:
            if board_order.name in all_location_names:
                order_rule = board_rule & logic.registry.special_order_rules[board_order.name]
                set_rule(multiworld.get_location(board_order.name, player), order_rule)

    if content.is_enabled(qi_board_content_pack):
        qi_rule = logic.region.can_reach(Region.qi_walnut_room) & logic.time.has_lived_months(8)
        for qi_order in locations.locations_by_tag[LocationTags.SPECIAL_ORDER_QI]:
            if qi_order.name in all_location_names:
                order_rule = qi_rule & logic.registry.special_order_rules[qi_order.name]
                set_rule(multiworld.get_location(qi_order.name, player), order_rule)


help_wanted_prefix = "Help Wanted:"
item_delivery = "Item Delivery"
gathering = "Gathering"
fishing = "Fishing"
slay_monsters = "Slay Monsters"


def set_help_wanted_quests_rules(logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    if world_options.quest_locations.has_no_story_quests():
        return
    help_wanted_number = world_options.quest_locations.value
    for i in range(0, help_wanted_number):
        set_number = i // 7
        month_rule = logic.time.has_lived_months(set_number)
        quest_number = set_number + 1
        quest_number_in_set = i % 7
        if quest_number_in_set < 4:
            quest_number = set_number * 4 + quest_number_in_set + 1
            set_help_wanted_delivery_rule(logic, multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 4:
            set_help_wanted_fishing_rule(logic, multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 5:
            set_help_wanted_slay_monsters_rule(logic, multiworld, player, month_rule, quest_number)
        elif quest_number_in_set == 6:
            set_help_wanted_gathering_rule(logic, multiworld, player, month_rule, quest_number)


def set_help_wanted_delivery_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {item_delivery} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), logic.quest.can_do_item_delivery_quest() & month_rule)


def set_help_wanted_gathering_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {gathering} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), logic.quest.can_do_gathering_quest() & month_rule)


def set_help_wanted_fishing_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {fishing} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), logic.quest.can_do_fishing_quest() & month_rule)


def set_help_wanted_slay_monsters_rule(logic: StardewLogic, multiworld, player, month_rule, quest_number):
    location_name = f"{help_wanted_prefix} {slay_monsters} {quest_number}"
    set_rule(multiworld.get_location(location_name, player), logic.quest.can_do_slaying_quest() & month_rule)


def set_fishsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int):
    fish_prefix = "Fishsanity: "
    for fish_location in locations.locations_by_tag[LocationTags.FISHSANITY]:
        if fish_location.name in all_location_names:
            fish_name = fish_location.name[len(fish_prefix):]
            set_rule(multiworld.get_location(fish_location.name, player),
                     logic.has(fish_name))


def set_museumsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int,
                           world_options: StardewValleyOptions):
    museum_prefix = "Museumsanity: "
    if world_options.museumsanity == Museumsanity.option_milestones:
        for museum_milestone in locations.locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            set_museum_milestone_rule(logic, multiworld, museum_milestone, museum_prefix, player)
    elif world_options.museumsanity != Museumsanity.option_none:
        set_museum_individual_donations_rules(all_location_names, logic, multiworld, museum_prefix, player)


def set_museum_individual_donations_rules(all_location_names, logic: StardewLogic, multiworld, museum_prefix, player):
    all_donations = sorted(locations.locations_by_tag[LocationTags.MUSEUM_DONATIONS],
                           key=lambda x: all_museum_items_by_name[x.name[len(museum_prefix):]].difficulty, reverse=True)
    counter = 0
    number_donations = len(all_donations)
    for museum_location in all_donations:
        if museum_location.name in all_location_names:
            donation_name = museum_location.name[len(museum_prefix):]
            required_detectors = counter * 3 // number_donations
            rule = logic.museum.can_find_museum_item(all_museum_items_by_name[donation_name]) & logic.received(Wallet.metal_detector, required_detectors)
            set_rule(multiworld.get_location(museum_location.name, player),
                     rule)
        counter += 1


def set_museum_milestone_rule(logic: StardewLogic, multiworld: MultiWorld, museum_milestone, museum_prefix: str,
                              player: int):
    milestone_name = museum_milestone.name[len(museum_prefix):]
    donations_suffix = " Donations"
    minerals_suffix = " Minerals"
    artifacts_suffix = " Artifacts"
    metal_detector = Wallet.metal_detector
    rule = None
    if milestone_name.endswith(donations_suffix):
        rule = get_museum_item_count_rule(logic, donations_suffix, milestone_name, all_museum_items, logic.museum.can_find_museum_items)
    elif milestone_name.endswith(minerals_suffix):
        rule = get_museum_item_count_rule(logic, minerals_suffix, milestone_name, all_museum_minerals, logic.museum.can_find_museum_minerals)
    elif milestone_name.endswith(artifacts_suffix):
        rule = get_museum_item_count_rule(logic, artifacts_suffix, milestone_name, all_museum_artifacts, logic.museum.can_find_museum_artifacts)
    elif milestone_name == "Dwarf Scrolls":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in dwarf_scrolls)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Front":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_front)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Middle":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_middle)) & logic.received(metal_detector, 2)
    elif milestone_name == "Skeleton Back":
        rule = And(*(logic.museum.can_find_museum_item(item) for item in skeleton_back)) & logic.received(metal_detector, 2)
    elif milestone_name == "Ancient Seed":
        rule = logic.museum.can_find_museum_item(Artifact.ancient_seed) & logic.received(metal_detector, 2)
    if rule is None:
        return
    set_rule(multiworld.get_location(museum_milestone.name, player), rule)


def get_museum_item_count_rule(logic: StardewLogic, suffix, milestone_name, accepted_items, donation_func):
    metal_detector = Wallet.metal_detector
    num = int(milestone_name[:milestone_name.index(suffix)])
    required_detectors = (num - 1) * 3 // len(accepted_items)
    rule = donation_func(num) & logic.received(metal_detector, required_detectors)
    return rule


def set_backpack_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions, content: StardewContent):
    if world_options.backpack_progression == BackpackProgression.option_vanilla:
        return

    num_per_tier = world_options.backpack_size.count_per_tier()
    start_without_tools = world_options.tool_progression & ToolProgression.value_no_starting_tools
    backpack_tier_names = Backpack.get_purchasable_tiers(content.is_enabled(ModNames.big_backpack), start_without_tools)
    previous_backpacks = 0
    for tier in backpack_tier_names:
        for i in range(1, num_per_tier + 1):
            loc_name = f"{tier} {i}"
            if num_per_tier == 1:
                loc_name = tier
            price = Backpack.prices_per_tier[tier]
            set_rule(multiworld.get_location(loc_name, player),
                     logic.money.can_spend(price) & logic.received("Progressive Backpack", previous_backpacks))
            previous_backpacks += 1


def set_festival_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player):
    festival_locations = []
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL])
    festival_locations.extend(locations.locations_by_tag[LocationTags.FESTIVAL_HARD])
    for festival in festival_locations:
        if festival.name in all_location_names:
            set_rule(multiworld.get_location(festival.name, player),
                     logic.registry.festival_rules[festival.name])


monster_eradication_prefix = "Monster Eradication: "


def set_monstersanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    monstersanity_option = world_options.monstersanity
    if monstersanity_option == Monstersanity.option_none:
        return

    if monstersanity_option == Monstersanity.option_one_per_monster or monstersanity_option == Monstersanity.option_split_goals:
        set_monstersanity_monster_rules(all_location_names, logic, multiworld, player, monstersanity_option)
        return

    if monstersanity_option == Monstersanity.option_progressive_goals:
        set_monstersanity_progressive_category_rules(all_location_names, logic, multiworld, player)
        return

    set_monstersanity_category_rules(all_location_names, logic, multiworld, player, monstersanity_option)


def set_monstersanity_monster_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monstersanity_option):
    for monster_name in logic.monster.all_monsters_by_name:
        location_name = f"{monster_eradication_prefix}{monster_name}"
        if location_name not in all_location_names:
            continue
        location = multiworld.get_location(location_name, player)
        if monstersanity_option == Monstersanity.option_split_goals:
            rule = logic.monster.can_kill_many(logic.monster.all_monsters_by_name[monster_name])
        else:
            rule = logic.monster.can_kill(logic.monster.all_monsters_by_name[monster_name])
        set_rule(location, rule)


def set_monstersanity_progressive_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player):
    for monster_category in logic.monster.all_monsters_by_category:
        set_monstersanity_progressive_single_category_rules(all_location_names, logic, multiworld, player, monster_category)


def set_monstersanity_progressive_single_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monster_category: str):
    location_names = [name for name in all_location_names if name.startswith(monster_eradication_prefix) and name.endswith(monster_category)]
    if not location_names:
        return
    location_names = sorted(location_names, key=lambda name: get_monster_eradication_number(name, monster_category))
    for i in range(5):
        location_name = location_names[i]
        set_monstersanity_progressive_category_rule(all_location_names, logic, multiworld, player, monster_category, location_name, i)


def set_monstersanity_progressive_category_rule(all_location_names: Set[str], logic: StardewLogic, multiworld, player,
                                                monster_category: str, location_name: str, goal_index):
    if location_name not in all_location_names:
        return
    location = multiworld.get_location(location_name, player)
    if goal_index < 3:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index + 1)
    else:
        rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], goal_index * 2)
    set_rule(location, rule)


def get_monster_eradication_number(location_name, monster_category) -> int:
    number = location_name[len(monster_eradication_prefix):-len(monster_category)]
    number = number.strip()
    if number.isdigit():
        return int(number)
    return 1000


def set_monstersanity_category_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, monstersanity_option):
    for monster_category in logic.monster.all_monsters_by_category:
        location_name = f"{monster_eradication_prefix}{monster_category}"
        if location_name not in all_location_names:
            continue
        location = multiworld.get_location(location_name, player)
        if monstersanity_option == Monstersanity.option_one_per_category:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category])
        else:
            rule = logic.monster.can_kill_any(logic.monster.all_monsters_by_category[monster_category], MAX_MONTHS)
        set_rule(location, rule)


def set_shipsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    shipsanity_option = world_options.shipsanity
    if shipsanity_option == Shipsanity.option_none:
        return

    shipsanity_prefix = "Shipsanity: "
    for location in locations.locations_by_tag[LocationTags.SHIPSANITY]:
        if location.name not in all_location_names:
            continue
        item_to_ship = location.name[len(shipsanity_prefix):]
        set_rule(multiworld.get_location(location.name, player), logic.shipping.can_ship(item_to_ship))


def set_cooksanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    cooksanity_option = world_options.cooksanity
    if cooksanity_option == Cooksanity.option_none:
        return

    cooksanity_prefix = "Cook "
    for location in locations.locations_by_tag[LocationTags.COOKSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[len(cooksanity_prefix):]
        recipe = all_cooking_recipes_by_name[recipe_name]
        cook_rule = logic.cooking.can_cook(recipe)
        set_rule(multiworld.get_location(location.name, player), cook_rule)


def set_chefsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    chefsanity_option = world_options.chefsanity
    if chefsanity_option == Chefsanity.option_none:
        return

    chefsanity_suffix = " Recipe"
    for location in locations.locations_by_tag[LocationTags.CHEFSANITY]:
        if location.name not in all_location_names:
            continue
        recipe_name = location.name[:-len(chefsanity_suffix)]
        recipe = all_cooking_recipes_by_name[recipe_name]
        learn_rule = logic.cooking.can_learn_recipe(recipe.source)
        set_rule(multiworld.get_location(location.name, player), learn_rule)


def set_craftsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld, player, world_options: StardewValleyOptions):
    craftsanity_option = world_options.craftsanity
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
        set_rule(multiworld.get_location(location.name, player), craft_rule)


def set_booksanity_rules(logic: StardewLogic, multiworld, player, content: StardewContent):
    booksanity = content.features.booksanity
    if not booksanity.is_enabled:
        return

    for book in content.find_tagged_items(ItemTag.BOOK):
        if booksanity.is_included(book):
            set_rule(multiworld.get_location(booksanity.to_location_name(book.name), player), logic.has(book.name))

    for i, book in enumerate(booksanity.get_randomized_lost_books()):
        if i <= 0:
            continue
        set_rule(multiworld.get_location(booksanity.to_location_name(book), player), logic.received(booksanity.progressive_lost_book, i))


def set_traveling_merchant_day_rules(logic: StardewLogic, multiworld: MultiWorld, player: int):
    for day in Weekday.all_days:
        item_for_day = f"Traveling Merchant: {day}"
        entrance_name = f"Buy from Traveling Merchant {day}"
        set_entrance_rule(multiworld, player, entrance_name, logic.received(item_for_day))


def set_arcade_machine_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    play_junimo_kart_rule = logic.received(Wallet.skull_key)

    if world_options.arcade_machine_locations != ArcadeMachineLocations.option_full_shuffling:
        set_entrance_rule(multiworld, player, Entrance.play_junimo_kart, play_junimo_kart_rule)
        return

    set_entrance_rule(multiworld, player, Entrance.play_junimo_kart, play_junimo_kart_rule & logic.has("Junimo Kart Small Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_2, logic.has("Junimo Kart Medium Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_3, logic.has("Junimo Kart Big Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_junimo_kart_4, logic.has("Junimo Kart Max Buff"))
    set_entrance_rule(multiworld, player, Entrance.play_journey_of_the_prairie_king, logic.has("JotPK Small Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_jotpk_world_2, logic.has("JotPK Medium Buff"))
    set_entrance_rule(multiworld, player, Entrance.reach_jotpk_world_3, logic.has("JotPK Big Buff"))
    set_location_rule(multiworld, player, "Journey of the Prairie King Victory", logic.has("JotPK Max Buff"))


def set_movie_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions, content: StardewContent):
    moviesanity = world_options.moviesanity.value
    if moviesanity <= Moviesanity.option_none:
        return

    if moviesanity >= Moviesanity.option_all_movies:
        watch_prefix = "Watch "
        for movie_location in locations.locations_by_tag[LocationTags.MOVIE]:
            movie_name = movie_location.name[len(watch_prefix):]
            if moviesanity == Moviesanity.option_all_movies:
                rule = logic.movie.can_watch_movie(movie_name)
            elif moviesanity == Moviesanity.option_all_movies_loved or moviesanity == Moviesanity.option_all_movies_and_all_snacks:
                rule = logic.movie.can_watch_movie_with_loving_npc(movie_name)
            else:
                rule = logic.movie.can_watch_movie_with_loving_npc_and_snack(movie_name)
            set_location_rule(multiworld, player, movie_location.name, rule)
    if moviesanity >= Moviesanity.option_all_movies_and_all_snacks:
        snack_prefix = "Share "
        for snack_location in locations.locations_by_tag[LocationTags.MOVIE_SNACK]:
            snack_name = snack_location.name[len(snack_prefix):]
            if moviesanity == Moviesanity.option_all_movies_and_all_loved_snacks:
                rule = logic.movie.can_buy_snack_for_someone_who_loves_it(snack_name)
            else:
                rule = logic.movie.can_buy_snack(snack_name)
            set_location_rule(multiworld, player, snack_location.name, rule)


def set_secrets_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions, content: StardewContent):
    if not world_options.secretsanity:
        return

    if SecretsanityOptionName.easy in world_options.secretsanity:
        set_location_rule(multiworld, player, "Old Master Cannoli", logic.has(Fruit.sweet_gem_berry))
        set_location_rule(multiworld, player, "Pot Of Gold", logic.season.has(Season.spring))
        set_location_rule(multiworld, player, "Poison The Governor", logic.has(SpecialItem.lucky_purple_shorts))
        set_location_rule(multiworld, player, "Grange Display Bribe", logic.has(SpecialItem.lucky_purple_shorts))
        set_location_rule(multiworld, player, "Purple Lettuce", logic.has(SpecialItem.lucky_purple_shorts))
        set_location_rule(multiworld, player, "Make Marnie Laugh", logic.has(SpecialItem.trimmed_purple_shorts) & logic.relationship.can_meet(NPC.marnie))
        set_location_rule(multiworld, player, "Jumpscare Lewis", logic.has(SpecialItem.trimmed_purple_shorts) & logic.relationship.can_meet(NPC.lewis))
        set_location_rule(multiworld, player, "Confront Marnie", logic.gifts.can_gift_to(NPC.marnie, SpecialItem.lucky_purple_shorts))
        set_location_rule(multiworld, player, "Lucky Purple Bobber", logic.fishing.can_use_tackle(SpecialItem.lucky_purple_shorts))
        set_location_rule(multiworld, player, "Something For Santa", logic.season.has(Season.winter) & logic.has_any(AnimalProduct.any_milk, Meal.cookie))
        cc_rewards = ["Bridge Repair", "Greenhouse", "Glittering Boulder Removed", "Minecarts Repair", Transportation.bus_repair, "Friendship Bonus (2 <3)"]
        set_location_rule(multiworld, player, "Jungle Junimo", logic.action.can_speak_junimo() & logic.and_(*[logic.received(reward) for reward in cc_rewards]))
        set_location_rule(multiworld, player, "??HMTGF??", logic.has(Fish.super_cucumber))
        set_location_rule(multiworld, player, "??Pinky Lemon??", logic.has(ArtisanGood.duck_mayonnaise))
        set_location_rule(multiworld, player, "??Foroguemon??", logic.has(Meal.strange_bun) & logic.relationship.has_hearts(NPC.vincent, 2))
        set_location_rule(multiworld, player, "Galaxies Will Heed Your Cry", logic.wallet.can_speak_dwarf())
        set_location_rule(multiworld, player, "Summon Bone Serpent", logic.has(ArtifactName.ancient_doll))
        set_location_rule(multiworld, player, "Meowmere", logic.has(SpecialItem.far_away_stone) & logic.region.can_reach(Region.wizard_basement))
        set_location_rule(multiworld, player, "A Familiar Tune", logic.relationship.can_meet(NPC.elliott))
        set_location_rule(multiworld, player, "Flubber Experiment",
                          logic.relationship.can_get_married() & logic.building.has_building(Building.slime_hutch)
                          & logic.has_all(Machine.slime_incubator, AnimalProduct.slime_egg_green))
        set_location_rule(multiworld, player, "Seems Fishy", logic.money.can_spend_at(Region.wizard_basement, 500))
        set_location_rule(multiworld, player, "What kind of monster is this?", logic.gifts.can_gift_to(NPC.willy, Fish.mutant_carp))
        set_location_rule(multiworld, player, "My mouth is watering already", logic.gifts.can_gift_to(NPC.abigail, Meal.magic_rock_candy))
        set_location_rule(multiworld, player, "A gift of lovely perfume", logic.gifts.can_gift_to(NPC.krobus, Consumable.monster_musk))
        set_location_rule(multiworld, player, "Where exactly does this juice come from?", logic.gifts.can_gift_to(NPC.dwarf, AnimalProduct.cow_milk))
        set_location_rule(multiworld, player, "Thank the Devs", logic.received("Stardrop") & logic.money.can_spend_at(Region.wizard_basement, 500))

    if SecretsanityOptionName.fishing in world_options.secretsanity:
        if world_options.farm_type == FarmType.option_beach:
            set_location_rule(multiworld, player, "'Boat'", logic.fishing.can_fish_at(Region.farm))
        if content.is_enabled(ginger_island_content_pack):
            set_location_rule(multiworld, player, "Foliage Print", logic.fishing.can_fish_with_cast_distance(Region.island_north, 5))
            set_location_rule(multiworld, player, "Frog Hat", logic.fishing.can_fish_at(Region.gourmand_frog_cave))
            set_location_rule(multiworld, player, "Gourmand Statue", logic.fishing.can_fish_at(Region.pirate_cove))
            set_location_rule(multiworld, player, "'Physics 101'", logic.fishing.can_fish_at(Region.volcano_floor_10))
            set_location_rule(multiworld, player, "Lifesaver", logic.fishing.can_fish_at(Region.boat_tunnel))
            set_location_rule(multiworld, player, "Squirrel Figurine", logic.fishing.can_fish_at(Region.volcano_secret_beach))
        set_location_rule(multiworld, player, "Decorative Trash Can", logic.fishing.can_fish_at(Region.town))
        set_location_rule(multiworld, player, "Iridium Krobus", logic.fishing.can_fish_with_cast_distance(Region.forest, 7))
        set_location_rule(multiworld, player, "Pyramid Decal", logic.fishing.can_fish_with_cast_distance(Region.desert, 4))
        set_location_rule(multiworld, player, "'Vista'", logic.fishing.can_fish_at(Region.railroad))
        set_location_rule(multiworld, player, "Wall Basket", logic.fishing.can_fish_at(Region.secret_woods))

    if SecretsanityOptionName.difficult in world_options.secretsanity:
        set_location_rule(multiworld, player, "Free The Forsaken Souls", logic.action.can_watch(Channel.sinister_signal))
        set_location_rule(multiworld, player, "Annoy the Moon Man", logic.shipping.can_use_shipping_bin & logic.time.has_lived_months(6))
        set_location_rule(multiworld, player, "Strange Sighting", logic.region.can_reach_all(Region.bus_stop, Region.town) & logic.time.has_lived_months(6))
        set_location_rule(multiworld, player, "Sea Monster Sighting", logic.region.can_reach(Region.beach) & logic.time.has_lived_months(2))
        set_location_rule(multiworld, player, "...Bigfoot?",
                          logic.region.can_reach_all(Region.forest, Region.town, Region.secret_woods) & logic.time.has_lived_months(4))
        set_location_rule(multiworld, player, "'Me me me me me me me me me me me me me me me me'",
                          logic.region.can_reach(Region.railroad) & logic.tool.has_scythe())
        set_location_rule(multiworld, player, "Secret Iridium Stackmaster Trophy", logic.grind.can_grind_item(10000, Material.wood))

    if SecretsanityOptionName.secret_notes in world_options.secretsanity:
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_1)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_2)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_3)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_4)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_5)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_6)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_7)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_8)
        set_secret_note_gift_rule(logic, multiworld, player, SecretNote.note_9)
        set_location_rule(multiworld, player, SecretNote.note_10, logic.registry.quest_rules[Quest.cryptic_note])
        set_location_rule(multiworld, player, SecretNote.note_11, logic.relationship.can_meet_all(NPC.marnie, NPC.jas, ))
        set_location_rule(multiworld, player, SecretNote.note_12, logic.region.can_reach(Region.town))
        set_location_rule(multiworld, player, SecretNote.note_13, logic.time.has_lived_months(1) & logic.region.can_reach(Region.town))
        set_location_rule(multiworld, player, SecretNote.note_14, logic.region.can_reach(Region.town) & logic.season.has(Season.spring))
        set_location_rule(multiworld, player, SecretNote.note_15, logic.region.can_reach(LogicRegion.night_market))
        set_location_rule(multiworld, player, SecretNote.note_16, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.railroad))
        set_location_rule(multiworld, player, SecretNote.note_17, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.town))
        set_location_rule(multiworld, player, SecretNote.note_18, logic.tool.can_use_tool_at(Tool.hoe, ToolMaterial.basic, Region.desert))
        set_location_rule(multiworld, player, SecretNote.note_19_part_1, logic.region.can_reach(Region.town))
        set_location_rule(multiworld, player, SecretNote.note_19_part_2, logic.region.can_reach(Region.town) & logic.has(SpecialItem.solid_gold_lewis))
        set_location_rule(multiworld, player, SecretNote.note_20, logic.region.can_reach(Region.town) & logic.has(AnimalProduct.rabbit_foot))
        set_location_rule(multiworld, player, SecretNote.note_21, logic.region.can_reach(Region.town))
        set_location_rule(multiworld, player, SecretNote.note_22, logic.registry.quest_rules[Quest.the_mysterious_qi])
        set_location_rule(multiworld, player, SecretNote.note_23, logic.registry.quest_rules[Quest.strange_note])
        set_location_rule(multiworld, player, SecretNote.note_24,
                          logic.building.has_wizard_building(WizardBuilding.junimo_hut) & logic.has(Mineral.any_gem) & logic.season.has_any_not_winter())
        set_location_rule(multiworld, player, SecretNote.note_25, logic.season.has_any_not_winter() & logic.fishing.can_fish_at(Region.railroad)
                          & logic.relationship.can_meet_any(NPC.abigail, NPC.caroline, ))
        set_location_rule(multiworld, player, SecretNote.note_26,
                          logic.building.has_wizard_building(WizardBuilding.junimo_hut) & logic.has(ArtisanGood.raisins) & logic.season.has_any_not_winter())
        set_location_rule(multiworld, player, SecretNote.note_27, logic.region.can_reach(Region.mastery_cave))


def set_secret_note_gift_rule(logic: StardewLogic, multiworld: MultiWorld, player: int, secret_note_location: str) -> None:
    set_location_rule(multiworld, player, secret_note_location, logic.gifts.can_fulfill(gift_requirements[secret_note_location]))


def set_hatsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions, content: StardewContent):
    for hat_location in locations.locations_by_tag[LocationTags.HATSANITY]:
        if hat_location.name not in all_location_names:
            continue
        hat_name = hat_location.name[len(wear_prefix):]
        if hat_name not in content.hats:
            hat_name = f"{hat_name}{hat_clarifier}"
        if hat_name not in content.hats:
            continue
        set_rule(multiworld.get_location(hat_location.name, player), logic.hat.can_wear(hat_name))


def set_eatsanity_rules(all_location_names: Set[str], logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if world_options.eatsanity == Eatsanity.preset_none:
        return
    for eat_location in locations.locations_by_tag[LocationTags.EATSANITY]:
        if eat_location.name not in all_location_names:
            continue
        eat_prefix = "Eat "
        drink_prefix = "Drink "
        if eat_location.name.startswith(eat_prefix):
            item_name = eat_location.name[len(eat_prefix):]
        elif eat_location.name.startswith(drink_prefix):
            item_name = eat_location.name[len(drink_prefix):]
        else:
            raise Exception(f"Eatsanity Location does not have a recognized prefix: '{eat_location.name}'")
        set_rule(multiworld.get_location(eat_location.name, player), logic.has(item_name))


def set_endgame_locations_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, world_options: StardewValleyOptions):
    if not world_options.include_endgame_locations:
        return

    set_location_rule(multiworld, player, "Earth Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.earth_obelisk))
    set_location_rule(multiworld, player, "Water Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.water_obelisk))
    set_location_rule(multiworld, player, "Desert Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.desert_obelisk))
    set_location_rule(multiworld, player, "Junimo Hut Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.junimo_hut))
    set_location_rule(multiworld, player, "Gold Clock Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.gold_clock))
    set_location_rule(multiworld, player, "Purchase Return Scepter", logic.money.can_spend_at(Region.sewer, 2_000_000))
    set_location_rule(multiworld, player, "Pam House Blueprint", logic.money.can_spend_at(Region.carpenter, 500_000) & logic.grind.can_grind_item(950, Material.wood))
    set_location_rule(multiworld, player, "Forest To Beach Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    set_location_rule(multiworld, player, "Mountain Shortcuts Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    set_location_rule(multiworld, player, "Town To Tide Pools Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    set_location_rule(multiworld, player, "Tunnel To Backwoods Shortcut Blueprint", logic.money.can_spend_at(Region.carpenter, 75_000))
    set_location_rule(multiworld, player, "Purchase Statue Of Endless Fortune", logic.money.can_spend_at(Region.casino, 1_000_000))
    set_location_rule(multiworld, player, "Purchase Catalogue", logic.money.can_spend_at(Region.pierre_store, 30_000))
    set_location_rule(multiworld, player, "Purchase Furniture Catalogue", logic.money.can_spend_at(Region.carpenter, 200_000))
    set_location_rule(multiworld, player, "Purchase Joja Furniture Catalogue", logic.action.can_speak_junimo() & logic.money.can_spend_at(Region.movie_theater, 25_000))
    set_location_rule(multiworld, player, "Purchase Junimo Catalogue", logic.action.can_speak_junimo() & logic.money.can_spend_at(LogicRegion.traveling_cart, 70_000))
    set_location_rule(multiworld, player, "Purchase Retro Catalogue", logic.money.can_spend_at(LogicRegion.traveling_cart, 110_000))
    # set_location_rule(multiworld, player, "Find Trash Catalogue", logic) # No need, the region is enough
    set_location_rule(multiworld, player, "Purchase Wizard Catalogue", logic.money.can_spend_at(Region.sewer, 150_000))
    set_location_rule(multiworld, player, "Purchase Tea Set", logic.money.can_spend_at(LogicRegion.traveling_cart, 1_000_000) & logic.time.has_lived_max_months)
    if world_options.friendsanity == Friendsanity.option_all_with_marriage:
        set_location_rule(multiworld, player, "Purchase Abigail Portrait", logic.relationship.can_purchase_portrait(NPC.abigail))
        set_location_rule(multiworld, player, "Purchase Alex Portrait", logic.relationship.can_purchase_portrait(NPC.alex))
        set_location_rule(multiworld, player, "Purchase Elliott Portrait", logic.relationship.can_purchase_portrait(NPC.elliott))
        set_location_rule(multiworld, player, "Purchase Emily Portrait", logic.relationship.can_purchase_portrait(NPC.emily))
        set_location_rule(multiworld, player, "Purchase Haley Portrait", logic.relationship.can_purchase_portrait(NPC.haley))
        set_location_rule(multiworld, player, "Purchase Harvey Portrait", logic.relationship.can_purchase_portrait(NPC.harvey))
        set_location_rule(multiworld, player, "Purchase Krobus Portrait", logic.relationship.can_purchase_portrait(NPC.krobus))
        set_location_rule(multiworld, player, "Purchase Leah Portrait", logic.relationship.can_purchase_portrait(NPC.leah))
        set_location_rule(multiworld, player, "Purchase Maru Portrait", logic.relationship.can_purchase_portrait(NPC.maru))
        set_location_rule(multiworld, player, "Purchase Penny Portrait", logic.relationship.can_purchase_portrait(NPC.penny))
        set_location_rule(multiworld, player, "Purchase Sam Portrait", logic.relationship.can_purchase_portrait(NPC.sam))
        set_location_rule(multiworld, player, "Purchase Sebastian Portrait", logic.relationship.can_purchase_portrait(NPC.sebastian))
        set_location_rule(multiworld, player, "Purchase Shane Portrait", logic.relationship.can_purchase_portrait(NPC.shane))
    elif world_options.friendsanity != Friendsanity.option_none:
        set_location_rule(multiworld, player, "Purchase Spouse Portrait", logic.relationship.can_purchase_portrait())
    if world_options.exclude_ginger_island == ExcludeGingerIsland.option_false:
        set_location_rule(multiworld, player, "Island Obelisk Blueprint", logic.building.can_purchase_wizard_blueprint(WizardBuilding.island_obelisk))
        if world_options.special_order_locations == SpecialOrderLocations.option_board_qi:
            set_location_rule(multiworld, player, "Purchase Horse Flute", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            set_location_rule(multiworld, player, "Purchase Pierre's Missing Stocklist", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            set_location_rule(multiworld, player, "Purchase Key To The Town", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 20))
            set_location_rule(multiworld, player, "Purchase Mini-Shipping Bin", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 60))
            set_location_rule(multiworld, player, "Purchase Exotic Double Bed", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 50))
            set_location_rule(multiworld, player, "Purchase Golden Egg", logic.money.can_trade_at(Region.qi_walnut_room, Currency.qi_gem, 100))


def set_friendsanity_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.features.friendsanity.is_enabled:
        return
    set_location_rule(multiworld, player, "Spouse Stardrop", logic.relationship.has_hearts_with_any_bachelor(13))
    set_location_rule(multiworld, player, "Have a Baby", logic.relationship.can_reproduce(1))
    set_location_rule(multiworld, player, "Have Another Baby", logic.relationship.can_reproduce(2))

    for villager in content.villagers.values():
        for heart in content.features.friendsanity.get_randomized_hearts(villager):
            rule = logic.relationship.can_earn_relationship(villager.name, heart)
            location_name = friendsanity.to_location_name(villager.name, heart)
            set_rule(multiworld.get_location(location_name, player), rule)

    for heart in content.features.friendsanity.get_pet_randomized_hearts():
        rule = logic.pet.can_befriend_pet(heart)
        location_name = friendsanity.to_location_name(NPC.pet, heart)
        set_rule(multiworld.get_location(location_name, player), rule)


def set_deepwoods_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.is_enabled(ModNames.deepwoods):
        return

    set_location_rule(multiworld, player, "Breaking Up Deep Woods Gingerbread House", logic.tool.has_tool(Tool.axe, ToolMaterial.gold))
    set_location_rule(multiworld, player, "Chop Down a Deep Woods Iridium Tree", logic.tool.has_tool(Tool.axe, ToolMaterial.iridium))
    set_entrance_rule(multiworld, player, DeepWoodsEntrance.use_woods_obelisk, logic.received("Woods Obelisk"))
    for depth in range(10, 100 + 10, 10):
        set_entrance_rule(multiworld, player, move_to_woods_depth(depth), logic.mod.deepwoods.can_chop_to_depth(depth))
    set_location_rule(multiworld, player, "The Sword in the Stone", logic.mod.deepwoods.can_pull_sword() & logic.mod.deepwoods.can_chop_to_depth(100))


def set_magic_spell_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.is_enabled(ModNames.magic):
        return

    set_location_rule(multiworld, player, "Analyze: Clear Debris", logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe))
    set_location_rule(multiworld, player, "Analyze: Till", logic.tool.has_tool(Tool.hoe))
    set_location_rule(multiworld, player, "Analyze: Water", logic.tool.has_tool(Tool.watering_can))
    set_location_rule(multiworld, player, "Analyze All Toil School Locations",
                      logic.tool.has_tool(Tool.watering_can)
                      & logic.tool.has_tool(Tool.hoe)
                      & (logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe)))
    # Do I *want* to add boots into logic when you get them even in vanilla without effort?  idk
    set_location_rule(multiworld, player, "Analyze: Evac", logic.ability.can_mine_perfectly())
    set_location_rule(multiworld, player, "Analyze: Haste", logic.has("Coffee"))
    set_location_rule(multiworld, player, "Analyze: Heal", logic.has("Life Elixir"))
    set_location_rule(multiworld, player, "Analyze All Life School Locations",
                      logic.has_all("Coffee", "Life Elixir") & logic.ability.can_mine_perfectly())
    set_location_rule(multiworld, player, "Analyze: Descend", logic.region.can_reach(Region.mines))
    set_location_rule(multiworld, player, "Analyze: Fireball", logic.has("Fire Quartz"))
    set_location_rule(multiworld, player, "Analyze: Frostbolt", logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    set_location_rule(multiworld, player, "Analyze All Elemental School Locations",
                      logic.has("Fire Quartz") & logic.region.can_reach(Region.mines_floor_60) & logic.fishing.can_fish(85))
    # set_location_rule(multiworld, player, "Analyze: Lantern", player),)
    set_location_rule(multiworld, player, "Analyze: Tendrils", logic.region.can_reach(Region.farm))
    set_location_rule(multiworld, player, "Analyze: Shockwave", logic.has("Earth Crystal"))
    set_location_rule(multiworld, player, "Analyze All Nature School Locations", logic.has("Earth Crystal") & logic.region.can_reach("Farm")),
    set_location_rule(multiworld, player, "Analyze: Meteor", logic.region.can_reach(Region.farm) & logic.time.has_lived_months(12)),
    set_location_rule(multiworld, player, "Analyze: Lucksteal", logic.region.can_reach(Region.witch_hut))
    set_location_rule(multiworld, player, "Analyze: Bloodmana", logic.region.can_reach(Region.mines_floor_100))
    set_location_rule(multiworld, player, "Analyze All Eldritch School Locations",
                      logic.region.can_reach_all(Region.witch_hut, Region.mines_floor_100, Region.farm) & logic.time.has_lived_months(12))
    set_location_rule(multiworld, player, "Analyze Every Magic School Location",
                      logic.tool.has_tool(Tool.watering_can)
                      & logic.tool.has_tool(Tool.hoe)
                      & (logic.tool.has_tool(Tool.axe) | logic.tool.has_tool(Tool.pickaxe))
                      & logic.has_all("Coffee", "Life Elixir", "Earth Crystal", "Fire Quartz")
                      & logic.ability.can_mine_perfectly()
                      & logic.fishing.can_fish(85)
                      & logic.region.can_reach_all(Region.witch_hut, Region.mines_floor_100, Region.farm)
                      & logic.time.has_lived_months(12))


def set_sve_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.is_enabled(ModNames.sve):
        return

    set_entrance_rule(multiworld, player, SVEEntrance.forest_to_lost_woods, logic.bundle.can_complete_community_center)
    set_entrance_rule(multiworld, player, SVEEntrance.enter_summit, logic.mod.sve.has_iridium_bomb())
    set_entrance_rule(multiworld, player, SVEEntrance.backwoods_to_grove, logic.mod.sve.has_any_rune())
    set_entrance_rule(multiworld, player, SVEEntrance.badlands_to_cave, logic.has("Aegis Elixir") | logic.combat.can_fight_at_level(Performance.maximum))
    set_entrance_rule(multiworld, player, SVEEntrance.forest_west_to_spring, logic.quest.can_complete_quest(Quest.magic_ink))
    set_entrance_rule(multiworld, player, SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    set_entrance_rule(multiworld, player, SVEEntrance.secret_woods_to_west, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.grandpa_shed_to_interior, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.aurora_warp_to_aurora, logic.received(SVERunes.nexus_aurora))
    set_entrance_rule(multiworld, player, SVEEntrance.farm_warp_to_farm, logic.received(SVERunes.nexus_farm))
    set_entrance_rule(multiworld, player, SVEEntrance.guild_warp_to_guild, logic.received(SVERunes.nexus_guild))
    set_entrance_rule(multiworld, player, SVEEntrance.junimo_warp_to_junimo, logic.received(SVERunes.nexus_junimo))
    set_entrance_rule(multiworld, player, SVEEntrance.spring_warp_to_spring, logic.received(SVERunes.nexus_spring))
    set_entrance_rule(multiworld, player, SVEEntrance.outpost_warp_to_outpost, logic.received(SVERunes.nexus_outpost))
    set_entrance_rule(multiworld, player, SVEEntrance.wizard_warp_to_wizard, logic.received(SVERunes.nexus_wizard))
    set_entrance_rule(multiworld, player, SVEEntrance.use_purple_junimo, logic.relationship.has_hearts(ModNPC.apples, 10))
    set_entrance_rule(multiworld, player, SVEEntrance.grandpa_interior_to_upstairs, logic.mod.sve.has_grandpa_shed_repaired())
    set_entrance_rule(multiworld, player, SVEEntrance.use_bear_shop, (logic.mod.sve.can_buy_bear_recipe()))
    set_entrance_rule(multiworld, player, SVEEntrance.railroad_to_grampleton_station, logic.received(SVEQuestItem.scarlett_job_offer))
    set_entrance_rule(multiworld, player, SVEEntrance.museum_to_gunther_bedroom, logic.relationship.has_hearts(ModNPC.gunther, 2))
    set_entrance_rule(multiworld, player, SVEEntrance.to_aurora_basement, logic.mod.quest.has_completed_aurora_vineyard_bundle())
    logic.mod.sve.initialize_rules()
    for location in logic.registry.sve_location_rules:
        set_rule(multiworld.get_location(location, player),
                 logic.registry.sve_location_rules[location])
    set_sve_ginger_island_rules(logic, multiworld, player, content)
    set_boarding_house_rules(logic, multiworld, player, content)


def set_sve_ginger_island_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    set_entrance_rule(multiworld, player, SVEEntrance.summit_to_highlands, logic.mod.sve.has_marlon_boat())
    set_entrance_rule(multiworld, player, SVEEntrance.wizard_to_fable_reef, logic.received(SVEQuestItem.fable_reef_portal))
    set_entrance_rule(multiworld, player, SVEEntrance.highlands_to_cave,
                      logic.tool.has_tool(Tool.pickaxe, ToolMaterial.iron) & logic.tool.has_tool(Tool.axe, ToolMaterial.iron))
    set_entrance_rule(multiworld, player, SVEEntrance.highlands_to_pond, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))


def set_boarding_house_rules(logic: StardewLogic, multiworld: MultiWorld, player: int, content: StardewContent):
    if not content.is_enabled(ModNames.boarding_house):
        return
    set_entrance_rule(multiworld, player, BoardingHouseEntrance.the_lost_valley_to_lost_valley_ruins, logic.tool.has_tool(Tool.axe, ToolMaterial.iron))


def set_entrance_rule(multiworld, player, entrance: str, rule: StardewRule):
    try:
        potentially_required_regions = look_for_indirect_connection(rule)
        if potentially_required_regions:
            for region in potentially_required_regions:
                logger.debug(f"Registering indirect condition for {region} -> {entrance}")
                multiworld.register_indirect_condition(multiworld.get_region(region, player), multiworld.get_entrance(entrance, player))

        set_rule(multiworld.get_entrance(entrance, player), rule)
    except KeyError as ex:
        logger.error(f"""Failed to evaluate indirect connection in: {explain(rule, CollectionState(multiworld))}""")
        raise ex


def set_island_entrance_rule(multiworld, player, entrance: str, rule: StardewRule, content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    set_entrance_rule(multiworld, player, entrance, rule)


def set_many_island_entrances_rules(multiworld, player, entrance_rules: Dict[str, StardewRule], content: StardewContent):
    if not content.is_enabled(ginger_island_content_pack):
        return
    for entrance, rule in entrance_rules.items():
        set_entrance_rule(multiworld, player, entrance, rule)


def set_location_rule(multiworld, player: int, location_name: str, rule: StardewRule) -> None:
    set_rule(multiworld.get_location(location_name, player), rule)
