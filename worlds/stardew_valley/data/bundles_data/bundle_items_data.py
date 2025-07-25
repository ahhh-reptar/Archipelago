from ..hats_data import Hats
from ..shirt_data import Shirts
from ...bundles.bundle_item import BundleItem
from ...strings.animal_product_names import AnimalProduct
from ...strings.artisan_good_names import ArtisanGood
from ...strings.boot_names import Boots
from ...strings.catalogue_names import CatalogueItem
from ...strings.craftable_names import Consumable, Lighting, Fishing, Craftable, Bomb, Furniture, Floor, Edible
from ...strings.crop_names import Vegetable, Fruit
from ...strings.currency_names import Currency
from ...strings.decoration_names import Decoration
from ...strings.fertilizer_names import Fertilizer, SpeedGro, RetainingSoil
from ...strings.fish_names import Fish, WaterItem, Trash
from ...strings.flower_names import Flower
from ...strings.food_names import Meal, Beverage
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.fruit_tree_names import Sapling
from ...strings.geode_names import Geode
from ...strings.gift_names import Gift
from ...strings.ingredient_names import Ingredient
from ...strings.material_names import Material
from ...strings.meme_item_names import MemeItem
from ...strings.metal_names import Fossil, Ore, MetalBar, Mineral, Artifact
from ...strings.monster_drop_names import Loot
from ...strings.seed_names import TreeSeed, Seed
from ...strings.special_item_names import SpecialItem, NotReallyAnItem

wild_horseradish = BundleItem(Forageable.wild_horseradish)
daffodil = BundleItem(Forageable.daffodil)
leek = BundleItem(Forageable.leek)
dandelion = BundleItem(Forageable.dandelion)
morel = BundleItem(Mushroom.morel)
common_mushroom = BundleItem(Mushroom.common)
salmonberry = BundleItem(Forageable.salmonberry)
spring_onion = BundleItem(Forageable.spring_onion)

grape = BundleItem(Fruit.grape)
spice_berry = BundleItem(Forageable.spice_berry)
sweet_pea = BundleItem(Forageable.sweet_pea)
red_mushroom = BundleItem(Mushroom.red)
fiddlehead_fern = BundleItem(Forageable.fiddlehead_fern)

wild_plum = BundleItem(Forageable.wild_plum)
hazelnut = BundleItem(Forageable.hazelnut)
blackberry = BundleItem(Forageable.blackberry)
chanterelle = BundleItem(Mushroom.chanterelle)

winter_root = BundleItem(Forageable.winter_root)
crystal_fruit = BundleItem(Forageable.crystal_fruit)
snow_yam = BundleItem(Forageable.snow_yam)
crocus = BundleItem(Forageable.crocus)
holly = BundleItem(Forageable.holly)

coconut = BundleItem(Forageable.coconut)
golden_coconut = BundleItem(Geode.golden_coconut, source=BundleItem.Sources.island)
cactus_fruit = BundleItem(Forageable.cactus_fruit)
cave_carrot = BundleItem(Forageable.cave_carrot)
purple_mushroom = BundleItem(Mushroom.purple)
maple_syrup = BundleItem(ArtisanGood.maple_syrup)
oak_resin = BundleItem(ArtisanGood.oak_resin)
pine_tar = BundleItem(ArtisanGood.pine_tar)
nautilus_shell = BundleItem(WaterItem.nautilus_shell)
coral = BundleItem(WaterItem.coral)
sea_urchin = BundleItem(WaterItem.sea_urchin)
rainbow_shell = BundleItem(Forageable.rainbow_shell)
clam = BundleItem(Fish.clam)
cockle = BundleItem(Fish.cockle)
mussel = BundleItem(Fish.mussel)
oyster = BundleItem(Fish.oyster)
seaweed = BundleItem(WaterItem.seaweed, can_have_quality=False)

wood = BundleItem(Material.wood, 99)
stone = BundleItem(Material.stone, 99)
hardwood = BundleItem(Material.hardwood, 10)
clay = BundleItem(Material.clay)
fiber = BundleItem(Material.fiber)
moss = BundleItem(Material.moss)

mixed_seeds = BundleItem(Seed.mixed)
acorn = BundleItem(TreeSeed.acorn)
maple_seed = BundleItem(TreeSeed.maple)
pine_cone = BundleItem(TreeSeed.pine)
mahogany_seed = BundleItem(TreeSeed.mahogany)
mushroom_tree_seed = BundleItem(TreeSeed.mushroom, source=BundleItem.Sources.island)
mystic_tree_seed = BundleItem(TreeSeed.mystic, source=BundleItem.Sources.masteries)
mossy_seed = BundleItem(TreeSeed.mossy)

strawberry_seeds = BundleItem(Seed.strawberry)
sunflower_seeds = BundleItem(Seed.sunflower)

blue_jazz = BundleItem(Flower.blue_jazz)
cauliflower = BundleItem(Vegetable.cauliflower)
green_bean = BundleItem(Vegetable.green_bean)
kale = BundleItem(Vegetable.kale)
parsnip = BundleItem(Vegetable.parsnip)
potato = BundleItem(Vegetable.potato)
strawberry = BundleItem(Fruit.strawberry, source=BundleItem.Sources.festival)
tulip = BundleItem(Flower.tulip)
unmilled_rice = BundleItem(Vegetable.unmilled_rice)
coffee_bean = BundleItem(Seed.coffee)
garlic = BundleItem(Vegetable.garlic)
blueberry = BundleItem(Fruit.blueberry)
corn = BundleItem(Vegetable.corn)
hops = BundleItem(Vegetable.hops)
hot_pepper = BundleItem(Fruit.hot_pepper)
melon = BundleItem(Fruit.melon)
poppy = BundleItem(Flower.poppy)
radish = BundleItem(Vegetable.radish)
summer_spangle = BundleItem(Flower.summer_spangle)
sunflower = BundleItem(Flower.sunflower)
tomato = BundleItem(Vegetable.tomato)
wheat = BundleItem(Vegetable.wheat)
hay = BundleItem(Forageable.hay)
amaranth = BundleItem(Vegetable.amaranth)
bok_choy = BundleItem(Vegetable.bok_choy)
cranberries = BundleItem(Fruit.cranberries)
eggplant = BundleItem(Vegetable.eggplant)
fairy_rose = BundleItem(Flower.fairy_rose)
pumpkin = BundleItem(Vegetable.pumpkin)
yam = BundleItem(Vegetable.yam)
sweet_gem_berry = BundleItem(Fruit.sweet_gem_berry)
rhubarb = BundleItem(Fruit.rhubarb)
beet = BundleItem(Vegetable.beet)
red_cabbage = BundleItem(Vegetable.red_cabbage)
starfruit = BundleItem(Fruit.starfruit)
artichoke = BundleItem(Vegetable.artichoke)
pineapple = BundleItem(Fruit.pineapple, source=BundleItem.Sources.content)
taro_root = BundleItem(Vegetable.taro_root, source=BundleItem.Sources.content)
dragon_tooth = BundleItem(Forageable.dragon_tooth, source=BundleItem.Sources.content)

carrot = BundleItem(Vegetable.carrot)
summer_squash = BundleItem(Vegetable.summer_squash)
broccoli = BundleItem(Vegetable.broccoli)
powdermelon = BundleItem(Fruit.powdermelon)

egg = BundleItem(AnimalProduct.egg)
large_egg = BundleItem(AnimalProduct.large_egg)
brown_egg = BundleItem(AnimalProduct.brown_egg)
large_brown_egg = BundleItem(AnimalProduct.large_brown_egg)
wool = BundleItem(AnimalProduct.wool)
milk = BundleItem(AnimalProduct.milk)
large_milk = BundleItem(AnimalProduct.large_milk)
goat_milk = BundleItem(AnimalProduct.goat_milk)
large_goat_milk = BundleItem(AnimalProduct.large_goat_milk)
truffle = BundleItem(AnimalProduct.truffle)
duck_feather = BundleItem(AnimalProduct.duck_feather)
duck_egg = BundleItem(AnimalProduct.duck_egg)
rabbit_foot = BundleItem(AnimalProduct.rabbit_foot)
dinosaur_egg = BundleItem(AnimalProduct.dinosaur_egg)
void_egg = BundleItem(AnimalProduct.void_egg)
ostrich_egg = BundleItem(AnimalProduct.ostrich_egg, source=BundleItem.Sources.content)
golden_egg = BundleItem(AnimalProduct.golden_egg)

truffle_oil = BundleItem(ArtisanGood.truffle_oil)
cloth = BundleItem(ArtisanGood.cloth)
goat_cheese = BundleItem(ArtisanGood.goat_cheese)
cheese = BundleItem(ArtisanGood.cheese)
honey = BundleItem(ArtisanGood.honey)
beer = BundleItem(Beverage.beer)
mayonnaise = BundleItem(ArtisanGood.mayonnaise)
juice = BundleItem(ArtisanGood.juice)
mead = BundleItem(ArtisanGood.mead)
pale_ale = BundleItem(ArtisanGood.pale_ale)
wine = BundleItem(ArtisanGood.wine)
jelly = BundleItem(ArtisanGood.jelly)
pickles = BundleItem(ArtisanGood.pickles)
caviar = BundleItem(ArtisanGood.caviar)
aged_roe = BundleItem(ArtisanGood.aged_roe)
roe = BundleItem(AnimalProduct.roe)
squid_ink = BundleItem(AnimalProduct.squid_ink)
coffee = BundleItem(Beverage.coffee)
green_tea = BundleItem(ArtisanGood.green_tea)
apple = BundleItem(Fruit.apple)
apricot = BundleItem(Fruit.apricot)
orange = BundleItem(Fruit.orange)
peach = BundleItem(Fruit.peach)
pomegranate = BundleItem(Fruit.pomegranate)
cherry = BundleItem(Fruit.cherry)
banana = BundleItem(Fruit.banana, source=BundleItem.Sources.content)
mango = BundleItem(Fruit.mango, source=BundleItem.Sources.content)

basic_fertilizer = BundleItem(Fertilizer.basic, 100)
quality_fertilizer = BundleItem(Fertilizer.quality, 20)
deluxe_fertilizer = BundleItem(Fertilizer.deluxe, 5, source=BundleItem.Sources.island)
basic_retaining_soil = BundleItem(RetainingSoil.basic, 80)
quality_retaining_soil = BundleItem(RetainingSoil.quality, 50)
deluxe_retaining_soil = BundleItem(RetainingSoil.deluxe, 20, source=BundleItem.Sources.island)
speed_gro = BundleItem(SpeedGro.basic, 40)
deluxe_speed_gro = BundleItem(SpeedGro.deluxe, 20)
hyper_speed_gro = BundleItem(SpeedGro.hyper, 5, source=BundleItem.Sources.island)
tree_fertilizer = BundleItem(Fertilizer.tree, 20)

lobster = BundleItem(Fish.lobster)
crab = BundleItem(Fish.crab)
shrimp = BundleItem(Fish.shrimp)
crayfish = BundleItem(Fish.crayfish)
snail = BundleItem(Fish.snail)
periwinkle = BundleItem(Fish.periwinkle)
trash = BundleItem(Trash.trash)
driftwood = BundleItem(Trash.driftwood)
soggy_newspaper = BundleItem(Trash.soggy_newspaper)
broken_cd = BundleItem(Trash.broken_cd)
broken_glasses = BundleItem(Trash.broken_glasses)

chub = BundleItem(Fish.chub)
catfish = BundleItem(Fish.catfish)
rainbow_trout = BundleItem(Fish.rainbow_trout)
lingcod = BundleItem(Fish.lingcod)
walleye = BundleItem(Fish.walleye)
perch = BundleItem(Fish.perch)
pike = BundleItem(Fish.pike)
bream = BundleItem(Fish.bream)
salmon = BundleItem(Fish.salmon)
sunfish = BundleItem(Fish.sunfish)
tiger_trout = BundleItem(Fish.tiger_trout)
shad = BundleItem(Fish.shad)
smallmouth_bass = BundleItem(Fish.smallmouth_bass)
dorado = BundleItem(Fish.dorado)
carp = BundleItem(Fish.carp)
midnight_carp = BundleItem(Fish.midnight_carp)
largemouth_bass = BundleItem(Fish.largemouth_bass)
sturgeon = BundleItem(Fish.sturgeon)
bullhead = BundleItem(Fish.bullhead)
tilapia = BundleItem(Fish.tilapia)
pufferfish = BundleItem(Fish.pufferfish)
tuna = BundleItem(Fish.tuna)
super_cucumber = BundleItem(Fish.super_cucumber)
flounder = BundleItem(Fish.flounder)
anchovy = BundleItem(Fish.anchovy)
sardine = BundleItem(Fish.sardine)
red_mullet = BundleItem(Fish.red_mullet)
herring = BundleItem(Fish.herring)
eel = BundleItem(Fish.eel)
octopus = BundleItem(Fish.octopus)
red_snapper = BundleItem(Fish.red_snapper)
squid = BundleItem(Fish.squid)
sea_cucumber = BundleItem(Fish.sea_cucumber)
albacore = BundleItem(Fish.albacore)
halibut = BundleItem(Fish.halibut)
scorpion_carp = BundleItem(Fish.scorpion_carp)
sandfish = BundleItem(Fish.sandfish)
woodskip = BundleItem(Fish.woodskip)
lava_eel = BundleItem(Fish.lava_eel)
ice_pip = BundleItem(Fish.ice_pip)
stonefish = BundleItem(Fish.stonefish)
ghostfish = BundleItem(Fish.ghostfish)

bouquet = BundleItem(Gift.bouquet)
wilted_bouquet = BundleItem(Gift.wilted_bouquet)
copper_bar = BundleItem(MetalBar.copper)
iron_bar = BundleItem(MetalBar.iron)
gold_bar = BundleItem(MetalBar.gold)
iridium_bar = BundleItem(MetalBar.iridium)
radioactive_bar = BundleItem(MetalBar.radioactive, source=BundleItem.Sources.island)
refined_quartz = BundleItem(MetalBar.quartz)
coal = BundleItem(Material.coal)
iridium_ore = BundleItem(Ore.iridium)
gold_ore = BundleItem(Ore.gold)
iron_ore = BundleItem(Ore.iron)
copper_ore = BundleItem(Ore.copper)
radioactive_ore = BundleItem(Ore.radioactive, source=BundleItem.Sources.island)
battery_pack = BundleItem(ArtisanGood.battery_pack)

quartz = BundleItem(Mineral.quartz)
fire_quartz = BundleItem(Mineral.fire_quartz)
frozen_tear = BundleItem(Mineral.frozen_tear)
earth_crystal = BundleItem(Mineral.earth_crystal)
emerald = BundleItem(Mineral.emerald)
aquamarine = BundleItem(Mineral.aquamarine)
ruby = BundleItem(Mineral.ruby)
amethyst = BundleItem(Mineral.amethyst)
topaz = BundleItem(Mineral.topaz)
jade = BundleItem(Mineral.jade)
obsidian = BundleItem(Mineral.obsidian)
jamborite = BundleItem(Mineral.jamborite)
tigerseye = BundleItem(Mineral.tigerseye)
opal = BundleItem(Mineral.opal)
thunder_egg = BundleItem(Mineral.thunder_egg)
ghost_crystal = BundleItem(Mineral.ghost_crystal)
kyanite = BundleItem(Mineral.kyanite)
lemon_stone = BundleItem(Mineral.lemon_stone)
mudstone = BundleItem(Mineral.mudstone)
limestone = BundleItem(Mineral.limestone)

slime = BundleItem(Loot.slime, 99)
bug_meat = BundleItem(Loot.bug_meat, 10)
bat_wing = BundleItem(Loot.bat_wing, 10)
solar_essence = BundleItem(Loot.solar_essence)
void_essence = BundleItem(Loot.void_essence)

petrified_slime = BundleItem(Mineral.petrified_slime)
blue_slime_egg = BundleItem(AnimalProduct.slime_egg_blue)
red_slime_egg = BundleItem(AnimalProduct.slime_egg_red)
purple_slime_egg = BundleItem(AnimalProduct.slime_egg_purple)
green_slime_egg = BundleItem(AnimalProduct.slime_egg_green)
tiger_slime_egg = BundleItem(AnimalProduct.slime_egg_tiger, source=BundleItem.Sources.island)

cherry_bomb = BundleItem(Bomb.cherry_bomb, 5)
bomb = BundleItem(Bomb.bomb, 2)
mega_bomb = BundleItem(Bomb.mega_bomb)
explosive_ammo = BundleItem(Craftable.explosive_ammo, 5)

maki_roll = BundleItem(Meal.maki_roll)
fried_egg = BundleItem(Meal.fried_egg)
omelet = BundleItem(Meal.omelet)
pizza = BundleItem(Meal.pizza)
hashbrowns = BundleItem(Meal.hashbrowns)
pancakes = BundleItem(Meal.pancakes)
bread = BundleItem(Meal.bread)
tortilla = BundleItem(Meal.tortilla)
triple_shot_espresso = BundleItem(Beverage.triple_shot_espresso)
farmer_s_lunch = BundleItem(Meal.farmer_lunch)
survival_burger = BundleItem(Meal.survival_burger)
dish_o_the_sea = BundleItem(Meal.dish_o_the_sea)
miner_s_treat = BundleItem(Meal.miners_treat)
roots_platter = BundleItem(Meal.roots_platter)
salad = BundleItem(Meal.salad)
cheese_cauliflower = BundleItem(Meal.cheese_cauliflower)
parsnip_soup = BundleItem(Meal.parsnip_soup)
fried_mushroom = BundleItem(Meal.fried_mushroom)
salmon_dinner = BundleItem(Meal.salmon_dinner)
pepper_poppers = BundleItem(Meal.pepper_poppers)
spaghetti = BundleItem(Meal.spaghetti)
sashimi = BundleItem(Meal.sashimi)
blueberry_tart = BundleItem(Meal.blueberry_tart)
algae_soup = BundleItem(Meal.algae_soup)
pale_broth = BundleItem(Meal.pale_broth)
chowder = BundleItem(Meal.chowder)
cookie = BundleItem(Meal.cookie)
ancient_doll = BundleItem(Artifact.ancient_doll)
ice_cream = BundleItem(Meal.ice_cream)
cranberry_candy = BundleItem(Meal.cranberry_candy)
ginger_ale = BundleItem(Beverage.ginger_ale, source=BundleItem.Sources.island)
pink_cake = BundleItem(Meal.pink_cake)
plum_pudding = BundleItem(Meal.plum_pudding)
chocolate_cake = BundleItem(Meal.chocolate_cake)
rhubarb_pie = BundleItem(Meal.rhubarb_pie)
shrimp_cocktail = BundleItem(Meal.shrimp_cocktail)
pina_colada = BundleItem(Beverage.pina_colada, source=BundleItem.Sources.island)
stuffing = BundleItem(Meal.stuffing)
magic_rock_candy = BundleItem(Meal.magic_rock_candy)
spicy_eel = BundleItem(Meal.spicy_eel)
crab_cakes = BundleItem(Meal.crab_cakes)
eggplant_parmesan = BundleItem(Meal.eggplant_parmesan)
pumpkin_soup = BundleItem(Meal.pumpkin_soup)
lucky_lunch = BundleItem(Meal.lucky_lunch)
joja_cola = BundleItem(Trash.joja_cola)
strange_bun = BundleItem(Meal.strange_bun)
moss_soup = BundleItem(Meal.moss_soup)
roasted_hazelnuts = BundleItem(Meal.roasted_hazelnuts)
maple_bar = BundleItem(Meal.maple_bar)

green_algae = BundleItem(WaterItem.green_algae)
white_algae = BundleItem(WaterItem.white_algae)
geode = BundleItem(Geode.geode)
frozen_geode = BundleItem(Geode.frozen)
magma_geode = BundleItem(Geode.magma)
omni_geode = BundleItem(Geode.omni)
sap = BundleItem(Material.sap)

dwarf_scroll_1 = BundleItem(Artifact.dwarf_scroll_i)
dwarf_scroll_2 = BundleItem(Artifact.dwarf_scroll_ii)
dwarf_scroll_3 = BundleItem(Artifact.dwarf_scroll_iii)
dwarf_scroll_4 = BundleItem(Artifact.dwarf_scroll_iv)
elvish_jewelry = BundleItem(Artifact.elvish_jewelry)
ancient_drum = BundleItem(Artifact.ancient_drum)
dried_starfish = BundleItem(Fossil.dried_starfish)
bone_fragment = BundleItem(Fossil.bone_fragment)

golden_mask = BundleItem(Artifact.golden_mask)
golden_relic = BundleItem(Artifact.golden_relic)
dwarf_gadget = BundleItem(Artifact.dwarf_gadget)
dwarvish_helm = BundleItem(Artifact.dwarvish_helm)
prehistoric_handaxe = BundleItem(Artifact.prehistoric_handaxe)
bone_flute = BundleItem(Artifact.bone_flute)
anchor = BundleItem(Artifact.anchor)
prehistoric_tool = BundleItem(Artifact.prehistoric_tool)
chicken_statue = BundleItem(Artifact.chicken_statue)
rusty_cog = BundleItem(Artifact.rusty_cog)
rusty_spur = BundleItem(Artifact.rusty_spur)
rusty_spoon = BundleItem(Artifact.rusty_spoon)
ancient_sword = BundleItem(Artifact.ancient_sword)
ornamental_fan = BundleItem(Artifact.ornamental_fan)
chipped_amphora = BundleItem(Artifact.chipped_amphora)
strange_doll = BundleItem(Artifact.strange_doll)
strange_doll_green = BundleItem(Artifact.strange_doll_green)
ancient_seed = BundleItem(Artifact.ancient_seed)
rare_disc = BundleItem(Artifact.rare_disc)

prehistoric_scapula = BundleItem(Fossil.prehistoric_scapula)
prehistoric_tibia = BundleItem(Fossil.prehistoric_tibia)
prehistoric_skull = BundleItem(Fossil.prehistoric_skull)
skeletal_hand = BundleItem(Fossil.skeletal_hand)
prehistoric_rib = BundleItem(Fossil.prehistoric_rib)
prehistoric_vertebra = BundleItem(Fossil.prehistoric_vertebra)
skeletal_tail = BundleItem(Fossil.skeletal_tail)
nautilus_fossil = BundleItem(Fossil.nautilus_fossil)
amphibian_fossil = BundleItem(Fossil.amphibian_fossil)
palm_fossil = BundleItem(Fossil.palm_fossil)
trilobite = BundleItem(Fossil.trilobite)
snake_vertebrae = BundleItem(Fossil.snake_vertebrae, source=BundleItem.Sources.island)
mummified_bat = BundleItem(Fossil.mummified_bat, source=BundleItem.Sources.island)
fossilized_tail = BundleItem(Fossil.fossilized_tail, source=BundleItem.Sources.island)

dinosaur_mayo = BundleItem(ArtisanGood.dinosaur_mayonnaise)
void_mayo = BundleItem(ArtisanGood.void_mayonnaise)
prismatic_shard = BundleItem(Mineral.prismatic_shard)
diamond = BundleItem(Mineral.diamond)
ancient_fruit = BundleItem(Fruit.ancient_fruit)
void_salmon = BundleItem(Fish.void_salmon)
tea_leaves = BundleItem(Vegetable.tea_leaves)
blobfish = BundleItem(Fish.blobfish)
spook_fish = BundleItem(Fish.spook_fish)
lionfish = BundleItem(Fish.lionfish, source=BundleItem.Sources.island)
blue_discus = BundleItem(Fish.blue_discus, source=BundleItem.Sources.island)
stingray = BundleItem(Fish.stingray, source=BundleItem.Sources.island)
spookfish = BundleItem(Fish.spookfish)
midnight_squid = BundleItem(Fish.midnight_squid)

angler = BundleItem(Fish.angler)
crimsonfish = BundleItem(Fish.crimsonfish)
mutant_carp = BundleItem(Fish.mutant_carp)
glacierfish = BundleItem(Fish.glacierfish)
legend = BundleItem(Fish.legend)

spinner = BundleItem(Fishing.spinner)
dressed_spinner = BundleItem(Fishing.dressed_spinner)
trap_bobber = BundleItem(Fishing.trap_bobber)
sonar_bobber = BundleItem(Fishing.sonar_bobber)
cork_bobber = BundleItem(Fishing.cork_bobber)
lead_bobber = BundleItem(Fishing.lead_bobber)
treasure_hunter = BundleItem(Fishing.treasure_hunter)
barbed_hook = BundleItem(Fishing.barbed_hook)
curiosity_lure = BundleItem(Fishing.curiosity_lure)
quality_bobber = BundleItem(Fishing.quality_bobber)
bait = BundleItem(Fishing.bait, 100)
deluxe_bait = BundleItem(Fishing.deluxe_bait, 50)
magnet = BundleItem(Fishing.magnet)
wild_bait = BundleItem(Fishing.wild_bait, 20)
magic_bait = BundleItem(Fishing.magic_bait, 10, source=BundleItem.Sources.island)
pearl = BundleItem(Gift.pearl)
challenge_bait = BundleItem(Fishing.challenge_bait, 25, source=BundleItem.Sources.masteries)
targeted_bait = BundleItem(ArtisanGood.targeted_bait, 25, source=BundleItem.Sources.content)

ginger = BundleItem(Forageable.ginger, source=BundleItem.Sources.content)
magma_cap = BundleItem(Mushroom.magma_cap, source=BundleItem.Sources.content)

wheat_flour = BundleItem(Ingredient.wheat_flour)
sugar = BundleItem(Ingredient.sugar)
vinegar = BundleItem(Ingredient.vinegar)

jack_o_lantern = BundleItem(Lighting.jack_o_lantern)
prize_ticket = BundleItem(Currency.prize_ticket)
mystery_box = BundleItem(Consumable.mystery_box)
gold_mystery_box = BundleItem(Consumable.gold_mystery_box, source=BundleItem.Sources.masteries)
calico_egg = BundleItem(Currency.calico_egg)
golden_tag = BundleItem(Currency.golden_tag)
stardrop_tea = BundleItem(ArtisanGood.stardrop_tea)
rotten_plant = BundleItem(Decoration.rotten_plant)

apple_slices = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.apple))

infinity_crown = BundleItem(Hats.infinity_crown.name, source=BundleItem.Sources.content)
bowler_hat = BundleItem(Hats.bowler.name, source=BundleItem.Sources.content)
sombrero = BundleItem(Hats.sombrero.name, source=BundleItem.Sources.content)
good_ol_cap = BundleItem(Hats.good_ol_cap.name, source=BundleItem.Sources.content)
living_hat = BundleItem(Hats.living_hat.name, source=BundleItem.Sources.content)
garbage_hat = BundleItem(Hats.garbage_hat.name, source=BundleItem.Sources.content)
golden_helmet = BundleItem(Hats.golden_helmet.name, source=BundleItem.Sources.content)
laurel_wreath_crown = BundleItem(Hats.laurel_wreath_crown.name, source=BundleItem.Sources.content)
joja_cap = BundleItem(Hats.joja_cap.name, source=BundleItem.Sources.content)
deluxe_pirate_hat = BundleItem(Hats.deluxe_pirate_hat.name, source=BundleItem.Sources.content)
dark_cowboy_hat = BundleItem(Hats.dark_cowboy_hat.name, source=BundleItem.Sources.content)
tiger_hat = BundleItem(Hats.tiger_hat.name, source=BundleItem.Sources.content)
mystery_hat = BundleItem(Hats.mystery_hat.name, source=BundleItem.Sources.content)
dark_ballcap = BundleItem(Hats.dark_ballcap.name, source=BundleItem.Sources.content)
goblin_mask = BundleItem(Hats.goblin_mask.name, source=BundleItem.Sources.island)

vacation_shirt = BundleItem(Shirts.vacation.name)
green_jacket_shirt = BundleItem(Shirts.green_jacket.name)

mermaid_boots = BundleItem(Boots.mermaid_boots)

lucky_purple_shorts = BundleItem(SpecialItem.lucky_purple_shorts)

ancient_fruit_wine = BundleItem(ArtisanGood.specific_wine(Fruit.ancient_fruit))
dried_ancient_fruit = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.ancient_fruit))
ancient_fruit_jelly = BundleItem(ArtisanGood.specific_jelly(Fruit.ancient_fruit))
starfruit_wine = BundleItem(ArtisanGood.specific_wine(Fruit.starfruit))
dried_starfruit = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.starfruit))
starfruit_jelly = BundleItem(ArtisanGood.specific_jelly(Fruit.starfruit))
rhubarb_wine = BundleItem(ArtisanGood.specific_wine(Fruit.rhubarb))
dried_rhubarb = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.rhubarb))
melon_wine = BundleItem(ArtisanGood.specific_wine(Fruit.melon))
dried_melon = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.melon))
pineapple_wine = BundleItem(ArtisanGood.specific_wine(Fruit.pineapple), source=BundleItem.Sources.content)
dried_pineapple = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.pineapple), source=BundleItem.Sources.content)
strawberry_wine = BundleItem(ArtisanGood.specific_wine(Fruit.strawberry))
dried_strawberry = BundleItem(ArtisanGood.specific_dried_fruit(Fruit.strawberry))
pumpkin_juice = BundleItem(ArtisanGood.specific_juice(Vegetable.pumpkin))
raisins = BundleItem(ArtisanGood.raisins)

aged_lava_eel_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.lava_eel))
aged_crimsonfish_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.crimsonfish))
aged_angler_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.angler))
legend_roe = BundleItem(AnimalProduct.specific_roe(Fish.legend))
aged_legend_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.legend))
aged_glacierfish_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.glacierfish))
aged_mutant_carp_roe = BundleItem(ArtisanGood.specific_aged_roe(Fish.mutant_carp))

legend_bait = BundleItem(ArtisanGood.specific_bait(Fish.legend))

smoked_legend = BundleItem(ArtisanGood.specific_smoked_fish(Fish.legend))

mystic_syrup = BundleItem(ArtisanGood.mystic_syrup)
apple_sapling = BundleItem(Sapling.apple)
apricot_sapling = BundleItem(Sapling.apricot)
banana_sapling = BundleItem(Sapling.banana, source=BundleItem.Sources.content)
cherry_sapling = BundleItem(Sapling.cherry)
mango_sapling = BundleItem(Sapling.mango, source=BundleItem.Sources.content)
orange_sapling = BundleItem(Sapling.orange)
peach_sapling = BundleItem(Sapling.peach)
pomegranate_sapling = BundleItem(Sapling.pomegranate)

cookout_kit = BundleItem(Craftable.cookout_kit)
tent_kit = BundleItem(Craftable.tent_kit)
bug_steak = BundleItem(Edible.bug_steak)

tea_set = BundleItem(Gift.tea_set)
golden_pumpkin = BundleItem(Gift.golden_pumpkin)
mermaid_pendant = BundleItem(Gift.mermaid_pendant)
advanced_tv_remote = BundleItem(SpecialItem.advanced_tv_remote)

crystal_ball = BundleItem(CatalogueItem.crystal_ball)
amethyst_crystal_ball = BundleItem(CatalogueItem.amethyst_crystal_ball)
aquamarine_crystal_ball = BundleItem(CatalogueItem.aquamarine_crystal_ball)
emerald_crystal_ball = BundleItem(CatalogueItem.emerald_crystal_ball)
ruby_crystal_ball = BundleItem(CatalogueItem.ruby_crystal_ball)
topaz_crystal_ball = BundleItem(CatalogueItem.topaz_crystal_ball)
flute_block = BundleItem(Furniture.flute_block)
candle_lamp = BundleItem(Furniture.candle_lamp)
modern_lamp = BundleItem(Furniture.modern_lamp)
single_bed = BundleItem(Furniture.single_bed)

wood_floor = BundleItem(Floor.wood)
rustic_plank_floor = BundleItem(Floor.rustic)
straw_floor = BundleItem(Floor.straw)
weathered_floor = BundleItem(Floor.weathered)
crystal_floor = BundleItem(Floor.crystal)
stone_floor = BundleItem(Floor.stone)
stone_walkway_floor = BundleItem(Floor.stone_walkway)
brick_floor = BundleItem(Floor.brick)
wood_path = BundleItem(Floor.wood_path)
gravel_path = BundleItem(Floor.gravel_path)
cobblestone_path = BundleItem(Floor.cobblestone_path)
stepping_stone_path = BundleItem(Floor.stepping_stone_path)
crystal_path = BundleItem(Floor.crystal_path)

warp_totem_beach = BundleItem(Consumable.warp_totem_beach)
warp_totem_mountains = BundleItem(Consumable.warp_totem_mountains)
warp_totem_farm = BundleItem(Consumable.warp_totem_farm)
warp_totem_desert = BundleItem(Consumable.warp_totem_desert, source=BundleItem.Sources.content)
warp_totem_island = BundleItem(Consumable.warp_totem_island, source=BundleItem.Sources.island)
rain_totem = BundleItem(Consumable.rain_totem)
treasure_totem = BundleItem(Consumable.treasure_totem, source=BundleItem.Sources.masteries)

death = BundleItem(NotReallyAnItem.death)

camping_stove = BundleItem(MemeItem.camping_stove)
decorative_pot = BundleItem(MemeItem.decorative_pot)
slime_crate = BundleItem(MemeItem.slime_crate)
supply_crate = BundleItem(MemeItem.supply_crate)
warp_totem_qis_arena = BundleItem(MemeItem.warp_totem_qis_arena)
artifact_spot = BundleItem(MemeItem.artifact_spot)
twig = BundleItem(MemeItem.twig)
weeds = BundleItem(MemeItem.weeds)
lumber = BundleItem(MemeItem.lumber)
green_rain_weeds_0 = BundleItem(MemeItem.green_rain_weeds_0)
seed_spot = BundleItem(MemeItem.seed_spot)
pot_of_gold = BundleItem(MemeItem.pot_of_gold)
