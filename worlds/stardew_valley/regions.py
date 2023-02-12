from dataclasses import dataclass, field
from enum import IntFlag
from random import Random
from typing import Iterable, Dict, Protocol, Optional, List, Tuple

from BaseClasses import Region, Entrance
from . import options
from .options import StardewOptions


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0b0
    PELICAN_TOWN = 0b11111
    NON_PROGRESSION = 0b11110
    BUILDINGS = 0b11100
    EVERYTHING = 0b11000
    CHAOS = 0b10000


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    reverse: Optional[str] = None
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED


stardew_valley_regions = [
    RegionData("Menu", ["To Stardew Valley"]),
    RegionData("Stardew Valley", ["To Farmhouse"]),
    RegionData("Farmhouse", ["Outside To Farm", "Downstairs To Cellar"]),
    RegionData("Cellar", []),
    RegionData("Farm", ["Farm To Backwoods", "Farm To Bus Stop", "Farm To Forest", "Enter Farmcave", "Enter Greenhouse",
                        "Use Desert Obelisk", "Use Island Obelisk"]),
    RegionData("Backwoods", ["Backwoods To Mountain"]),
    RegionData("Bus Stop", ["Bus Stop To Town", "Take Bus To Desert", "Bus Stop To Tunnel Entrance"]),
    RegionData("Forest", ["Forest To Town", "Enter Secret Woods", "Enter Wizard Tower", "Enter Marnie's Ranch",
                          "Enter Leah's Cottage", "Forest To Sewers"]),
    RegionData("Farmcave", []),
    RegionData("Greenhouse", []),
    RegionData("Mountain", ["Mountain to Railroad", "Enter Tent", "Enter Carpenter Shop", "Enter The Mines",
                            "Enter Quarry", "Enter Adventurer's Guild", "Mountain To Town"]),
    RegionData("Tunnel Entrance", ["Enter Tunnel"]),
    RegionData("Tunnel", []),
    RegionData("Town", ["Town to Community Center", "Town To Beach", "Town to Hospital",
                        "Town to Pierre's General Store", "Town to Saloon", "Town to Alex's House", "Town to Mayor's Manor",
                        "Town to Sam's House", "Town to Haley's House", "Town To Sewers", "Town to Clint's Blacksmith", "Town to Museum",
                        "Town to JojaMart"], RandomizationFlag.PELICAN_TOWN),
    RegionData("Beach", ["Enter Willy's Fish Shop", "Enter Elliott's House", "Enter Tide Pools"]),
    RegionData("Railroad", ["Enter Bathhouse Entrance", "Enter Witch Warp Cave"]),  # "Enter Perfection Cutscene Area"
    RegionData("Marnie's Ranch", []),
    RegionData("Leah's Cottage", []),
    RegionData("Sewers", ["Enter Mutant Bug Lair"]),
    RegionData("Mutant Bug Lair", []),
    RegionData("Wizard Tower", ["Enter Wizard Basement"]),
    RegionData("Wizard Basement", []),
    RegionData("Tent", []),
    RegionData("Carpenter Shop", ["Enter Sebastian's Room"]),
    RegionData("Sebastian's Room", []),
    RegionData("Adventurer's Guild", []),
    RegionData("Community Center",
               ["Access Crafts Room", "Access Pantry", "Access Fish Tank", "Access Boiler Room", "Access Bulletin Board",
                "Access Vault"], RandomizationFlag.PELICAN_TOWN),
    RegionData("Crafts Room", []),
    RegionData("Pantry", []),
    RegionData("Fish Tank", []),
    RegionData("Boiler Room", []),
    RegionData("Bulletin Board", []),
    RegionData("Vault", []),
    RegionData("Hospital", ["Enter Harvey's Room"], RandomizationFlag.PELICAN_TOWN),
    RegionData("Harvey's Room", []),
    RegionData("Pierre's General Store", ["Enter Sunroom"], RandomizationFlag.PELICAN_TOWN),
    RegionData("Sunroom", []),
    RegionData("Saloon", ["Play Journey of the Prairie King", "Play Junimo Kart"], RandomizationFlag.PELICAN_TOWN),
    RegionData("Alex's House", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Mayor's Manor", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Sam's House", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Haley's House", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Clint's Blacksmith", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Museum", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("JojaMart", [], RandomizationFlag.PELICAN_TOWN),
    RegionData("Willy's Fish Shop", []),
    RegionData("Elliott's House", []),
    RegionData("Tide Pools", []),
    RegionData("Bathhouse Entrance", ["Enter Locker Room"]),
    RegionData("Locker Room", ["Enter Public Bath"]),
    RegionData("Public Bath", []),
    RegionData("Witch Warp Cave", ["Enter Witch's Swamp"]),
    RegionData("Witch's Swamp", []),
    RegionData("Quarry", ["Enter Quarry Mine Entrance"]),
    RegionData("Quarry Mine Entrance", ["Enter Quarry Mine"]),
    RegionData("Quarry Mine", []),
    RegionData("Secret Woods", []),
    RegionData("The Desert", ["Enter Skull Cavern Entrance"]),
    RegionData("Skull Cavern Entrance", ["Enter Skull Cavern"]),
    RegionData("Skull Cavern", []),
    RegionData("Ginger Island", []),
    RegionData("JotPK World 1", ["Reach JotPK World 2"]),
    RegionData("JotPK World 2", ["Reach JotPK World 3"]),
    RegionData("JotPK World 3", []),
    RegionData("Junimo Kart 1", ["Reach Junimo Kart 2"]),
    RegionData("Junimo Kart 2", ["Reach Junimo Kart 3"]),
    RegionData("Junimo Kart 3", []),
    RegionData("The Mines", ["Dig to The Mines - Floor 5", "Dig to The Mines - Floor 10", "Dig to The Mines - Floor 15",
                             "Dig to The Mines - Floor 20", "Dig to The Mines - Floor 25", "Dig to The Mines - Floor 30",
                             "Dig to The Mines - Floor 35", "Dig to The Mines - Floor 40", "Dig to The Mines - Floor 45",
                             "Dig to The Mines - Floor 50", "Dig to The Mines - Floor 55", "Dig to The Mines - Floor 60",
                             "Dig to The Mines - Floor 65", "Dig to The Mines - Floor 70", "Dig to The Mines - Floor 75",
                             "Dig to The Mines - Floor 80", "Dig to The Mines - Floor 85", "Dig to The Mines - Floor 90",
                             "Dig to The Mines - Floor 95", "Dig to The Mines - Floor 100", "Dig to The Mines - Floor 105",
                             "Dig to The Mines - Floor 110", "Dig to The Mines - Floor 115", "Dig to The Mines - Floor 120"]),
    RegionData("The Mines - Floor 5", []),
    RegionData("The Mines - Floor 10", []),
    RegionData("The Mines - Floor 15", []),
    RegionData("The Mines - Floor 20", []),
    RegionData("The Mines - Floor 25", []),
    RegionData("The Mines - Floor 30", []),
    RegionData("The Mines - Floor 35", []),
    RegionData("The Mines - Floor 40", []),
    RegionData("The Mines - Floor 45", []),
    RegionData("The Mines - Floor 50", []),
    RegionData("The Mines - Floor 55", []),
    RegionData("The Mines - Floor 60", []),
    RegionData("The Mines - Floor 65", []),
    RegionData("The Mines - Floor 70", []),
    RegionData("The Mines - Floor 75", []),
    RegionData("The Mines - Floor 80", []),
    RegionData("The Mines - Floor 85", []),
    RegionData("The Mines - Floor 90", []),
    RegionData("The Mines - Floor 95", []),
    RegionData("The Mines - Floor 100", []),
    RegionData("The Mines - Floor 105", []),
    RegionData("The Mines - Floor 110", []),
    RegionData("The Mines - Floor 115", []),
    RegionData("The Mines - Floor 120", []),
]

# Exists and where they lead
mandatory_connections = [
    ConnectionData("To Stardew Valley", "Stardew Valley"),
    ConnectionData("To Farmhouse", "Farmhouse"),
    ConnectionData("Outside To Farm", "Farm"),
    ConnectionData("Downstairs To Cellar", "Cellar"),
    ConnectionData("Farm To Backwoods", "Backwoods"),
    ConnectionData("Farm To Bus Stop", "Bus Stop"),
    ConnectionData("Farm To Forest", "Forest"),
    ConnectionData("Enter Farmcave", "Farmcave"),
    ConnectionData("Enter Greenhouse", "Greenhouse"),
    ConnectionData("Use Desert Obelisk", "The Desert"),
    ConnectionData("Use Island Obelisk", "Ginger Island"),
    ConnectionData("Backwoods To Mountain", "Mountain"),
    ConnectionData("Bus Stop To Town", "Town"),
    ConnectionData("Bus Stop To Tunnel Entrance", "Tunnel Entrance"),
    ConnectionData("Take Bus To Desert", "The Desert"),
    ConnectionData("Enter Tunnel", "Tunnel"),
    ConnectionData("Forest To Town", "Town"),
    ConnectionData("Enter Wizard Tower", "Wizard Tower"),
    ConnectionData("Enter Wizard Basement", "Wizard Basement"),
    ConnectionData("Enter Marnie's Ranch", "Marnie's Ranch"),
    ConnectionData("Enter Leah's Cottage", "Leah's Cottage"),
    ConnectionData("Enter Secret Woods", "Secret Woods"),
    ConnectionData("Forest To Sewers", "Sewers"),
    ConnectionData("Town To Sewers", "Sewers"),
    ConnectionData("Enter Mutant Bug Lair", "Mutant Bug Lair"),
    ConnectionData("Mountain to Railroad", "Railroad"),
    ConnectionData("Enter Tent", "Tent"),
    ConnectionData("Enter Carpenter Shop", "Carpenter Shop"),
    ConnectionData("Enter Sebastian's Room", "Sebastian's Room"),
    ConnectionData("Enter Adventurer's Guild", "Adventurer's Guild"),
    ConnectionData("Enter Quarry", "Quarry"),
    ConnectionData("Enter Quarry Mine Entrance", "Quarry Mine Entrance"),
    ConnectionData("Enter Quarry Mine", "Quarry Mine"),
    ConnectionData("Mountain To Town", "Town"),
    ConnectionData("Town to Community Center", "Community Center", "Community Center to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Access Crafts Room", "Crafts Room"),
    ConnectionData("Access Pantry", "Pantry"),
    ConnectionData("Access Fish Tank", "Fish Tank"),
    ConnectionData("Access Boiler Room", "Boiler Room"),
    ConnectionData("Access Bulletin Board", "Bulletin Board"),
    ConnectionData("Access Vault", "Vault"),
    ConnectionData("Town to Hospital", "Hospital", "Exit Hospital", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Enter Harvey's Room", "Harvey's Room"),
    ConnectionData("Town to Pierre's General Store", "Pierre's General Store", "Pierre's General Store to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Enter Sunroom", "Sunroom"),
    ConnectionData("Town to Clint's Blacksmith", "Clint's Blacksmith", "Clint's Blacksmith to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Saloon", "Saloon", "Exit Saloon", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Play Journey of the Prairie King", "JotPK World 1"),
    ConnectionData("Reach JotPK World 2", "JotPK World 2"),
    ConnectionData("Reach JotPK World 3", "JotPK World 3"),
    ConnectionData("Play Junimo Kart", "Junimo Kart 1"),
    ConnectionData("Reach Junimo Kart 2", "Junimo Kart 2"),
    ConnectionData("Reach Junimo Kart 3", "Junimo Kart 3"),
    ConnectionData("Town to Sam's House", "Sam's House", "Sam's House to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Haley's House", "Haley's House", "Haley's House to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Mayor's Manor", "Mayor's Manor", "Mayor's Manor to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Alex's House", "Alex's House", "Alex's House to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to Museum", "Museum", "Museum to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town to JojaMart", "JojaMart", "JojaMart to Town", RandomizationFlag.PELICAN_TOWN),
    ConnectionData("Town To Beach", "Beach"),
    ConnectionData("Enter Elliott's House", "Elliott's House"),
    ConnectionData("Enter Willy's Fish Shop", "Willy's Fish Shop"),
    ConnectionData("Enter Tide Pools", "Tide Pools"),
    ConnectionData("Enter The Mines", "The Mines"),
    ConnectionData("Dig to The Mines - Floor 5", "The Mines - Floor 5"),
    ConnectionData("Dig to The Mines - Floor 10", "The Mines - Floor 10"),
    ConnectionData("Dig to The Mines - Floor 15", "The Mines - Floor 15"),
    ConnectionData("Dig to The Mines - Floor 20", "The Mines - Floor 20"),
    ConnectionData("Dig to The Mines - Floor 25", "The Mines - Floor 25"),
    ConnectionData("Dig to The Mines - Floor 30", "The Mines - Floor 30"),
    ConnectionData("Dig to The Mines - Floor 35", "The Mines - Floor 35"),
    ConnectionData("Dig to The Mines - Floor 40", "The Mines - Floor 40"),
    ConnectionData("Dig to The Mines - Floor 45", "The Mines - Floor 45"),
    ConnectionData("Dig to The Mines - Floor 50", "The Mines - Floor 50"),
    ConnectionData("Dig to The Mines - Floor 55", "The Mines - Floor 55"),
    ConnectionData("Dig to The Mines - Floor 60", "The Mines - Floor 60"),
    ConnectionData("Dig to The Mines - Floor 65", "The Mines - Floor 65"),
    ConnectionData("Dig to The Mines - Floor 70", "The Mines - Floor 70"),
    ConnectionData("Dig to The Mines - Floor 75", "The Mines - Floor 75"),
    ConnectionData("Dig to The Mines - Floor 80", "The Mines - Floor 80"),
    ConnectionData("Dig to The Mines - Floor 85", "The Mines - Floor 85"),
    ConnectionData("Dig to The Mines - Floor 90", "The Mines - Floor 90"),
    ConnectionData("Dig to The Mines - Floor 95", "The Mines - Floor 95"),
    ConnectionData("Dig to The Mines - Floor 100", "The Mines - Floor 100"),
    ConnectionData("Dig to The Mines - Floor 105", "The Mines - Floor 105"),
    ConnectionData("Dig to The Mines - Floor 110", "The Mines - Floor 110"),
    ConnectionData("Dig to The Mines - Floor 115", "The Mines - Floor 115"),
    ConnectionData("Dig to The Mines - Floor 120", "The Mines - Floor 120"),
    ConnectionData("Enter Skull Cavern Entrance", "Skull Cavern Entrance"),
    ConnectionData("Enter Skull Cavern", "Skull Cavern"),
    ConnectionData("Enter Witch Warp Cave", "Witch Warp Cave"),
    ConnectionData("Enter Witch's Swamp", "Witch's Swamp"),
    ConnectionData("Enter Bathhouse Entrance", "Bathhouse Entrance"),
    ConnectionData("Enter Locker Room", "Locker Room"),
    ConnectionData("Enter Public Bath", "Public Bath"),
]


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewOptions) -> Tuple[Iterable[Region], Dict[str, str]]:
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in stardew_valley_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    connections, randomized_data = randomize_connections(random, world_options)

    for connection in connections:
        if connection.name not in entrances:
            continue
        entrances[connection.name].connect(regions[connection.destination])

    return regions.values(), randomized_data


def randomize_connections(random: Random, world_options: StardewOptions) -> Tuple[List[ConnectionData], Dict[str, str]]:
    connections_to_randomize = []
    if world_options[options.EntranceRandomization] == options.EntranceRandomization.option_pelican_town:
        connections_to_randomize = [connection for connection in mandatory_connections if RandomizationFlag.PELICAN_TOWN in connection.flag]
    random.shuffle(connections_to_randomize)

    destination_pool = list(connections_to_randomize)
    random.shuffle(destination_pool)

    randomized_connections = []
    randomized_data = {}
    for connection in connections_to_randomize:
        destination = destination_pool.pop()
        randomized_connections.append(ConnectionData(connection.name, destination.destination, destination.reverse))
        randomized_data[connection.name] = destination.name
        randomized_data[destination.reverse] = connection.reverse

    return mandatory_connections, randomized_data
