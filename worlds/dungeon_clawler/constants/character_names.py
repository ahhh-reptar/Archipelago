from typing import List

from .item_flags import ItemFlags


class CharacterData:
    name: str
    good_item_flags: List[str]

    def __init__(self, name: str, good_item_flags: List[str]):
        self.name = name
        self.good_item_flags = good_item_flags
        all_characters.append(self)


all_characters: List[CharacterData] = []


class Character:
    sir_bunalot = CharacterData("Sir Bunalot", [ItemFlags.damage])
    scrappy = CharacterData("Scrappy", [ItemFlags.metal])
    felina = CharacterData("Felina", [ItemFlags.pets, ItemFlags.strength])
    count_clawcula = CharacterData("Count Clawcula", [ItemFlags.damage])
    dolly = CharacterData("Dolly", [ItemFlags.self_damage])
    benny_beaver = CharacterData("Benny Beaver", [ItemFlags.wood, ItemFlags.strength])
    bernie = CharacterData("Bernie", [ItemFlags.coins, ItemFlags.damage])
    squiddy = CharacterData("Squiddy", [ItemFlags.water])
    garbage_greg = CharacterData("Garbage Greg", [ItemFlags.more_items])
    anne_bunny = CharacterData("Anne Bunny", [ItemFlags.less_items])
    hare_l_quinn = CharacterData("Hare L. Quinn", [ItemFlags.damage, ItemFlags.less_items, ItemFlags.metal])
    chief_bunner = CharacterData("Chief Bunner", [ItemFlags.block])
    cuddline_floofington = CharacterData("Cuddline Floofington", [ItemFlags.fluff])
