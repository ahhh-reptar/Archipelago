from dataclasses import dataclass

quality_dict = {
    0: "",
    1: "Silver",
    2: "Gold",
    3: "Iridium"
}


@dataclass(frozen=True)
class BundleItem:
    name: str
    id: int
    amount: int
    quality: int

    @staticmethod
    def money_bundle(amount: int):
        return BundleItem("Money", -1, amount, amount)

    def as_amount(self, amount: int):
        return BundleItem(self.name, self.id, amount, self.quality)

    def as_quality(self, quality: int):
        return BundleItem(self.name, self.id, self.amount, quality)

    def __repr__(self):
        return f"{self.amount} {quality_dict[self.quality]} {self.name}"


wild_horseradish = BundleItem("Wild Horseradish", 16, 1, 0)
daffodil = BundleItem("Daffodil", 18, 1, 0)
leek = BundleItem("Leek", 20, 1, 0)
dandelion = BundleItem("Dandelion", 22, 1, 0)
morel = BundleItem("Morel", 257, 1, 0)
common_mushroom = BundleItem("Common Mushroom", 404, 1, 0)
salmonberry = BundleItem("Salmonberry", 296, 1, 0)
spring_onion = BundleItem("Spring Onion", 399, 1, 0)

grape = BundleItem("Grape", 398, 1, 0)
spice_berry = BundleItem("Spice Berry", 396, 1, 0)
sweet_pea = BundleItem("Sweet Pea", 402, 1, 0)
red_mushroom = BundleItem("Red Mushroom", 420, 1, 0)
fiddlehead_fern = BundleItem("Fiddlehead Fern", 259, 1, 0)

wild_plum = BundleItem("Wild Plum", 406, 1, 0)
hazelnut = BundleItem("Hazelnut", 408, 1, 0)
blackberry = BundleItem("Blackberry", 410, 1, 0)
chanterelle = BundleItem("Chanterelle", 281, 1, 0)

winter_root = BundleItem("Winter Root", 412, 1, 0)
crystal_fruit = BundleItem("Crystal Fruit", 414, 1, 0)
snow_yam = BundleItem("Snow Yam", 416, 1, 0)
crocus = BundleItem("Crocus", 418, 1, 0)
holly = BundleItem("Holly", 283, 1, 0)

coconut = BundleItem("Coconut", 88, 1, 0)
cactus_fruit = BundleItem("Cactus Fruit", 90, 1, 0)
cave_carrot = BundleItem("Cave Carrot", 78, 1, 0)
purple_mushroom = BundleItem("Purple Mushroom", 422, 1, 0)
maple_syrup = BundleItem("Maple Syrup", 724, 1, 0)
oak_resin = BundleItem("Oak Resin", 725, 1, 0)
pine_tar = BundleItem("Pine Tar", 726, 1, 0)
nautilus_shell = BundleItem("Nautilus Shell", 392, 1, 0)
coral = BundleItem("Coral", 393, 1, 0)
sea_urchin = BundleItem("Sea Urchin", 397, 1, 0)
rainbow_shell = BundleItem("Rainbow Shell", 394, 1, 0)
clam = BundleItem("Clam", 372, 1, 0)
cockle = BundleItem("Cockle", 718, 1, 0)
mussel = BundleItem("Mussel", 719, 1, 0)
oyster = BundleItem("Oyster", 723, 1, 0)
seaweed = BundleItem("Seaweed", 152, 1, 0)

wood = BundleItem("Wood", 388, 99, 0)
stone = BundleItem("Stone", 390, 99, 0)
hardwood = BundleItem("Hardwood", 709, 10, 0)
clay = BundleItem("Clay", 330, 10, 0)
fiber = BundleItem("Fiber", 771, 99, 0)

blue_jazz = BundleItem("Blue Jazz", 597, 1, 0)
cauliflower = BundleItem("Cauliflower", 190, 1, 0)
green_bean = BundleItem("Green Bean", 188, 1, 0)
kale = BundleItem("Kale", 250, 1, 0)
parsnip = BundleItem("Parsnip", 24, 1, 0)
potato = BundleItem("Potato", 192, 1, 0)
strawberry = BundleItem("Strawberry", 400, 1, 0)
tulip = BundleItem("Tulip", 591, 1, 0)
unmilled_rice = BundleItem("Unmilled Rice", 271, 1, 0)
blueberry = BundleItem("Blueberry", 258, 1, 0)
corn = BundleItem("Corn", 270, 1, 0)
hops = BundleItem("Hops", 304, 1, 0)
hot_pepper = BundleItem("Hot Pepper", 260, 1, 0)
melon = BundleItem("Melon", 254, 1, 0)
poppy = BundleItem("Poppy", 376, 1, 0)
radish = BundleItem("Radish", 264, 1, 0)
summer_spangle = BundleItem("Summer Spangle", 593, 1, 0)
sunflower = BundleItem("Sunflower", 421, 1, 0)
tomato = BundleItem("Tomato", 256, 1, 0)
wheat = BundleItem("Wheat", 262, 1, 0)
hay = BundleItem("Hay", 178, 1, 0)
amaranth = BundleItem("Amaranth", 300, 1, 0)
bok_choy = BundleItem("Bok Choy", 278, 1, 0)
cranberries = BundleItem("Cranberries", 282, 1, 0)
eggplant = BundleItem("Eggplant", 272, 1, 0)
fairy_rose = BundleItem("Fairy Rose", 595, 1, 0)
pumpkin = BundleItem("Pumpkin", 276, 1, 0)
yam = BundleItem("Yam", 280, 1, 0)
sweet_gem_berry = BundleItem("Sweet Gem Berry", 417, 1, 0)
rhubarb = BundleItem("Rhubarb", 252, 1, 0)
beet = BundleItem("Beet", 284, 1, 0)
red_cabbage = BundleItem("Red Cabbage", 266, 1, 0)
artichoke = BundleItem("Artichoke", 274, 1, 0)

egg = BundleItem("Egg", 176, 1, 0)
large_egg = BundleItem("Large Egg", 174, 1, 0)
brown_egg = BundleItem("Egg (Brown)", 180, 1, 0)
large_brown_egg = BundleItem("Large Egg (Brown)", 182, 1, 0)
wool = BundleItem("Wool", 440, 1, 0)
milk = BundleItem("Milk", 184, 1, 0)
large_milk = BundleItem("Large Milk", 186, 1, 0)
goat_milk = BundleItem("Goat Milk", 436, 1, 0)
large_goat_milk = BundleItem("Large Goat Milk", 438, 1, 0)
truffle = BundleItem("Truffle", 430, 1, 0)
duck_feather = BundleItem("Duck Feather", 444, 1, 0)
duck_egg = BundleItem("Duck Egg", 442, 1, 0)
rabbit_foot = BundleItem("Rabbit's Foot", 446, 1, 0)

truffle_oil = BundleItem("Truffle Oil", 432, 1, 0)
cloth = BundleItem("Cloth", 428, 1, 0)
goat_cheese = BundleItem("Goat Cheese", 426, 1, 0)
cheese = BundleItem("Cheese", 424, 1, 0)
honey = BundleItem("Honey", 340, 1, 0)
beer = BundleItem("Beer", 346, 1, 0)
juice = BundleItem("Juice", 350, 1, 0)
mead = BundleItem("Mead", 459, 1, 0)
pale_ale = BundleItem("Pale Ale", 303, 1, 0)
wine = BundleItem("Wine", 348, 1, 0)
jelly = BundleItem("Jelly", 344, 1, 0)
pickles = BundleItem("Pickles", 342, 1, 0)
caviar = BundleItem("Caviar", 445, 1, 0)
aged_roe = BundleItem("Aged Roe", 447, 1, 0)
apple = BundleItem("Apple", 613, 1, 0)
apricot = BundleItem("Apricot", 634, 1, 0)
orange = BundleItem("Orange", 635, 1, 0)
peach = BundleItem("Peach", 636, 1, 0)
pomegranate = BundleItem("Pomegranate", 637, 1, 0)
cherry = BundleItem("Cherry", 638, 1, 0)

chub = BundleItem("Chub", 702, 1, 0)
catfish = BundleItem("Catfish", 143, 1, 0)
rainbow_trout = BundleItem("Rainbow Trout", 138, 1, 0)
lingcod = BundleItem("Lingcod", 707, 1, 0)
walleye = BundleItem("Walleye", 140, 1, 0)
perch = BundleItem("Perch", 141, 1, 0)
pike = BundleItem("Pike", 144, 1, 0)
bream = BundleItem("Bream", 132, 1, 0)
salmon = BundleItem("Salmon", 139, 1, 0)
sunfish = BundleItem("Sunfish", 145, 1, 0)
tiger_trout = BundleItem("Tiger Trout", 699, 1, 0)
shad = BundleItem("Shad", 706, 1, 0)
smallmouth_bass = BundleItem("Smallmouth Bass", 137, 1, 0)
dorado = BundleItem("Dorado", 704, 1, 0)
carp = BundleItem("Carp", 142, 1, 0)
midnight_carp = BundleItem("Midnight Carp", 269, 1, 0)
largemouth_bass = BundleItem("Largemouth Bass", 136, 1, 0)
sturgeon = BundleItem("Sturgeon", 698, 1, 0)
bullhead = BundleItem("Bullhead", 700, 1, 0)
tilapia = BundleItem("Tilapia", 701, 1, 0)
pufferfish = BundleItem("Pufferfish", 128, 1, 0)
tuna = BundleItem("Tuna", 130, 1, 0)
super_cucumber = BundleItem("Super Cucumber", 155, 1, 0)
flounder = BundleItem("Flounder", 267, 1, 0)
anchovy = BundleItem("Anchovy", 129, 1, 0)
sardine = BundleItem("Sardine", 131, 1, 0)
red_mullet = BundleItem("Red Mullet", 146, 1, 0)
herring = BundleItem("Herring", 147, 1, 0)
eel = BundleItem("Eel", 148, 1, 0)
octopus = BundleItem("Octopus", 149, 1, 0)
red_snapper = BundleItem("Red Snapper", 150, 1, 0)
squid = BundleItem("Squid", 151, 1, 0)
sea_cucumber = BundleItem("Sea Cucumber", 154, 1, 0)
albacore = BundleItem("Albacore", 705, 1, 0)
halibut = BundleItem("Halibut", 708, 1, 0)
scorpion_carp = BundleItem("Scorpion Carp", 165, 1, 0)
sandfish = BundleItem("Sandfish", 164, 1, 0)
woodskip = BundleItem("Woodskip", 734, 1, 0)
lava_eel = BundleItem("Lava Eel", 162, 1, 0)
ice_pip = BundleItem("Ice Pip", 161, 1, 0)
stonefish = BundleItem("Stonefish", 158, 1, 0)
ghostfish = BundleItem("Ghostfish", 156, 1, 0)
lobster = BundleItem("Lobster", 715, 1, 0)
crab = BundleItem("Crab", 717, 1, 0)
shrimp = BundleItem("Shrimp", 720, 1, 0)
crayfish = BundleItem("Crayfish", 716, 1, 0)
snail = BundleItem("Snail", 721, 1, 0)
periwinkle = BundleItem("Periwinkle", 722, 1, 0)
trash = BundleItem("Trash", 168, 1, 0)
driftwood = BundleItem("Driftwood", 169, 1, 0)
soggy_newspaper = BundleItem("Soggy Newspaper", 172, 1, 0)
broken_cd = BundleItem("Broken CD", 171, 1, 0)
broken_glasses = BundleItem("Broken Glasses", 170, 1, 0)

wilted_bouquet = BundleItem("Wilted Bouquet", 277, 1, 0)
copper_bar = BundleItem("Copper Bar", 334, 2, 0)
iron_Bar = BundleItem("Iron Bar", 335, 2, 0)
gold_bar = BundleItem("Gold Bar", 336, 1, 0)
iridium_bar = BundleItem("Iridium Bar", 337, 1, 0)
refined_quartz = BundleItem("Refined Quartz", 338, 2, 0)
coal = BundleItem("Coal", 382, 5, 0)

quartz = BundleItem("Quartz", 80, 1, 0)
fire_quartz = BundleItem("Fire Quartz", 82, 1, 0)
frozen_tear = BundleItem("Frozen Tear", 84, 1, 0)
earth_crystal = BundleItem("Earth Crystal", 86, 1, 0)
emerald = BundleItem("Emerald", 60, 1, 0)
aquamarine = BundleItem("Aquamarine", 62, 1, 0)
ruby = BundleItem("Ruby", 64, 1, 0)
amethyst = BundleItem("Amethyst", 66, 1, 0)
topaz = BundleItem("Topaz", 68, 1, 0)
jade = BundleItem("Jade", 70, 1, 0)

slime = BundleItem("Slime", 766, 99, 0)
bug_meat = BundleItem("Bug Meat", 684, 10, 0)
bat_wing = BundleItem("Bat Wing", 767, 10, 0)
solar_essence = BundleItem("Solar Essence", 768, 1, 0)
void_essence = BundleItem("Void Essence", 769, 1, 0)

maki_roll = BundleItem("Maki Roll", 228, 1, 0)
fried_egg = BundleItem("Fried Egg", 194, 1, 0)
omelet = BundleItem("Omelet", 195, 1, 0)
pizza = BundleItem("Pizza", 206, 1, 0)
hashbrowns = BundleItem("Hashbrowns", 210, 1, 0)
pancakes = BundleItem("Pancakes", 211, 1, 0)
bread = BundleItem("Bread", 216, 1, 0)
tortilla = BundleItem("Tortilla", 229, 1, 0)
triple_shot_espresso = BundleItem("Triple Shot Espresso", 253, 1, 0)
farmer_s_lunch = BundleItem("Farmer's Lunch", 240, 1, 0)
survival_burger = BundleItem("Survival Burger", 241, 1, 0)
dish_o_the_sea = BundleItem("Dish O' The Sea", 242, 1, 0)
miner_s_treat = BundleItem("Miner's Treat", 243, 1, 0)
roots_platter = BundleItem("Roots Platter", 244, 1, 0)
salad = BundleItem("Salad", 196, 1, 0)
cheese_cauliflower = BundleItem("Cheese Cauliflower", 197, 1, 0)
parsnip_soup = BundleItem("Parsnip Soup", 198, 1, 0)
fried_mushroom = BundleItem("Fried Mushroom", 205, 1, 0)
salmon_dinner = BundleItem("Salmon Dinner", 212, 1, 0)
pepper_poppers = BundleItem("Pepper Poppers", 215, 1, 0)
spaghetti = BundleItem("Spaghetti", 224, 1, 0)
sashimi = BundleItem("Sashimi", 227, 1, 0)
blueberry_tart = BundleItem("Blueberry Tart", 234, 1, 0)
algae_soup = BundleItem("Algae Soup", 456, 1, 0)
pale_broth = BundleItem("Pale Broth", 457, 1, 0)
chowder = BundleItem("Chowder", 727, 1, 0)
green_algae = BundleItem("Green Algae", 153, 1, 0)
white_algae = BundleItem("White Algae", 157, 1, 0)
geode = BundleItem("Geode", 535, 1, 0)
frozen_geode = BundleItem("Frozen Geode", 536, 1, 0)
magma_geode = BundleItem("Magma Geode", 537, 1, 0)
omni_geode = BundleItem("Omni Geode", 749, 1, 0)

spring_foraging_items = [wild_horseradish, daffodil, leek, dandelion, salmonberry, spring_onion]
summer_foraging_items = [grape, spice_berry, sweet_pea, fiddlehead_fern, rainbow_shell]
fall_foraging_items = [common_mushroom, wild_plum, hazelnut, blackberry]
winter_foraging_items = [winter_root, crystal_fruit, snow_yam, crocus, holly, nautilus_shell]
exotic_foraging_items = [coconut, cactus_fruit, cave_carrot, red_mushroom, purple_mushroom,
                         maple_syrup, oak_resin, pine_tar, morel, coral,
                         sea_urchin, clam, cockle, mussel, oyster, seaweed]
construction_items = [wood, stone, hardwood, clay, fiber]

# TODO coffee_bean, garlic, rhubarb, tea_leaves
spring_crop_items = [blue_jazz, cauliflower, green_bean, kale, parsnip, potato, strawberry, tulip, unmilled_rice]
# TODO red_cabbage, starfruit, ancient_fruit, pineapple, taro_root
summer_crops_items = [blueberry, corn, hops, hot_pepper, melon, poppy,
                      radish, summer_spangle, sunflower, tomato, wheat]
# TODO artichoke, beet
fall_crops_items = [corn, sunflower, wheat, amaranth, bok_choy, cranberries,
                    eggplant, fairy_rose, grape, pumpkin, yam, sweet_gem_berry]
all_crops_items = {*spring_crop_items, *summer_crops_items, *fall_crops_items}
quality_crops_items = {item.as_quality(2).as_amount(5) for item in all_crops_items}
# TODO void_egg, dinosaur_egg, ostrich_egg, golden_egg
animal_product_items = [egg, large_egg, brown_egg, large_brown_egg, wool, milk, large_milk,
                        goat_milk, large_goat_milk, truffle, duck_feather, duck_egg, rabbit_foot]
# TODO coffee, green_tea
artisan_goods_items = [truffle_oil, cloth, goat_cheese, cheese, honey, beer, juice, mead, pale_ale, wine, jelly,
                       pickles, caviar, aged_roe, apple, apricot, orange, peach, pomegranate, cherry]

river_fish_items = [chub, catfish, rainbow_trout, lingcod, walleye, perch, pike, bream,
                    salmon, sunfish, tiger_trout, shad, smallmouth_bass, dorado]
lake_fish_items = [chub, rainbow_trout, lingcod, walleye, perch, carp, midnight_carp,
                   largemouth_bass, sturgeon, bullhead, midnight_carp]
ocean_fish_items = [tilapia, pufferfish, tuna, super_cucumber, flounder, anchovy, sardine, red_mullet,
                    herring, eel, octopus, red_snapper, squid, sea_cucumber, albacore, halibut]
night_fish_items = [walleye, bream, super_cucumber, eel, squid, midnight_carp]
# TODO void_salmon
specialty_fish_items = [scorpion_carp, sandfish, woodskip, pufferfish, eel, octopus,
                        squid, lava_eel, ice_pip, stonefish, ghostfish, dorado]
crab_pot_items = [lobster, clam, crab, cockle, mussel, shrimp, oyster, crayfish, snail,
                  periwinkle, trash, driftwood, soggy_newspaper, broken_cd, broken_glasses]

# TODO radioactive_bar
blacksmith_items = [wilted_bouquet, copper_bar, iron_Bar, gold_bar, iridium_bar, refined_quartz, coal]
geologist_items = [quartz, earth_crystal, frozen_tear, fire_quartz, emerald, aquamarine, ruby, amethyst, topaz, jade]
adventurer_items = [slime, bug_meat, bat_wing, solar_essence, void_essence, coal]

chef_items = [maki_roll, fried_egg, omelet, pizza, hashbrowns, pancakes, bread, tortilla, triple_shot_espresso,
              farmer_s_lunch, survival_burger, dish_o_the_sea, miner_s_treat, roots_platter, salad,
              cheese_cauliflower, parsnip_soup, fried_mushroom, salmon_dinner, pepper_poppers, spaghetti,
              sashimi, blueberry_tart, algae_soup, pale_broth, chowder]

dwarf_scroll_1 = BundleItem("Dwarf Scroll I", 96, 1, 0)
dwarf_scroll_2 = BundleItem("Dwarf Scroll II", 97, 1, 0)
dwarf_scroll_3 = BundleItem("Dwarf Scroll III", 98, 1, 0)
dwarf_scroll_4 = BundleItem("Dwarf Scroll IV", 99, 1, 0)
elvish_jewelry = BundleItem("Elvish Jewelry", 104, 1, 0)
ancient_drum = BundleItem("Ancient Drum", 123, 1, 0)
dried_starfish = BundleItem("Dried Starfish", 116, 1, 0)

# TODO Dye Bundle
dye_red_items = [cranberries, dwarf_scroll_1, hot_pepper, radish, rhubarb, spaghetti, strawberry, tomato, tulip]
dye_orange_items = [poppy, pumpkin, apricot, orange, spice_berry, winter_root]
dye_yellow_items = [dried_starfish, dwarf_scroll_4, elvish_jewelry, corn, parsnip, summer_spangle, sunflower]
dye_green_items = [dwarf_scroll_2, fiddlehead_fern, kale, artichoke, bok_choy, green_bean]
dye_blue_items = [blueberry, dwarf_scroll_3, blue_jazz, blackberry, crystal_fruit]
dye_purple_items = [ancient_drum, beet, crocus, eggplant, red_cabbage, sweet_pea]
dye_items = [dye_red_items, dye_orange_items, dye_yellow_items, dye_green_items, dye_blue_items, dye_purple_items]
field_research_items = [purple_mushroom, nautilus_shell, chub, geode, frozen_geode, magma_geode, omni_geode,
                        rainbow_shell, amethyst, bream, carp]
fodder_items = [wheat.as_amount(10), hay.as_amount(10), apple.as_amount(3), kale.as_amount(3), corn.as_amount(3),
                green_bean.as_amount(3), potato.as_amount(3), green_algae.as_amount(5), white_algae.as_amount(3)]
enchanter_items = [oak_resin, wine, rabbit_foot, pomegranate, purple_mushroom, solar_essence,
                   super_cucumber, void_essence, fire_quartz, frozen_tear, jade]

vault_2500_items = [BundleItem.money_bundle(2500)]
vault_5000_items = [BundleItem.money_bundle(5000)]
vault_10000_items = [BundleItem.money_bundle(10000)]
vault_25000_items = [BundleItem.money_bundle(25000)]

crafts_room_bundle_items = {
    *spring_foraging_items,
    *summer_foraging_items,
    *fall_foraging_items,
    *winter_foraging_items,
    *exotic_foraging_items,
    *construction_items,
}

pantry_bundle_items = {
    *spring_crop_items,
    *summer_crops_items,
    *fall_crops_items,
    *quality_crops_items,
    *animal_product_items,
    *artisan_goods_items,
}

fish_tank_bundle_items = {
    *river_fish_items,
    *lake_fish_items,
    *ocean_fish_items,
    *night_fish_items,
    *crab_pot_items,
    *specialty_fish_items,
}

boiler_room_bundle_items = {
    *blacksmith_items,
    *geologist_items,
    *adventurer_items,
}

bulletin_board_bundle_items = {
    *chef_items,
    *[item for dye_color_items in dye_items for item in dye_color_items],
    *field_research_items,
    *fodder_items,
    *enchanter_items
}

vault_bundle_items = {
    *vault_2500_items,
    *vault_5000_items,
    *vault_10000_items,
    *vault_25000_items,
}

all_bundle_items_except_money = sorted({
    *crafts_room_bundle_items,
    *pantry_bundle_items,
    *fish_tank_bundle_items,
    *boiler_room_bundle_items,
    *bulletin_board_bundle_items,
}, key=lambda x: x.name)

all_bundle_items = sorted({
    *crafts_room_bundle_items,
    *pantry_bundle_items,
    *fish_tank_bundle_items,
    *boiler_room_bundle_items,
    *bulletin_board_bundle_items,
    *vault_bundle_items,
}, key=lambda x: x.name)

all_bundle_items_by_name = {item.name: item for item in all_bundle_items}
all_bundle_items_by_id = {item.id: item for item in all_bundle_items}
