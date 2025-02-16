import math
from typing import List, Callable, Any

from BaseClasses import ItemClassification, MultiWorld
from worlds.generic.Rules import add_rule
from . import ItemFlags, all_fighters
from .constants.combat_items import all_combat_items
from .constants.difficulties import all_difficulties, Difficulty
from .constants.lucky_paws import all_lucky_paws
from .constants.perks import all_perk_items, max_perk_stack
from .items_classes import DungeonClawlerItem
from .locations import beat_floor_entrance_name, character_location_name, perk_location_name
from .options import DungeonClawlerOptions, ShuffleCombatItems, ShufflePerks, ShuffleFighters, Enemysanity


def set_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions, generated_items: List[str]):
    set_floor_entrance_rules(multiworld, player, world_options, generated_items)
    set_character_win_rules(multiworld, player, world_options, generated_items)
    set_perk_rules(multiworld, player, world_options, generated_items)


def set_floor_entrance_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions, generated_items: List[str]):
    generated_combat_items = [item for item in generated_items if item in [combat_item.name for combat_item in all_combat_items]]
    generated_perks = [item for item in generated_items if item in [perk.name for perk in all_perk_items]]
    for i, difficulty in enumerate(all_difficulties):
        if i <= 0:
            continue
        entrance_name = f"Start {difficulty} Run"
        start_run_name = multiworld.get_entrance(entrance_name, player)
        if world_options.shuffle_fighters >= ShuffleFighters.option_fighters:
            add_rule(start_run_name, has_count_fighters(i, player))
        if world_options.shuffle_fighters == ShuffleFighters.option_fighters_and_paws:
            add_rule(start_run_name, has_count_paws(i, player))
    for floor in range(1, 50):
        for difficulty in all_difficulties:
            floor_entrance_name = beat_floor_entrance_name(floor, difficulty)
            floor_entrance = multiworld.get_entrance(floor_entrance_name, player)
            required_combat_items = get_required_combat_items(floor, difficulty, world_options)
            required_perks = (required_combat_items - 4)
            if world_options.shuffle_combat_items == ShuffleCombatItems.option_true:
                required_combat_items = min(len(generated_combat_items), required_combat_items)
                add_rule(floor_entrance, has_count_combat_items(required_combat_items, player))
            if world_options.shuffle_perks == ShufflePerks.option_true:
                required_perks = min(len(generated_perks), required_perks)
                add_rule(floor_entrance, has_count_perks(required_perks, player))


def get_required_combat_items(floor: int, difficulty: str, world_options: DungeonClawlerOptions):
    required_combat_items = 2
    if difficulty == Difficulty.normal:
        required_combat_items += floor * 0.75
    elif difficulty == Difficulty.hard:
        required_combat_items += floor
    elif difficulty == Difficulty.very_hard:
        required_combat_items += floor * 1.25
    elif difficulty == Difficulty.nightmare:
        required_combat_items += floor * 1.5
    if world_options.shuffle_perks == ShufflePerks.option_true:
        if floor > 5:
            required_combat_items += 5
        if floor > 10:
            required_combat_items += 5
        if floor > 15:
            required_combat_items += 5
    if world_options.enemysanity == Enemysanity.option_true:
        if difficulty == Difficulty.hard:
            required_combat_items += 5
        if difficulty == Difficulty.very_hard:
            required_combat_items += 10
        if difficulty == Difficulty.nightmare:
            required_combat_items += 15
    return round(required_combat_items)


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


def has_count_fighters(number: int, player: int) -> Callable[[Any], bool]:
    fighters = []
    fighters.extend(all_fighters)
    fighter_names = [fighter.name for fighter in fighters]
    return lambda state: has_count(state, number, player, fighter_names)


def has_count_paws(number: int, player: int) -> Callable[[Any], bool]:
    paw_names = []
    paw_names.extend(all_lucky_paws)
    return lambda state: has_count(state, number, player, paw_names)


def set_character_win_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions, generated_items: List[str]):
    if world_options.shuffle_fighters == ShuffleFighters.option_none:
        return
    for character in all_fighters:
        character_win_location_name = character_location_name(character.name)
        character_win_location = multiworld.get_location(character_win_location_name, player)
        add_rule(character_win_location, lambda state, name=character.name: state.has(name, player))
        synergy_items = []
        for good_flag in character.good_item_flags:
            if world_options.shuffle_combat_items == ShuffleCombatItems.option_true:
                synergy_items.extend([item.name for item in all_combat_items if good_flag in item.flags])
            if world_options.shuffle_perks == ShufflePerks.option_true:
                synergy_items.extend([item.name for item in all_perk_items if good_flag in item.flags])
        generated_synergy_items = [item for item in generated_items if item in [synergy_item for synergy_item in synergy_items]]
        if synergy_items:
            required_synergy_items = min(5, len(generated_synergy_items))
            add_rule(character_win_location, has_count_rule(required_synergy_items, player, synergy_items))


def set_perk_rules(multiworld: MultiWorld, player, world_options: DungeonClawlerOptions, generated_items: List[str]):
    if world_options.shuffle_perks == ShufflePerks.option_false:
        return

    generated_perks = {}
    for item in generated_items:
        if item in [perk.name for perk in all_perk_items]:
            if item not in generated_perks:
                generated_perks[item] = 0
            generated_perks[item] += 1

    for perk in all_perk_items:
        for level in range(1, min(max_perk_stack, perk.max_stack)+1):
            perk_obtention_location_name = perk_location_name(perk.name, level)
            perk_obtention_location =  multiworld.get_location(perk_obtention_location_name, player)
            if perk.name in generated_perks:
                generated_amount = generated_perks[perk.name]
                if generated_amount >= level:
                    add_rule(perk_obtention_location, has_rule(player, perk.name, level))
                else:
                    add_rule(perk_obtention_location, has_rule(player, perk.name, generated_amount))
            else:
                add_rule(perk_obtention_location, has_count_rule(level * 2, player, [item.name for item in all_perk_items]))


def has_count_rule(number: int, player: int, items: List[str]) -> Callable[[Any], bool]:
    return lambda state: has_count(state, number, player, items)


def has_count(state, number: int, player: int, items: List[str]) -> bool:
    return state.has_from_list(items, player, number)


def has_rule(player: int, item: str, number: int = 1) -> Callable[[Any], bool]:
    return lambda state: has(state, player, item, number)


def has(state, player: int, item: str, number: int = 1) -> bool:
    return state.has(item, player, number)