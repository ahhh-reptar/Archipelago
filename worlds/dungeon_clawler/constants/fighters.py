from typing import List

from .item_flags import ItemFlags


class FighterData:
    name: str
    good_item_flags: List[str]

    def __init__(self, name: str, good_item_flags: List[str]):
        self.name = name
        self.good_item_flags = good_item_flags
        all_fighters.append(self)


all_fighters: List[FighterData] = []


class Fighter:
    sir_bunalot = FighterData("Sir Bunalot", [ItemFlags.damage])
    scrappy = FighterData("Scrappy", [ItemFlags.metal])
    felina = FighterData("Felina", [ItemFlags.pets, ItemFlags.strength])
    count_clawcula = FighterData("Count Clawcula", [ItemFlags.damage])
    dolly = FighterData("Dolly", [ItemFlags.self_damage])
    benny_beaver = FighterData("Benny Beaver", [ItemFlags.wood, ItemFlags.strength])
    bernie = FighterData("Bernie", [ItemFlags.coins, ItemFlags.damage])
    squiddy = FighterData("Squiddy", [ItemFlags.water])
    garbage_greg = FighterData("Garbage Greg", [ItemFlags.more_items])
    anne_bunny = FighterData("Anne Bunny", [ItemFlags.less_items])
    hare_l_quinn = FighterData("Hare L. Quinn", [ItemFlags.damage, ItemFlags.metal])
    chief_bunner = FighterData("Chief Bunner", [ItemFlags.block])
    cuddline_floofington = FighterData("Cuddline Floofington", [ItemFlags.fluff])
