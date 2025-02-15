from typing import Dict, List

from BaseClasses import ItemClassification
from .constants.character_names import all_characters
from .constants.combat_items import all_combat_items
from .constants.filler_names import Filler
from .constants.perks import all_perk_items
from .items_classes import ItemData

character_items = [character.name for character in all_characters]


def create_character_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, inventory_item, progression) for i, inventory_item in enumerate(character_items)]


combat_items = [combat_item.name for combat_item in all_combat_items]


def create_combat_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, combat_item, progression) for i, combat_item in enumerate(combat_items)]


perk_items = [perk_item.name for perk_item in all_perk_items]


def create_perk_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + i, perk_item, progression) for i, perk_item in enumerate(perk_items)]


def create_inventory_size_items_data(start_index: int) -> List[ItemData]:
    return [ItemData(start_index + 0, "Combat Inventory Size", progression),
            ItemData(start_index + 1, "Perk Inventory Size", progression)]


progression = ItemClassification.progression

all_items: List[ItemData] = [
    *create_character_items_data(1),
    *create_combat_items_data(201),
    *create_perk_items_data(401),
    *create_inventory_size_items_data(401),
    ItemData(601, Filler.starting_money, ItemClassification.filler),
]


item_table: Dict[str, ItemData] = {}


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


initialize_item_table()
