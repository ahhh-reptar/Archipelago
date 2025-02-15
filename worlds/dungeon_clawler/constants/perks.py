from typing import List

from .item_flags import ItemFlags


max_perk_stack = 4


class PerkData:
    name: str
    max_stack: int
    flags: List[str]

    def __init__(self, name: str, max_stack: int, flags: List[str]):
        self.name = name
        self.max_stack = max_stack
        self.flags = flags
        all_perk_items.append(self)


all_perk_items: List[PerkData] = []


class Perk:
    blockmaster = PerkData("Blockmaster", 4, [ItemFlags.block])
    bulwark = PerkData("Bulwark", 10, [ItemFlags.block])
    deflation = PerkData("Deflation", 10, [ItemFlags.coins])
    hoarder = PerkData("Hoarder", 10, [ItemFlags.more_items, ItemFlags.fluff])
    picky = PerkData("Picky", 1, [ItemFlags.less_items])
    pin_cushion = PerkData("Pin Cushion", 10, [ItemFlags.more_items, ItemFlags.healing])
    alchemist_coupon = PerkData("Alchemist Coupon", 4, [ItemFlags.coins, ItemFlags.magnetism])
    bargain = PerkData("Bargain", 4, [ItemFlags.coins])
    blacksmith_coupon = PerkData("Blacksmith Coupon", 4, [ItemFlags.coins])
    golden_armor = PerkData("Golden Armor", 5, [ItemFlags.coins])
    reroll_coupon = PerkData("Reroll Coupon", 4, [ItemFlags.coins])
    savings_account = PerkData("Savings Account", 5, [ItemFlags.coins])
    shredder_coupon = PerkData("Shredder Coupon", 4, [ItemFlags.coins, ItemFlags.less_items])
    thief = PerkData("Thief", 4, [ItemFlags.coins])
    critical_strength = PerkData("Critical Strength", 1, [ItemFlags.critical_hits, ItemFlags.self_damage])
    deep_cuts = PerkData("Deep Cuts", 1, [ItemFlags.critical_hits])
    enraged = PerkData("Enraged", 1, [ItemFlags.critical_hits, ItemFlags.self_damage])
    hard_hits = PerkData("Hard Hits", 10, [ItemFlags.critical_hits])
    junk_jet = PerkData("Junk Jet", 10, [ItemFlags.more_items, ItemFlags.indirect_damage])
    catsuit = PerkData("Catsuit", 10, [ItemFlags.avoidance])
    dodgy = PerkData("Dodgy", 10, [ItemFlags.avoidance, ItemFlags.indirect_damage])
    cuddly = PerkData("Cuddly", 10, [ItemFlags.more_items, ItemFlags.water, ItemFlags.fluff])
    fluffy = PerkData("Fluffy", 10, [ItemFlags.more_items, ItemFlags.water, ItemFlags.fluff])
    swamp = PerkData("Swamp", 5, [ItemFlags.water, ItemFlags.fluff])
    critical_healing = PerkData("Critical Healing", 10, [ItemFlags.healing, ItemFlags.critical_hits])
    giantism = PerkData("Giantism", 10, [ItemFlags.self_damage])
    resilient = PerkData("Resilient", 10, [ItemFlags.healing])
    vampire_fangs = PerkData("Vampire Fangs", 10, [ItemFlags.healing])
    catnip = PerkData("Catnip", 10, [ItemFlags.pets])
    contagious_venom = PerkData("Contagious Venom", 1, [ItemFlags.poison])
    poisonous_weapons = PerkData("Poisonous Weapons", 10, [ItemFlags.poison])
    vaccine = PerkData("Vaccine", 1, [ItemFlags.avoidance])
    golden_tentacle = PerkData("Golden Tentacle", 1, [ItemFlags.coins])
    greedy = PerkData("Greedy", 2, [ItemFlags.coins])
    lucky = PerkData("Lucky", 1, [])
    magic_mirror = PerkData("Magic Mirror", 1, [ItemFlags.less_items])
    magnetism = PerkData("Magnetism", 10, [ItemFlags.magnetism, ItemFlags.metal])
    weaklings = PerkData("Weaklings", 1, [])
    hedgehog = PerkData("Hedgehog", 10, [ItemFlags.indirect_damage])
    spikes = PerkData("Spikes", 10, [ItemFlags.indirect_damage])
    berserker = PerkData("Berserker", 10, [ItemFlags.strength, ItemFlags.self_damage])
    minimalist = PerkData("Minimalist", 10, [ItemFlags.less_items])
    natural_strength = PerkData("Natural Strength", 10, [ItemFlags.strength])
