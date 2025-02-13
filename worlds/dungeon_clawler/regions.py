from typing import List, Union

from BaseClasses import Entrance, MultiWorld, Region
from .constants.difficulties import all_difficulties
from .locations import floor_region_name, beat_floor_entrance_name
from .options import DungeonClawlerOptions


def create_regions(multiworld: MultiWorld, player: int, world_options: DungeonClawlerOptions):
    new_region(multiworld, player, "Menu", None, [f"Start {difficulty} Run" for difficulty in all_difficulties])

    for i in range(1, 51):
        for difficulty in all_difficulties:
            if i == 1:
                parent_entrance = f"Start {difficulty} Run"
            else:
                parent_entrance = beat_floor_entrance_name(i - 1, difficulty)
            if i < 50:
                exits = [beat_floor_entrance_name(i, difficulty)]
            else:
                exits = []
            new_region(multiworld, player, floor_region_name(i, difficulty), parent_entrance, exits)


def new_region(multiworld: MultiWorld, player: int, region_name: str, parent_entrances: Union[None, str, List[str]], exits: Union[str, List[str]]) -> Region:
    region = Region(region_name, player, multiworld)

    if isinstance(exits, str):
        exits = [exits]
    region.exits = [Entrance(player, exit_name, region) for exit_name in exits]

    multiworld.regions.append(region)

    if parent_entrances is None:
        return region
    if isinstance(parent_entrances, str):
        parent_entrances = [parent_entrances]
    for parent_entrance in parent_entrances:
        multiworld.get_entrance(parent_entrance, player).connect(region)

    return region
