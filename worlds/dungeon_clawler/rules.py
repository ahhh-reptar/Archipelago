from typing import List, Callable, Any

from BaseClasses import ItemClassification, MultiWorld
from worlds.generic.Rules import add_rule
from . import ItemFlags, all_characters
from .constants.combat_items import all_combat_items
from .constants.difficulties import all_difficulties, Difficulty
from .constants.perks import all_perk_items
from .items_classes import DungeonClawlerItem
from .locations import beat_floor_entrance_name, character_location_name
from .options import DungeonClawlerOptions, ShuffleItems, ShufflePerks, ShuffleCharacters


def set_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions):
    set_floor_entrance_rules(multiworld, player, world_options)
    set_character_win_rules(multiworld, player, world_options)


def set_floor_entrance_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions):
    for floor in range(1, 50):
        for difficulty in all_difficulties:
            floor_entrance_name = beat_floor_entrance_name(floor, difficulty)
            floor_entrance = multiworld.get_entrance(floor_entrance_name, player)
            required_combat_items = floor * 4
            if difficulty == Difficulty.hard:
                required_combat_items += 4
            elif difficulty == Difficulty.very_hard:
                required_combat_items += 8
            elif difficulty == Difficulty.nightmare:
                required_combat_items += 12
            if world_options.shuffle_items == ShuffleItems.option_true:
                add_rule(floor_entrance, has_count_combat_items(required_combat_items, player))
            if world_options.shuffle_perks == ShufflePerks.option_true:
                add_rule(floor_entrance, has_count_perks(required_combat_items // 4, player))


def has_count_combat_items(number: int, player: int) -> Callable[[Any], bool]:
    combat_items = []
    combat_items.extend(all_combat_items)
    damage_items = [item for item in combat_items if ItemFlags.damage in item.flags]
    combat_item_names = [item.name for item in combat_items]
    damage_items_names = [item.name for item in damage_items]
    return lambda state: has_count(state, number, player, combat_item_names) and has_count(state, number//4, player, damage_items_names)


def has_count_perks(number: int, player: int) -> Callable[[Any], bool]:
    perks = []
    perks.extend(all_perk_items)
    perks_names = [item.name for item in perks]
    return lambda state: has_count(state, number, player, perks_names)


def set_character_win_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions):
    for character in all_characters:
        character_win_location_name = character_location_name(character.name)
        character_win_location =  multiworld.get_location(character_win_location_name, player)
        if world_options.shuffle_characters == ShuffleCharacters.option_true:
            add_rule(character_win_location, lambda state: state.has(character.name, player))
        synergy_items = []
        for good_flag in character.good_item_flags:
            if world_options.shuffle_items == ShuffleItems.option_true:
                synergy_items.extend([item.name for item in all_combat_items if good_flag in item.flags])
            if world_options.shuffle_perks == ShufflePerks.option_true:
                synergy_items.extend([item.name for item in all_perk_items if good_flag in item.flags])
        if synergy_items:
            add_rule(character_win_location, has_count_rule(8, player, synergy_items))


def has_count_rule(number: int, player: int, items: List[str]) -> Callable[[Any], bool]:
    return lambda state: has_count(state, number, player, items)


def has_count(state, number: int, player: int, items: List[str]) -> bool:
    return state.has_from_list(items, player, number)