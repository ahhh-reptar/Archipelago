from typing import Iterable, Dict, Protocol

from BaseClasses import Region, Entrance


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


stardew_valley_regions = [
    ("Menu", ["To Stardew Valley"]),
    ("Stardew Valley",
     ["Enter Community Center", "Enter Pierre's General Store", "Enter The Mines", "Enter Clint's Blacksmith",
      "Enter Willy's Fish Shop", "Enter the Quarry", "Enter the Secret Woods", "Take the Bus to the Desert",
      "Use the Desert Obelisk", "Use the Island Obelisk", "Enter the Tide Pools", "Play Journey of the Prairie King",
      "Play Junimo Kart"]),
    ("Community Center",
     ["Access Crafts Room", "Access Pantry", "Access Fish Tank", "Access Boiler Room", "Access Bulletin Board",
      "Access Vault"]),
    ("Crafts Room", []),
    ("Pantry", []),
    ("Fish Tank", []),
    ("Boiler Room", []),
    ("Bulletin Board", []),
    ("Vault", []),
    ("Pierre's General Store", []),
    ("The Mines", ["Dig to The Mines - Floor 5", "Dig to The Mines - Floor 10", "Dig to The Mines - Floor 15",
                   "Dig to The Mines - Floor 20", "Dig to The Mines - Floor 25", "Dig to The Mines - Floor 30",
                   "Dig to The Mines - Floor 35", "Dig to The Mines - Floor 40", "Dig to The Mines - Floor 45",
                   "Dig to The Mines - Floor 50", "Dig to The Mines - Floor 55", "Dig to The Mines - Floor 60",
                   "Dig to The Mines - Floor 65", "Dig to The Mines - Floor 70", "Dig to The Mines - Floor 75",
                   "Dig to The Mines - Floor 80", "Dig to The Mines - Floor 85", "Dig to The Mines - Floor 90",
                   "Dig to The Mines - Floor 95", "Dig to The Mines - Floor 100", "Dig to The Mines - Floor 105",
                   "Dig to The Mines - Floor 110", "Dig to The Mines - Floor 115", "Dig to The Mines - Floor 120"]),
    ("The Mines - Floor 5", []),
    ("The Mines - Floor 10", []),
    ("The Mines - Floor 15", []),
    ("The Mines - Floor 20", []),
    ("The Mines - Floor 25", []),
    ("The Mines - Floor 30", []),
    ("The Mines - Floor 35", []),
    ("The Mines - Floor 40", []),
    ("The Mines - Floor 45", []),
    ("The Mines - Floor 50", []),
    ("The Mines - Floor 55", []),
    ("The Mines - Floor 60", []),
    ("The Mines - Floor 65", []),
    ("The Mines - Floor 70", []),
    ("The Mines - Floor 75", []),
    ("The Mines - Floor 80", []),
    ("The Mines - Floor 85", []),
    ("The Mines - Floor 90", []),
    ("The Mines - Floor 95", []),
    ("The Mines - Floor 100", []),
    ("The Mines - Floor 105", []),
    ("The Mines - Floor 110", []),
    ("The Mines - Floor 115", []),
    ("The Mines - Floor 120", []),
    ("Clint's Blacksmith", []),
    ("Willy's Fish Shop", []),
    ("Quarry", []),
    ("Secret Woods", []),
    ("The Desert", ["Enter the Skull Cavern"]),
    ("Skull Cavern", []),
    ("Ginger Island", []),
    ("Tide Pools", []),
    ("JotPK World 1", ["Reach JotPK World 2"]),
    ("JotPK World 2", ["Reach JotPK World 3"]),
    ("JotPK World 3", []),
    ("Junimo Kart 1", ["Reach Junimo Kart 2"]),
    ("Junimo Kart 2", ["Reach Junimo Kart 3"]),
    ("Junimo Kart 3", []),
]

# Exists and where they lead
mandatory_connections = [
    ("To Stardew Valley", "Stardew Valley"),
    ("Enter Community Center", "Community Center"),
    ("Access Crafts Room", "Crafts Room"),
    ("Access Pantry", "Pantry"),
    ("Access Fish Tank", "Fish Tank"),
    ("Access Boiler Room", "Boiler Room"),
    ("Access Bulletin Board", "Bulletin Board"),
    ("Access Vault", "Vault"),
    ("Enter Pierre's General Store", "Pierre's General Store"),
    ("Enter The Mines", "The Mines"),
    ("Dig to The Mines - Floor 5", "The Mines - Floor 5"),
    ("Dig to The Mines - Floor 10", "The Mines - Floor 10"),
    ("Dig to The Mines - Floor 15", "The Mines - Floor 15"),
    ("Dig to The Mines - Floor 20", "The Mines - Floor 20"),
    ("Dig to The Mines - Floor 25", "The Mines - Floor 25"),
    ("Dig to The Mines - Floor 30", "The Mines - Floor 30"),
    ("Dig to The Mines - Floor 35", "The Mines - Floor 35"),
    ("Dig to The Mines - Floor 40", "The Mines - Floor 40"),
    ("Dig to The Mines - Floor 45", "The Mines - Floor 45"),
    ("Dig to The Mines - Floor 50", "The Mines - Floor 50"),
    ("Dig to The Mines - Floor 55", "The Mines - Floor 55"),
    ("Dig to The Mines - Floor 60", "The Mines - Floor 60"),
    ("Dig to The Mines - Floor 65", "The Mines - Floor 65"),
    ("Dig to The Mines - Floor 70", "The Mines - Floor 70"),
    ("Dig to The Mines - Floor 75", "The Mines - Floor 75"),
    ("Dig to The Mines - Floor 80", "The Mines - Floor 80"),
    ("Dig to The Mines - Floor 85", "The Mines - Floor 85"),
    ("Dig to The Mines - Floor 90", "The Mines - Floor 90"),
    ("Dig to The Mines - Floor 95", "The Mines - Floor 95"),
    ("Dig to The Mines - Floor 100", "The Mines - Floor 100"),
    ("Dig to The Mines - Floor 105", "The Mines - Floor 105"),
    ("Dig to The Mines - Floor 110", "The Mines - Floor 110"),
    ("Dig to The Mines - Floor 115", "The Mines - Floor 115"),
    ("Dig to The Mines - Floor 120", "The Mines - Floor 120"),
    ("Enter Clint's Blacksmith", "Clint's Blacksmith"),
    ("Enter Willy's Fish Shop", "Willy's Fish Shop"),
    ("Enter the Quarry", "Quarry"),
    ("Enter the Secret Woods", "Secret Woods"),
    ("Take the Bus to the Desert", "The Desert"),
    ("Enter the Skull Cavern", "Skull Cavern"),
    ("Use the Desert Obelisk", "The Desert"),
    ("Use the Island Obelisk", "Ginger Island"),
    ("Enter the Tide Pools", "Tide Pools"),
    ("Play Journey of the Prairie King", "JotPK World 1"),
    ("Reach JotPK World 2", "JotPK World 2"),
    ("Reach JotPK World 3", "JotPK World 3"),
    ("Play Junimo Kart", "Junimo Kart 1"),
    ("Reach Junimo Kart 2", "Junimo Kart 2"),
    ("Reach Junimo Kart 3", "Junimo Kart 3"),
]


def create_regions(region_factory: RegionFactory) -> Iterable[Region]:
    regions: Dict[str: Region] = {region[0]: region_factory(*region) for region in stardew_valley_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    for connection in mandatory_connections:
        entrances[connection[0]].connect(regions[connection[1]])

    return regions.values()
