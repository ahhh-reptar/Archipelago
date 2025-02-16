import math
from typing import Union

from BaseClasses import Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import WebWorld, World
from .constants.fighters import all_fighters
from .constants.combat_items import combat_items_by_name
from .constants.filler_names import Filler
from .constants.item_flags import ItemFlags
from .items import item_table
from .items_creation import create_items, get_valid_combat_items
from .items_classes import ItemData, DungeonClawlerItem
from .locations import DungeonClawlerLocation, location_table, create_locations, offset
from .options import DungeonClawlerOptions, Goal, ShuffleCombatItems, ShuffleFighters, ShufflePerks, DungeonClawlerDeathlink, Enemysanity
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

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_items = []

    def generate_early(self) -> None:
        self.precollect_starting_items()

    def precollect_starting_items(self) -> None:
        starting_items = []
        if self.options.shuffle_combat_items == ShuffleCombatItems.option_true:
            valid_combat_items = get_valid_combat_items(self.options, self.random)
            damage_items = [item for item in valid_combat_items if ItemFlags.damage in combat_items_by_name[item].flags]
            starting_items.extend(self.random.sample(damage_items, k=2))
            number_starting_items = 3
            starting_items.extend(self.random.sample(valid_combat_items, k=number_starting_items))

        if self.options.shuffle_fighters != ShuffleFighters.option_none:
            starting_character = self.random.choice(all_fighters)
            starting_items.append(starting_character.name)

        for starting_item in starting_items:
            created_item = self.create_item(starting_item)
            self.multiworld.push_precollected(created_item)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
        create_locations(self.multiworld, self.player, self.options)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options, self.generated_items)

    def create_event(self, event: str):
        return DungeonClawlerItem(event, ItemClassification.progression_skip_balancing, None, self.player)

    def create_items(self):
        locations_count = len([location for location in self.multiworld.get_locations(self.player) if not location.advancement])

        items_to_exclude = [excluded_items for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self, self.options, locations_count, [item.name for item in items_to_exclude], self.multiworld.random)

        self.multiworld.itempool += created_items

        self.setup_victory()

    def create_item(self, item: Union[str, ItemData], classification: ItemClassification = None) -> DungeonClawlerItem:
        if isinstance(item, str):
            item = item_table[item]
        if classification is None:
            classification = item.classification

        self.generated_items.append(item.name)
        return DungeonClawlerItem(item.name, classification, item.code, self.player)

    def setup_victory(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def get_filler_item_name(self) -> str:
        # trap = self.multiworld.random.choice(items_by_group[Group.Trap])
        return Filler.starting_money

    def fill_slot_data(self):
        options_dict = self.options.as_dict(
            Goal.internal_name,
            ShuffleFighters.internal_name,
            ShuffleCombatItems.internal_name,
            ShufflePerks.internal_name,
            Enemysanity.internal_name,
            DungeonClawlerDeathlink.internal_name
        )
        options_dict.update({
            "seed": self.random.randrange(99999999),
            "multiworld_version": "1.0.0",
        })
        return options_dict
