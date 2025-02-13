import math
from typing import Union

from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .constants.character_names import all_characters
from .constants.combat_items import combat_items_by_name
from .constants.filler_names import Filler
from .constants.item_flags import ItemFlags
from .items import item_table
from .items_creation import create_items, get_valid_combat_items
from .items_classes import ItemData, DungeonClawlerItem
from .locations import DungeonClawlerLocation, location_table, create_locations, offset
from .options import DungeonClawlerOptions, Goal, ShuffleItems, ShuffleCharacters, ShufflePerks, DungeonClawlerDeathlink, Enemysanity
from .regions import create_regions
from .rules import set_rules
from .constants.world_strings import GAME_NAME

client_version = 0


class DungeonClawlerWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Dungeon Clawler game on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Kaito Kid"]
    )
    tutorials = [setup_en]


class DungeonClawlerWorld(World):
    """
    Dungeon Clawler mixes deck building with a dash of rogue-like mechanics and most importantly: a claw machine.
    """
    game = GAME_NAME
    topology_present = False
    web = DungeonClawlerWebWorld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    options_dataclass = DungeonClawlerOptions
    options: DungeonClawlerOptions

    def generate_early(self) -> None:
        self.precollect_starting_items()

    def precollect_starting_items(self) -> None:
        starting_items = []
        if self.options.shuffle_items == ShuffleItems.option_true:
            valid_combat_items = get_valid_combat_items(self.options)
            number_starting_items = 5
            starting_combat_items = self.random.sample(valid_combat_items, k=number_starting_items)
            damage_items = [item for item in valid_combat_items if ItemFlags.damage in combat_items_by_name[item].flags]
            while not any([damage_item in starting_combat_items for damage_item in damage_items]):
                starting_combat_items.append(self.random.choice(valid_combat_items))
            starting_items.extend(starting_combat_items)

        if self.options.shuffle_characters == ShuffleCharacters.option_true:
            starting_character = self.random.choice(all_characters)
            starting_items.append(starting_character.name)

        for starting_item in starting_items:
            created_item = DungeonClawlerItem(starting_item, ItemClassification.progression, offset + item_table[starting_item].code_without_offset, self.player)
            self.multiworld.push_precollected(created_item)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
        create_locations(self.multiworld, self.player, self.options)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_event(self, event: str):
        return DungeonClawlerItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def create_items(self):
        locations_count = len([location for location in self.multiworld.get_locations(self.player) if not location.advancement])

        items_to_exclude = [excluded_items for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self, self.options, locations_count + len(items_to_exclude), self.multiworld.random)

        self.multiworld.itempool += created_items

        for item in items_to_exclude:
            if item in self.multiworld.itempool:
                self.multiworld.itempool.remove(item)

        self.setup_victory()

    def create_item(self, item: Union[str, ItemData], classification: ItemClassification = None) -> DungeonClawlerItem:
        if isinstance(item, str):
            item = item_table[item]
        if classification is None:
            classification = item.classification

        return DungeonClawlerItem(item.name, classification, item.code, self.player)

    def setup_victory(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def get_filler_item_name(self) -> str:
        # trap = self.multiworld.random.choice(items_by_group[Group.Trap])
        return Filler.starting_money

    def fill_slot_data(self):
        options_dict = self.options.as_dict(
            Goal.internal_name,
            ShuffleCharacters.internal_name,
            ShuffleItems.internal_name,
            ShufflePerks.internal_name,
            Enemysanity.internal_name,
            DungeonClawlerDeathlink.internal_name
        )
        options_dict.update({
            "seed": self.random.randrange(99999999),
            "multiworld_version": "1.0.0",
        })
        return options_dict
