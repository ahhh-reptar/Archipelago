from random import Random
from typing import List

from BaseClasses import ItemClassification
from .constants.fighters import all_fighters
from .constants.combat_items import all_combat_items
from .constants.lucky_paws import all_lucky_paws
from .constants.perks import all_perk_items
from .items_classes import DungeonClawlerItem
from .options import DungeonClawlerOptions, ShuffleCombatItems, ShufflePerks, ShuffleFighters, TrapDifficulty
from .constants.filler_names import all_fillers, all_traps


def create_items(world, world_options: DungeonClawlerOptions, locations_count: int, items_to_exclude: List[str], random: Random) -> List[DungeonClawlerItem]:
    created_items = []
    create_characters(created_items, world, world_options, locations_count, items_to_exclude, random)
    create_inventory_sizes(created_items, world, world_options, locations_count, random)
    create_combat_items_and_perks(created_items, world, world_options, locations_count, items_to_exclude, random)
    create_fillers(created_items, world, world_options, locations_count, random)
    return created_items


def create_characters(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, items_to_exclude: List[str], random: Random) -> None:
    if world_options.shuffle_fighters == ShuffleFighters.option_none:
        return
    characters_to_create = [character.name for character in all_fighters if character.name not in items_to_exclude]
    created_items.extend(world.create_item(character_name, ItemClassification.progression) for character_name in characters_to_create)
    if world_options.shuffle_fighters != ShuffleFighters.option_fighters_and_paws:
        return
    paw_to_create = [paw for paw in all_lucky_paws]
    created_items.extend(world.create_item(paw_name, ItemClassification.progression) for paw_name in paw_to_create)


def create_inventory_sizes(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, random: Random) -> None:
    created_items.extend([world.create_item("Combat Inventory Size", ItemClassification.useful) for i in range(world_options.extra_inventory_sizes.value)])
    created_items.extend([world.create_item("Perk Inventory Size", ItemClassification.useful) for i in range(world_options.extra_inventory_sizes.value)])


def create_combat_items_and_perks(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, items_to_exclude: List[str], random: Random) -> None:
    valid_items = []
    valid_items.extend(get_valid_combat_items(world_options, random))
    valid_items.extend(get_valid_perks(world_options, random))
    for excluded_item in items_to_exclude:
        if excluded_item in valid_items:
            valid_items.remove(excluded_item)
    if not valid_items:
        return
    items_to_create = locations_count - len(created_items)
    if items_to_create > len(valid_items):
        chosen_items = valid_items
    else:
        chosen_items = random.sample(valid_items, k=items_to_create)
    created_items.extend(world.create_item(item, ItemClassification.progression) for item in chosen_items)


def get_valid_combat_items(world_options: DungeonClawlerOptions, random: Random) -> List[str]:
    if world_options.shuffle_combat_items == ShuffleCombatItems.option_false:
        return []
    valid_combat_items = []
    for combat_item in all_combat_items:
        valid_combat_items.extend([combat_item.name] * combat_item.max_stack)
        if combat_item.upgradeable:
            valid_combat_items.append(combat_item.name)
    maximum = world_options.maximum_combat_items.value
    if maximum >= len(valid_combat_items):
        return valid_combat_items
    valid_combat_items = random.sample(valid_combat_items, k=maximum)
    return valid_combat_items


def get_valid_perks(world_options: DungeonClawlerOptions, random: Random) -> List[str]:
    if world_options.shuffle_perks == ShufflePerks.option_false:
        return []
    valid_perks = []
    for perk in all_perk_items:
        valid_perks.extend([perk.name] * perk.max_stack)
    maximum = world_options.maximum_perks.value
    if maximum >= len(valid_perks):
        return valid_perks
    valid_perks = random.sample(valid_perks, k=maximum)
    return valid_perks


def create_fillers(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, random: Random) -> None:
    if locations_count <= len(created_items):
        return
    valid_filler = get_valid_filler_items(world_options)
    number_of_filler = locations_count - len(created_items)
    chosen_filler = random.choices(valid_filler, k=number_of_filler)
    created_filler = [world.create_item(item) for item in chosen_filler]
    created_items.extend(created_filler)


def get_valid_filler_items(world_options: DungeonClawlerOptions) -> List[str]:
    valid_filler = [filler_item for filler_item in all_fillers]
    if world_options.trap_difficulty > TrapDifficulty.option_no_traps:
        valid_filler.extend([trap_item for trap_item in all_traps])
    return valid_filler
