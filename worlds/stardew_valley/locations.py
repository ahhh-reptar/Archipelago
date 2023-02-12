import csv
import enum
import os
from dataclasses import dataclass
from typing import Optional, Dict, Protocol, List

from . import options

LOCATION_CODE_OFFSET = 717000
world_folder = os.path.dirname(__file__)


class LocationTags(enum.Enum):
    MANDATORY = enum.auto()
    BUNDLE = enum.auto()
    COMMUNITY_CENTER_BUNDLE = enum.auto()
    CRAFTS_ROOM_BUNDLE = enum.auto()
    PANTRY_BUNDLE = enum.auto()
    FISH_TANK_BUNDLE = enum.auto()
    BOILER_ROOM_BUNDLE = enum.auto()
    BULLETIN_BOARD_BUNDLE = enum.auto()
    VAULT_BUNDLE = enum.auto()
    COMMUNITY_CENTER_ROOM = enum.auto()
    BACKPACK = enum.auto()
    TOOL_UPGRADE = enum.auto()
    HOE_UPGRADE = enum.auto()
    PICKAXE_UPGRADE = enum.auto()
    AXE_UPGRADE = enum.auto()
    WATERING_CAN_UPGRADE = enum.auto()
    TRASH_CAN_UPGRADE = enum.auto()
    FISHING_ROD_UPGRADE = enum.auto()
    THE_MINES_TREASURE = enum.auto()
    THE_MINES_ELEVATOR = enum.auto()
    SKILL_LEVEL = enum.auto()
    FARMING_LEVEL = enum.auto()
    FISHING_LEVEL = enum.auto()
    FORAGING_LEVEL = enum.auto()
    COMBAT_LEVEL = enum.auto()
    MINING_LEVEL = enum.auto()
    BUILDING_BLUEPRINT = enum.auto()
    QUEST = enum.auto()
    ARCADE_MACHINE = enum.auto()
    ARCADE_MACHINE_VICTORY = enum.auto()
    JOTPK = enum.auto()
    JUNIMO_KART = enum.auto()
    HELP_WANTED = enum.auto()
    TRAVELING_MERCHANT = enum.auto()


@dataclass(frozen=True)
class LocationData:
    code_without_offset: Optional[int]
    region: str
    name: str
    tags: frozenset[LocationTags] = frozenset()

    @property
    def code(self) -> Optional[int]:
        return LOCATION_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


class StardewLocationCollector(Protocol):
    def __call__(self, name: str, code: Optional[int], region: str) -> None:
        raise NotImplementedError


def load_location_csv() -> List[LocationData]:
    locations = []
    with open(world_folder + "/data/locations.csv") as file:
        reader = csv.DictReader(file)
        for location in reader:
            locations.append(LocationData(int(location["id"]) if location["id"] else None,
                                          location["region"],
                                          location["name"],
                                          frozenset(LocationTags[group] for group in location["tags"].split(",") if group)))
    return locations


events_locations = [
    LocationData(None, "Stardew Valley", "Succeed Grandpa's Evaluation"),
    LocationData(None, "Community Center", "Complete Community Center"),
    LocationData(None, "The Mines - Floor 120", "Reach the Bottom of The Mines"),
    LocationData(None, "Skull Cavern", "Complete Quest Cryptic Note"),
    LocationData(None, "Stardew Valley", "Summer"),
    LocationData(None, "Stardew Valley", "Fall"),
    LocationData(None, "Stardew Valley", "Winter"),
    LocationData(None, "Stardew Valley", "Year Two"),
]

all_locations = load_location_csv() + events_locations
location_table: Dict[str, LocationData] = {location.name: location for location in all_locations}
locations_by_tag: Dict[LocationTags, List[LocationData]] = {}


def initialize_groups():
    for location in all_locations:
        for tag in location.tags:
            location_group = locations_by_tag.get(tag, list())
            location_group.append(location)
            locations_by_tag[tag] = location_group


initialize_groups()


def extend_help_wanted_quests(randomized_locations: list[LocationData], desired_number_of_quests: int):
    for i in range(0, desired_number_of_quests):
        batch = i // 7
        index_this_batch = i % 7
        if index_this_batch < 4:
            randomized_locations.append(location_table[f"Help Wanted: Item Delivery {(batch * 4) + index_this_batch + 1}"])
        elif index_this_batch == 4:
            randomized_locations.append(location_table[f"Help Wanted: Fishing {batch + 1}"])
        elif index_this_batch == 5:
            randomized_locations.append(location_table[f"Help Wanted: Slay Monsters {batch + 1}"])
        elif index_this_batch == 6:
            randomized_locations.append(location_table[f"Help Wanted: Gathering {batch + 1}"])


def create_locations(location_collector: StardewLocationCollector, world_options: options.StardewOptions):
    randomized_locations = []

    randomized_locations.extend(locations_by_tag[LocationTags.MANDATORY])

    if not world_options[options.BackpackProgression] == options.BackpackProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.BACKPACK])

    if not world_options[options.ToolProgression] == options.ToolProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.TOOL_UPGRADE])

    if not world_options[options.TheMinesElevatorsProgression] == options.TheMinesElevatorsProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.THE_MINES_ELEVATOR])

    if not world_options[options.SkillProgression] == options.SkillProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.SKILL_LEVEL])

    if not world_options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.BUILDING_BLUEPRINT])

    if not world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_disabled:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE_VICTORY])

    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        randomized_locations.extend(locations_by_tag[LocationTags.ARCADE_MACHINE])

    extend_help_wanted_quests(randomized_locations, world_options[options.HelpWantedLocations])

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)
