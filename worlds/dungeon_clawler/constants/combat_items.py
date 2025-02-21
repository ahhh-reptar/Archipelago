from typing import List, Dict

from .item_flags import ItemFlags

number_small_items = 4
number_big_items = 2
number_buff_items = 1


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
        combat_items_by_name[self.name] = self


all_combat_items: List[CombatItemData] = []
combat_items_by_name: Dict[str, CombatItemData] = {}


class CombatItem:
    big_shield = CombatItemData("Big Shield", number_big_items, [ItemFlags.block, ItemFlags.wood])
    body_armor = CombatItemData("Body Armor", number_buff_items, [ItemFlags.block, ItemFlags.buff, ItemFlags.metal])
    gauntlet = CombatItemData("Gauntlet", number_buff_items, [ItemFlags.block, ItemFlags.buff, ItemFlags.metal, ItemFlags.ethereal])
    helmet = CombatItemData("Helmet", number_buff_items, [ItemFlags.block, ItemFlags.metal, ItemFlags.ethereal])
    holy_shield = CombatItemData("Holy Shield", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff, ItemFlags.metal, ItemFlags.ethereal], False)
    metal_shield = CombatItemData("Metal Shield", number_big_items, [ItemFlags.block, ItemFlags.magnetism, ItemFlags.metal])
    morning_star = CombatItemData("Morning Star", number_big_items, [ItemFlags.block, ItemFlags.damage, ItemFlags.metal])
    plastic_shield = CombatItemData("Plastic Shield", number_big_items, [ItemFlags.block, ItemFlags.degrades])
    small_shield = CombatItemData("Small Shield", number_small_items, [ItemFlags.block, ItemFlags.wood])
    tower_shield = CombatItemData("Tower Shield", number_buff_items, [ItemFlags.block, ItemFlags.wood])
    vitamin_pill = CombatItemData("Vitamin Pill", number_buff_items, [ItemFlags.block, ItemFlags.strength])
    strength = CombatItemData("Warhammer", number_big_items, [ItemFlags.block, ItemFlags.damage])
    wood_oil = CombatItemData("Wood Oil", number_buff_items, [ItemFlags.block, ItemFlags.wood, ItemFlags.ethereal])
    brass_knuckle = CombatItemData("Brass Knuckle", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff, ItemFlags.wood])
    fortune_cookie = CombatItemData("Fortune Cookie", number_buff_items, [ItemFlags.buff])
    hand_mirror = CombatItemData("Hand Mirror", number_buff_items, [ItemFlags.avoidance, ItemFlags.buff], False)
    pearl = CombatItemData("Pearl", number_buff_items, [ItemFlags.buff, ItemFlags.ethereal])
    spikey_shield = CombatItemData("Spikey Shield", number_big_items, [ItemFlags.block, ItemFlags.indirect_damage, ItemFlags.buff, ItemFlags.wood])
    harpoon = CombatItemData("Harpoon", number_buff_items, [ItemFlags.less_items, ItemFlags.buff, ItemFlags.ethereal], False)
    magnet_claw = CombatItemData("Magnet Claw", number_buff_items, [ItemFlags.magnetism, ItemFlags.buff, ItemFlags.ethereal], False)
    tentacle_claw = CombatItemData("Tentacle Claw", number_buff_items, [ItemFlags.water, ItemFlags.more_items, ItemFlags.buff, ItemFlags.ethereal], False)
    credit_card = CombatItemData("Credit Card", number_buff_items, [ItemFlags.damage, ItemFlags.coins])
    gold_dagger = CombatItemData("Gold Dagger", number_big_items, [ItemFlags.damage, ItemFlags.coins, ItemFlags.metal])
    hand_of_midas = CombatItemData("Hand of Midas", number_buff_items, [ItemFlags.coins, ItemFlags.metal, ItemFlags.ethereal])
    piggy_bank = CombatItemData("Piggy Bank", number_big_items, [ItemFlags.coins, ItemFlags.ethereal])
    eyepatch = CombatItemData("Eyepatch", number_buff_items, [ItemFlags.critical_hits])
    sickle = CombatItemData("Sickle", number_big_items, [ItemFlags.damage, ItemFlags.critical_hits, ItemFlags.metal])
    battle_axe = CombatItemData("Battle Axe", number_big_items, [ItemFlags.damage, ItemFlags.metal])
    dagger = CombatItemData("Dagger", number_small_items, [ItemFlags.damage, ItemFlags.metal])
    dark_sword = CombatItemData("Dark Sword", number_big_items, [ItemFlags.damage, ItemFlags.self_damage, ItemFlags.metal])
    double_bladed_sword = CombatItemData("Double Bladed Sword", number_big_items, [ItemFlags.damage, ItemFlags.self_damage, ItemFlags.metal])
    great_sword = CombatItemData("Great Sword", number_big_items, [ItemFlags.damage, ItemFlags.metal])
    lucky_stick = CombatItemData("Lucky Stick", number_big_items, [ItemFlags.damage, ItemFlags.wood])
    plastic_knife = CombatItemData("Plastic Knife", number_big_items, [ItemFlags.damage])
    recycling_bin = CombatItemData("Recycling Bin", number_buff_items, [ItemFlags.damage, ItemFlags.more_items, ItemFlags.ethereal])
    small_sword = CombatItemData("Small Sword", number_big_items, [ItemFlags.damage, ItemFlags.metal])
    syringe = CombatItemData("Syringe", number_buff_items, [ItemFlags.damage])
    ticking_bomb = CombatItemData("Ticking Bomb", number_buff_items, [ItemFlags.indirect_damage, ItemFlags.buff, ItemFlags.metal])
    whetstone = CombatItemData("Whetstone", number_buff_items, [ItemFlags.damage, ItemFlags.metal, ItemFlags.ethereal])
    honey_ball = CombatItemData("Honey Ball", number_small_items, [ItemFlags.water], False)
    spike = CombatItemData("Spike", number_small_items, [ItemFlags.metal], False)
    meli_bomb = CombatItemData("Meli-Bomb", number_big_items, [ItemFlags.added_by_enemies], False)
    # poisonous_spore = CombatItemData("Poisonous Spore", number_big_items, [ItemFlags.added_by_enemies], False)
    healing_flask = CombatItemData("Healing Flask", number_small_items, [ItemFlags.healing])
    magic_wand = CombatItemData("Magic Wand", number_big_items, [ItemFlags.healing, ItemFlags.wood])
    teddy = CombatItemData("Teddy", number_big_items, [ItemFlags.healing, ItemFlags.fluff])
    thermometer = CombatItemData("Thermometer", number_small_items, [ItemFlags.self_damage])
    felinas_cat_carrier = CombatItemData("Felinas Cat Carrier", number_buff_items, [ItemFlags.pets, ItemFlags.buff, ItemFlags.ethereal], False)
    antidote = CombatItemData("Antidote", number_buff_items, [ItemFlags.avoidance], False)
    poison_dagger = CombatItemData("Poison Dagger", number_big_items, [ItemFlags.damage, ItemFlags.poison, ItemFlags.metal])
    poison_flask = CombatItemData("Poison Flask", number_big_items, [ItemFlags.poison, ItemFlags.ethereal])
    poison_grenade = CombatItemData("Poison Grenade", number_big_items, [ItemFlags.damage, ItemFlags.poison])
    shuriken = CombatItemData("Shuriken", number_big_items, [ItemFlags.poison, ItemFlags.metal])
    cactus = CombatItemData("Cactus", number_big_items, [ItemFlags.self_damage, ItemFlags.block])
    # stressball_spikes = CombatItemData("Stressball Spikes", number_small_items, [ItemFlags.self_damage, ItemFlags.added_by_other], False)
    spiky_stressball = CombatItemData("Spiky Stressball", number_big_items, [ItemFlags.strength, ItemFlags.self_damage])
    glass_cleaner = CombatItemData("Glass Cleaner", number_buff_items, [ItemFlags.ethereal], False)
    heat_gun = CombatItemData("Heat Gun", number_buff_items, [ItemFlags.more_items])
    magnet = CombatItemData("Magnet", number_big_items, [ItemFlags.magnetism, ItemFlags.metal])
    amulet_of_strength = CombatItemData("Amulet of Strength", number_buff_items, [ItemFlags.strength])
    energy_drink = CombatItemData("Energy Drink", number_buff_items, [ItemFlags.block, ItemFlags.strength])
    paperclip = CombatItemData("Paperclip", number_big_items, [ItemFlags.strength, ItemFlags.metal])
    ring_of_strength = CombatItemData("Ring of Strength", number_buff_items, [ItemFlags.strength, ItemFlags.metal])
    strength_potion = CombatItemData("Strength Potion", number_buff_items, [ItemFlags.strength, ItemFlags.ethereal])
    wooden_bracelet = CombatItemData("Wooden Bracelet", number_big_items, [ItemFlags.strength, ItemFlags.block, ItemFlags.wood])
    battery = CombatItemData("Battery", number_buff_items, [ItemFlags.damage, ItemFlags.water, ItemFlags.metal])
    lava_bathbomb = CombatItemData("Lava Bathbomb", number_buff_items, [ItemFlags.more_items, ItemFlags.water, ItemFlags.fluff], False)
    toy_piranha = CombatItemData("Toy Piranha", number_buff_items, [ItemFlags.water, ItemFlags.damage, ItemFlags.fluff])
    poison_bathbomb = CombatItemData("Poison Bathbomb", number_buff_items, [ItemFlags.more_items, ItemFlags.water, ItemFlags.fluff], False)
    sponge = CombatItemData("Sponge", number_big_items, [ItemFlags.damage, ItemFlags.water])
    treasure_chest = CombatItemData("Treasure Chest", number_buff_items, [ItemFlags.damage, ItemFlags.water, ItemFlags.wood])
    # open_treasure_chest = CombatItemData("Open Treasure Chest", number_big_items, [ItemFlags.damage, ItemFlags.water, ItemFlags.added_by_other])
    water_bottle = CombatItemData("Water Bottle", number_buff_items, [ItemFlags.water, ItemFlags.more_items], False)
    waterpistol = CombatItemData("Waterpistol", number_buff_items, [ItemFlags.damage, ItemFlags.water], False)
    healing_potion = CombatItemData("Healing Potion", number_big_items, [], False)
