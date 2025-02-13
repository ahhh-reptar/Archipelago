from typing import List

from .ItemFlags import ItemFlags

number_small_items = 5
number_big_items = 2
number_buff_items = 1


all_combat_items = []


class CombatItemData:
    name: str
    max_stack: int
    flags: List[str]
    upgradeable: bool

    def __init__(self, name: str, max_stack: int, flags: List[str], upgradeable: bool = True):
        self.name = name
        self.max_stack = max_stack
        self.flags = flags
        self.upgradeable = upgradeable
        all_combat_items.append(self)


class CombatItem:
    big_shield = CombatItemData("Big Shield", number_big_items, [ItemFlags.block])
    body_armor = CombatItemData("Body Armor", number_buff_items, [ItemFlags.block, ItemFlags.buff])
    gauntlet = CombatItemData("Gauntlet", number_buff_items, [ItemFlags.block, ItemFlags.buff])
    helmet = CombatItemData("Helmet", number_buff_items, [ItemFlags.block])
    holy_shield = CombatItemData("Holy Shield", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff], False)
    metal_shield = CombatItemData("Metal Shield", number_big_items, [ItemFlags.block, ItemFlags.magnetism])
    morning_star = CombatItemData("Morning Star", number_big_items, [ItemFlags.block, ItemFlags.damage])
    plastic_shield = CombatItemData("Plastic Shield", number_big_items, [ItemFlags.block, ItemFlags.degrades])
    small_shield = CombatItemData("Small Shield", number_small_items, [ItemFlags.block])
    tower_shield = CombatItemData("Tower Shield", number_buff_items, [ItemFlags.block])
    vitamin_pill = CombatItemData("Vitamin Pill", number_buff_items, [ItemFlags.block, ItemFlags.strength])
    strength = CombatItemData("Warhammer", number_big_items, [ItemFlags.block, ItemFlags.damage])
    wood_oil = CombatItemData("Wood Oil", number_buff_items, [ItemFlags.block])
    brass_knuckle = CombatItemData("Brass Knuckle", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff])
    fortune_cookie = CombatItemData("Fortune Cookie", number_buff_items, [ItemFlags.buff])
    hand_mirror = CombatItemData("Hand Mirror", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff], False)
    pearl = CombatItemData("Pearl", number_buff_items, [ItemFlags.buff])
    spikey_shield = CombatItemData("Spikey Shield", number_big_items, [ItemFlags.block, ItemFlags.indirect_damage, ItemFlags.buff])
    harpoon = CombatItemData("Harpoon", number_buff_items, [ItemFlags.less_items, ItemFlags.buff], False)
    magnet_claw = CombatItemData("Magnet Claw", number_buff_items, [ItemFlags.magnetism, ItemFlags.buff], False)
    tentacle_claw = CombatItemData("Tentacle Claw", number_buff_items, [ItemFlags.water, ItemFlags.more_items, ItemFlags.buff], False)
    credit_card = CombatItemData("Credit Card", number_buff_items, [ItemFlags.damage, ItemFlags.coins])
    gold_dagger = CombatItemData("Gold Dagger", number_big_items, [ItemFlags.damage, ItemFlags.coins])
    hand_of_midas = CombatItemData("Hand of Midas", number_buff_items, [ItemFlags.coins])
    piggy_bank = CombatItemData("Piggy Bank", number_big_items, [ItemFlags.coins])
    eyepatch = CombatItemData("Eyepatch", number_buff_items, [ItemFlags.critical_hits])
    sickle = CombatItemData("Sickle", number_big_items, [ItemFlags.damage, ItemFlags.critical_hits])
    battle_axe = CombatItemData("Battle Axe", number_big_items, [ItemFlags.damage])
    dagger = CombatItemData("Dagger", number_small_items, [ItemFlags.damage])
    dark_sword = CombatItemData("Dark Sword", number_big_items, [ItemFlags.damage, ItemFlags.self_damage])
    double_bladed_sword = CombatItemData("Double Bladed Sword", number_big_items, [ItemFlags.damage, ItemFlags.self_damage])
    great_sword = CombatItemData("Great Sword", number_big_items, [ItemFlags.damage])
    lucky_stick = CombatItemData("Lucky Stick", number_big_items, [ItemFlags.damage])
    plastic_knife = CombatItemData("Plastic Knife", number_big_items, [ItemFlags.damage])
    recycling_bin = CombatItemData("Recycling Bin", number_buff_items, [ItemFlags.damage, ItemFlags.more_items])
    small_sword = CombatItemData("Small Sword", number_big_items, [ItemFlags.damage])
    syringe = CombatItemData("Syringe", number_buff_items, [ItemFlags.damage])
    ticking_bomb = CombatItemData("Ticking Bomb", number_buff_items, [ItemFlags.indirect_damage, ItemFlags.buff])
    whetstone = CombatItemData("Whetstone", number_buff_items, [ItemFlags.damage])
    honey_ball = CombatItemData("Honey Ball", number_small_items, [ItemFlags.water], False)
    spike = CombatItemData("Spike", number_small_items, [], False)
    meli_bomb = CombatItemData("Meli-Bomb", number_big_items, [ItemFlags.added_by_enemies], False)
    poisonous_spore = CombatItemData("Poisonous Spore", number_big_items, [ItemFlags.added_by_enemies], False)
    healing_flask = CombatItemData("Healing Flask", number_small_items, [ItemFlags.healing])
    magic_wand = CombatItemData("Magic Wand", number_big_items, [ItemFlags.healing])
    teddy = CombatItemData("Teddy", number_big_items, [ItemFlags.healing, ItemFlags.fluff])
    thermometer = CombatItemData("Thermometer", number_small_items, [ItemFlags.self_damage])
    felinas_cat_carrier = CombatItemData("Felinas Cat Carrier", number_buff_items, [ItemFlags.pets, ItemFlags.buff], False)
    antidote = CombatItemData("Antidote", number_buff_items, [ItemFlags.avoidance], False)
    poison_dagger = CombatItemData("Poison Dagger", number_big_items, [ItemFlags.damage, ItemFlags.poison])
    poison_flask = CombatItemData("Poison Flask", number_big_items, [ItemFlags.poison])
    poison_grenade = CombatItemData("Poison Grenade", number_big_items, [ItemFlags.poison])
    shuriken = CombatItemData("Shuriken", number_big_items, [ItemFlags.poison])
    cactus = CombatItemData("Cactus", number_big_items, [ItemFlags.self_damage, ItemFlags.block])
    stressball_spikes = CombatItemData("Stressball Spikes", number_small_items, [ItemFlags.self_damage, ItemFlags.added_by_other], False)
    spiky_stressball = CombatItemData("Spiky Stressball", number_big_items, [ItemFlags.strength, ItemFlags.self_damage])
    glass_cleaner = CombatItemData("Glass Cleaner", number_buff_items, [ItemFlags.damage], False)
    heat_gun = CombatItemData("Heat Gun", number_buff_items, [ItemFlags.more_items])
    magnet = CombatItemData("Magnet", number_big_items, [ItemFlags.magnetism])
    amulet_of_strength = CombatItemData("Amulet of Strength", number_buff_items, [ItemFlags.strength])
    energy_drink = CombatItemData("Energy Drink", number_buff_items, [ItemFlags.block, ItemFlags.strength])
    paperclip = CombatItemData("Paperclip", number_big_items, [ItemFlags.strength])
    ring_of_strength = CombatItemData("Ring of Strength", number_buff_items, [ItemFlags.strength])
    strength_potion = CombatItemData("Strength Potion", number_buff_items, [ItemFlags.strength])
    wooden_bracelet = CombatItemData("Wooden Bracelet", number_big_items, [ItemFlags.strength, ItemFlags.block])
    battery = CombatItemData("Battery", number_buff_items, [ItemFlags.damage, ItemFlags.water])
    lava_bathbomb = CombatItemData("Lava Bathbomb", number_buff_items, [ItemFlags.more_items, ItemFlags.water, CombatItemFlags.fluff], False)
    toy_piranha = CombatItemData("Toy Piranha", number_buff_items, [CombatItemFlags.water, CombatItemFlags.damage, CombatItemFlags.fluff])
    poison_bathbomb = CombatItemData("Poison Bathbomb", number_buff_items, [CombatItemFlags.more_items, CombatItemFlags.water, CombatItemFlags.fluff], False)
    sponge = CombatItemData("Sponge", number_big_items, [CombatItemFlags.damage, CombatItemFlags.water])
    treasure_chest = CombatItemData("Treasure Chest", number_buff_items, [CombatItemFlags.damage, CombatItemFlags.water])
    open_treasure_chest = CombatItemData("Open Treasure Chest", number_big_items, [CombatItemFlags.damage, CombatItemFlags.water, CombatItemFlags.added_by_other])
    water_bottle = CombatItemData("Water Bottle", number_buff_items, [CombatItemFlags.water, CombatItemFlags.more_items], False)
    waterpistol = CombatItemData("Waterpistol", number_buff_items, [CombatItemFlags.damage, CombatItemFlags.water], False)
    healing_potion = CombatItemData("Healing Potion", number_big_items, [], False)
