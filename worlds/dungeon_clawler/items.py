from typing import Dict, List

from BaseClasses import ItemClassification
from .constants.fighters import all_fighters
from .constants.combat_items import all_combat_items
from .constants.filler_names import Filler, all_fillers, all_traps
from .constants.lucky_paws import all_lucky_paws
from .constants.perks import all_perk_items
from .items_classes import ItemData

character_items = [character.name for character in all_fighters]


def create_character_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, inventory_item, progression) for i, inventory_item in enumerate(character_items)]


lucky_paw_items = [paw for paw in all_lucky_paws]


def create_lucky_paws_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, paw_item, progression) for i, paw_item in enumerate(lucky_paw_items)]


combat_items = [combat_item.name for combat_item in all_combat_items]


def create_combat_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, combat_item, progression) for i, combat_item in enumerate(combat_items)]


perk_items = [perk_item.name for perk_item in all_perk_items]


def create_perk_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, perk_item, progression) for i, perk_item in enumerate(perk_items)]


def create_inventory_size_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + 0, "Combat Inventory Size", ItemClassification.useful),
            ItemData(start_index + 1, "Perk Inventory Size", ItemClassification.useful)]


filler_items = [filler_item for filler_item in all_fillers]


def create_filler_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, filler_item, ItemClassification.filler) for i, filler_item in enumerate(filler_items)]


trap_items = [trap_item for trap_item in all_traps]


def create_trap_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, trap_item, ItemClassification.trap) for i, trap_item in enumerate(trap_items)]


progression = ItemClassification.progression

all_items: List[ItemData] = [
    *create_character_items_data(1),
    *create_lucky_paws_items_data(101),
    *create_combat_items_data(201),
    *create_perk_items_data(401),
    *create_inventory_size_items_data(601),
    *create_filler_items_data(801),
    *create_trap_items_data(1001),
]


item_table: Dict[str, ItemData] = {}


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


initialize_item_table()
