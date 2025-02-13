from random import Random
from typing import List

from BaseClasses import ItemClassification
from .constants.character_names import all_characters
from .constants.combat_items import all_combat_items
from .constants.perks import all_perk_items
from .items_classes import DungeonClawlerItem
from .options import DungeonClawlerOptions, ShuffleItems, ShufflePerks, ShuffleCharacters
from .constants.filler_names import Filler


def create_items(world, world_options: DungeonClawlerOptions, locations_count: int, random: Random) -> List[DungeonClawlerItem]:
    created_items = []
    create_characters(created_items, world, world_options, locations_count, random)
    create_combat_items_and_perks(created_items, world, world_options, locations_count, random)
    create_fillers(created_items, world, world_options, locations_count, random)
    return created_items


def create_characters(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, random: Random) -> None:
    if world_options.shuffle_characters == ShuffleCharacters.option_false:
        return
    created_items.extend(world.create_item(character.name, ItemClassification.progression) for character in all_characters)


def create_combat_items_and_perks(created_items, world, world_options: DungeonClawlerOptions, locations_count: int, random: Random) -> None:
    valid_items = []
    valid_items.extend(get_valid_combat_items(world_options))
    valid_items.extend(get_valid_perks(world_options))
    if not valid_items:
        return
    chosen_items = random.sample(valid_items, k=locations_count)
    created_items.extend(world.create_item(item, ItemClassification.progression) for item in chosen_items)


def get_valid_combat_items(world_options: DungeonClawlerOptions) -> List[str]:
    if world_options.shuffle_items == ShuffleItems.option_false:
        return []
    valid_combat_items = []
    for combat_item in all_combat_items:
        valid_combat_items.append(combat_item.name)
        if combat_item.upgradeable:
            valid_combat_items.append(combat_item.name)
            if combat_item.max_stack > 1:
                valid_combat_items.extend([combat_item.name] * combat_item.max_stack)
    return valid_combat_items


def get_valid_perks(world_options: DungeonClawlerOptions) -> List[str]:
    if world_options.shuffle_perks == ShufflePerks.option_false:
        return []
    valid_perks = []
    for perk in all_perk_items:
        valid_perks.extend([perk.name] * perk.max_stack)
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
    valid_filler = [Filler.starting_money]
    return valid_filler
