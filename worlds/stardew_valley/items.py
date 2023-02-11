import bisect
import csv
import enum
import logging
import math
import os
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import cached_property
from random import Random
from typing import Dict, List, Protocol, Union, Set, Optional

from BaseClasses import Item, ItemClassification
from . import options

ITEM_CODE_OFFSET = 717000
RESOURCE_PACK_CODE_OFFSET = 500

logger = logging.getLogger(__name__)
world_folder = os.path.dirname(__file__)

class Group(enum.Enum):
    RESOURCE_PACK = enum.auto()
    COMMUNITY_REWARD = enum.auto()
    TRASH = enum.auto()
    MINES_FLOOR_10 = enum.auto()
    MINES_FLOOR_20 = enum.auto()
    MINES_FLOOR_50 = enum.auto()
    MINES_FLOOR_60 = enum.auto()
    MINES_FLOOR_80 = enum.auto()
    MINES_FLOOR_90 = enum.auto()
    MINES_FLOOR_110 = enum.auto()
    FOOTWEAR = enum.auto()
    HATS = enum.auto()
    RING = enum.auto()
    WEAPON = enum.auto()
    PROGRESSIVE_TOOLS = enum.auto()
    SKILL_LEVEL_UP = enum.auto()
    ARCADE_MACHINE_BUFFS = enum.auto()
    GALAXY_WEAPONS = enum.auto()


@dataclass(frozen=True)
class ItemData:
    code_without_offset: Optional[int]
    name: str
    classification: ItemClassification
    groups: Set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self):
        return ITEM_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


@dataclass(frozen=True)
class ResourcePackData:
    name: str
    default_amount: int = 1
    scaling_factor: int = 1
    classification: ItemClassification = ItemClassification.filler

    def as_item_data(self, base_code: int) -> [ItemData]:
        return [ItemData(base_code + i, self.create_item_name(quantity), self.classification, {Group.RESOURCE_PACK})
                for i, (_, quantity) in enumerate(self.scale_quantity.items())]

    def create_item_name(self, quantity: int) -> str:
        return f"Resource Pack: {quantity} {self.name}"

    @cached_property
    def scale_quantity(self) -> OrderedDict[int, int]:
        """Discrete scaling of the resource pack quantities.
        100 is default, 200 is double, 50 is half (if the scaling_factor allows it).
        """
        levels = math.ceil(self.default_amount / self.scaling_factor) * 2
        first_level = self.default_amount % self.scaling_factor
        if first_level == 0:
            first_level = self.scaling_factor
        quantities = sorted(set(range(first_level, self.scaling_factor * levels, self.scaling_factor))
                            | {self.default_amount * 2})

        return OrderedDict({round(quantity / self.default_amount * 100): quantity
                            for quantity in quantities
                            if quantity <= self.default_amount * 2})

    def calculate_quantity(self, multiplier: int) -> int:
        scales = list(self.scale_quantity)
        left_scale = bisect.bisect_left(scales, multiplier)
        closest_scale = min([scales[left_scale], scales[left_scale - 1]],
                            key=lambda x: abs(multiplier - x))
        return self.scale_quantity[closest_scale]

    def create_name_from_multiplier(self, multiplier: int) -> str:
        return self.create_item_name(self.calculate_quantity(multiplier))


class FriendshipPackData(ResourcePackData):
    def create_item_name(self, quantity: int) -> str:
        return f"Friendship Bonus ({quantity} <3)"


class StardewItemFactory(Protocol):
    def __call__(self, name: Union[str, ItemData]) -> Item:
        raise NotImplementedError


def load_item_csv():
    items = []
    with open(world_folder + "/data/items.csv") as item_csv:
        item_reader = csv.DictReader(item_csv)
        for item in item_reader:
            id = int(item["id"]) if item["id"] != "None" else None
            classification = ItemClassification[item["classification"]]
            groups = {Group[group] for group in item["groups"].split(",") if group}
            items.append(ItemData(id, item["name"], classification, groups))
    return items


all_items: List[ItemData] = load_item_csv()
item_table: Dict[str, ItemData] = {}
items_by_group: Dict[Group, List[ItemData]] = {}


def initialize_resource_pack_items():
    resource_pack_code = RESOURCE_PACK_CODE_OFFSET
    for resource_pack in resource_packs + [friendship_pack]:
        new_items = resource_pack.as_item_data(resource_pack_code)
        item_table.update({item.name: item for item in new_items})
        resource_pack_code = new_items[-1].code_without_offset + 1


def initialize_groups():
    for item in all_items:
        for group in item.groups:
            item_group = items_by_group.get(group, list())
            item_group.append(item)
            items_by_group[group] = item_group


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})


base_resource_packs = {
    ResourcePackData("Money", default_amount=1000, scaling_factor=500, classification=ItemClassification.useful),
    ResourcePackData("Stone", default_amount=50, scaling_factor=25),
    ResourcePackData("Wood", default_amount=50, scaling_factor=25),
    ResourcePackData("Hardwood", default_amount=10, scaling_factor=5, classification=ItemClassification.useful),
    ResourcePackData("Fiber", default_amount=30, scaling_factor=15),
    ResourcePackData("Coal", default_amount=10, scaling_factor=5),
    ResourcePackData("Clay", default_amount=10, scaling_factor=5),
}

warp_totem_resource_packs = [
    ResourcePackData("Warp Totem: Beach", default_amount=5, scaling_factor=2),
    ResourcePackData("Warp Totem: Desert", default_amount=5, scaling_factor=2),
    ResourcePackData("Warp Totem: Farm", default_amount=5, scaling_factor=2),
    ResourcePackData("Warp Totem: Island", default_amount=5, scaling_factor=2),
    ResourcePackData("Warp Totem: Mountains", default_amount=5, scaling_factor=2),
]

geode_resource_packs = [
    ResourcePackData("Geode", default_amount=12, scaling_factor=6),
    ResourcePackData("Frozen Geode", default_amount=8, scaling_factor=4),
    ResourcePackData("Magma Geode", default_amount=6, scaling_factor=3),
    ResourcePackData("Omni Geode", default_amount=4, scaling_factor=2, classification=ItemClassification.useful),
]

metal_resource_packs = [
    ResourcePackData("Copper Ore", default_amount=75, scaling_factor=25),
    ResourcePackData("Iron Ore", default_amount=50, scaling_factor=25),
    ResourcePackData("Gold Ore", default_amount=25, scaling_factor=13, classification=ItemClassification.useful),
    ResourcePackData("Iridium Ore", default_amount=10, scaling_factor=5, classification=ItemClassification.useful),
    ResourcePackData("Quartz", default_amount=10, scaling_factor=5)
]

fertilizer_resource_packs = [
    ResourcePackData("Basic Fertilizer", default_amount=30, scaling_factor=10),
    ResourcePackData("Basic Retaining Soil", default_amount=30, scaling_factor=10),
    ResourcePackData("Speed-Gro", default_amount=30, scaling_factor=10),
    ResourcePackData("Quality Fertilizer", default_amount=20, scaling_factor=10),
    ResourcePackData("Quality Retaining Soil", default_amount=20, scaling_factor=10),
    ResourcePackData("Deluxe Speed-Gro", default_amount=20, scaling_factor=10),
    ResourcePackData("Deluxe Fertilizer", default_amount=10, scaling_factor=10,
                     classification=ItemClassification.useful),
    ResourcePackData("Deluxe Retaining Soil", default_amount=10, scaling_factor=10,
                     classification=ItemClassification.useful),
    ResourcePackData("Hyper Speed-Gro", default_amount=10, scaling_factor=10, classification=ItemClassification.useful),
    ResourcePackData("Tree Fertilizer", default_amount=10, scaling_factor=10),
]

seed_resource_packs = [
    ResourcePackData("Spring Seeds", default_amount=30, scaling_factor=10),
    ResourcePackData("Summer Seeds", default_amount=30, scaling_factor=10),
    ResourcePackData("Fall Seeds", default_amount=30, scaling_factor=10),
    ResourcePackData("Winter Seeds", default_amount=30, scaling_factor=10),
    ResourcePackData("Mahogany Seed", default_amount=5, scaling_factor=2),
]

fishing_resource_packs = [
    ResourcePackData("Bait", default_amount=30, scaling_factor=10),
    ResourcePackData("Crab Pot", default_amount=3),
]

resource_packs = [
    *base_resource_packs,
    *warp_totem_resource_packs,
    *geode_resource_packs,
    *metal_resource_packs,
    *fertilizer_resource_packs,
    *seed_resource_packs,
    *fishing_resource_packs,
]

friendship_pack = FriendshipPackData("Friendship Bonus", default_amount=2, classification=ItemClassification.useful)

initialize_item_table()
initialize_resource_pack_items()
initialize_groups()


def create_items(item_factory: StardewItemFactory, locations_count: int, world_options: options.StardewOptions,
                 random: Random) \
        -> List[Item]:
    items = create_unique_items(item_factory, world_options, random)
    assert len(items) <= locations_count, \
        "There should be at least as many locations as there are mandatory items"
    logger.debug(f"Created {len(items)} unique items")

    resource_pack_items = fill_with_resource_packs(item_factory, world_options, random, locations_count - len(items))
    items += resource_pack_items
    logger.debug(f"Created {len(resource_pack_items)} resource packs")

    return items


def create_backpack_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if (world_options[options.BackpackProgression] == options.BackpackProgression.option_progressive or
            world_options[options.BackpackProgression] == options.BackpackProgression.option_early_progressive):
        items.extend(item_factory(item) for item in ["Progressive Backpack"] * 2)


def create_mine_rewards(item_factory: StardewItemFactory, items: List[Item], random: Random):
    items.append(item_factory("Rusty Sword"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_10])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_20])))
    items.append(item_factory("Slingshot"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_50])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_60])))
    items.append(item_factory("Master Slingshot"))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_80])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_90])))
    items.append(item_factory(random.choice(items_by_group[Group.MINES_FLOOR_110])))
    items.append(item_factory("Skull Key"))


def create_mine_elevators(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if (world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive or
            world_options[options.TheMinesElevatorsProgression] ==
            options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
        items.extend([item_factory(item) for item in ["Progressive Mine Elevator"] * 24])


def create_tools(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.ToolProgression] == options.ToolProgression.option_progressive:
        items.extend(item_factory(item) for item in items_by_group[Group.PROGRESSIVE_TOOLS] * 4)
    items.append(item_factory("Golden Scythe"))


def create_skills(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.SkillProgression] == options.SkillProgression.option_progressive:
        items.extend([item_factory(item) for item in items_by_group[Group.SKILL_LEVEL_UP] * 10])


def create_wizard_buildings(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Earth Obelisk"))
    items.append(item_factory("Water Obelisk"))
    items.append(item_factory("Desert Obelisk"))
    items.append(item_factory("Island Obelisk"))
    items.append(item_factory("Junimo Hut"))
    items.append(item_factory("Gold Clock"))


def create_carpenter_buildings(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.BuildingProgression] in {options.BuildingProgression.option_progressive,
                                                      options.BuildingProgression.option_progressive_early_shipping_bin}:
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Coop"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Progressive Barn"))
        items.append(item_factory("Well"))
        items.append(item_factory("Silo"))
        items.append(item_factory("Mill"))
        items.append(item_factory("Progressive Shed"))
        items.append(item_factory("Progressive Shed"))
        items.append(item_factory("Fish Pond"))
        items.append(item_factory("Stable"))
        items.append(item_factory("Slime Hutch"))
        items.append(item_factory("Shipping Bin"))
        items.append(item_factory("Progressive House"))
        items.append(item_factory("Progressive House"))
        items.append(item_factory("Progressive House"))


def create_special_quest_rewards(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Adventurer's Guild"))
    items.append(item_factory("Club Card"))
    items.append(item_factory("Magnifying Glass"))
    items.append(item_factory("Bear's Knowledge"))
    items.append(item_factory("Iridium Snake Milk"))


def create_stardrops(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Stardrop"))  # The Mines level 100
    items.append(item_factory("Stardrop"))  # Old Master Cannoli


def create_arcade_machine_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Boots"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Gun"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Progressive Ammo"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Extra Life"))
        items.append(item_factory("JotPK: Increased Drop Rate"))
        items.extend(item_factory(item) for item in ["Junimo Kart: Extra Life"] * 8)


def create_player_buffs(item_factory: StardewItemFactory, world_options: options.StardewOptions, items: List[Item]):
    number_of_buffs: int = world_options[options.NumberOfPlayerBuffs]
    items.extend(item_factory(item) for item in ["Movement Speed Bonus"] * number_of_buffs)
    items.extend(item_factory(item) for item in ["Luck Bonus"] * number_of_buffs)


def create_traveling_merchant_items(item_factory: StardewItemFactory, items: List[Item]):
    items.append(item_factory("Traveling Merchant: Sunday"))
    items.append(item_factory("Traveling Merchant: Monday"))
    items.append(item_factory("Traveling Merchant: Tuesday"))
    items.append(item_factory("Traveling Merchant: Wednesday"))
    items.append(item_factory("Traveling Merchant: Thursday"))
    items.append(item_factory("Traveling Merchant: Friday"))
    items.append(item_factory("Traveling Merchant: Saturday"))
    items.extend(item_factory(item) for item in ["Traveling Merchant Stock Size"] * 6)
    items.extend(item_factory(item) for item in ["Traveling Merchant Discount"] * 8)


def create_unique_items(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random) -> \
        List[Item]:
    items = []

    items.extend(item_factory(item) for item in items_by_group[Group.COMMUNITY_REWARD])

    create_backpack_items(item_factory, world_options, items)
    create_mine_rewards(item_factory, items, random)
    create_mine_elevators(item_factory, world_options, items)
    create_tools(item_factory, world_options, items)
    create_skills(item_factory, world_options, items)
    create_wizard_buildings(item_factory, items)
    create_carpenter_buildings(item_factory, world_options, items)
    items.append(item_factory("Beach Bridge"))
    create_special_quest_rewards(item_factory, items)
    create_stardrops(item_factory, items)
    create_arcade_machine_items(item_factory, world_options, items)
    items.append(item_factory(random.choice(items_by_group[Group.GALAXY_WEAPONS])))
    items.append(item_factory(friendship_pack.create_name_from_multiplier(world_options[options.ResourcePackMultiplier])))
    create_player_buffs(item_factory, world_options, items)
    create_traveling_merchant_items(item_factory, items)
    return items


def fill_with_resource_packs(item_factory: StardewItemFactory, world_options: options.StardewOptions, random: Random,
                             required_resource_pack: int) -> List[Item]:
    resource_pack_multiplier = world_options[options.ResourcePackMultiplier]

    if resource_pack_multiplier == 0:
        return [item_factory(cola) for cola in ["Joja Cola"] * required_resource_pack]

    items = []

    for i in range(required_resource_pack):
        resource_pack = random.choice(resource_packs)
        items.append(item_factory(resource_pack.create_name_from_multiplier(resource_pack_multiplier)))

    return items
