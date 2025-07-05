from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ..override import override
from ..vanilla.ginger_island import ginger_island_content_pack as ginger_island_content_pack
from ..vanilla.pelican_town import BuildingNames
from ...data import villagers_data, fish_data
from ...data.animal import Animal, AnimalName
from ...data.building import Building
from ...data.game_item import ItemTag, Tag, CustomRuleSource
from ...data.harvest import ForagingSource, HarvestCropSource
from ...data.monster_data import MonsterSource, register_monster_modification, create_monster
from ...data.requirement import YearRequirement, CombatRequirement, SpecificFriendRequirement, ToolRequirement, \
    SkillRequirement, FishingRequirement, QuestRequirement
from ...data.shop import ShopSource
from ...logic.time_logic import MAX_MONTHS
from ...mods.mod_data import ModNames
from ...strings.artisan_good_names import ArtisanGood, ModArtisanGood
from ...strings.building_names import ModBuilding
from ...strings.craftable_names import ModEdible
from ...strings.crop_names import Fruit, SVEVegetable, SVEFruit
from ...strings.fish_names import WaterItem, SVEWaterItem
from ...strings.flower_names import Flower
from ...strings.food_names import SVEMeal, SVEBeverage
from ...strings.forageable_names import Mushroom, Forageable, SVEForage
from ...strings.gift_names import SVEGift
from ...strings.machine_names import Machine
from ...strings.material_names import Material
from ...strings.metal_names import MetalBar, ModMineral
from ...strings.monster_drop_names import ModLoot
from ...strings.performance_names import Performance
from ...strings.quest_names import ModQuest
from ...strings.region_names import Region, SVERegion
from ...strings.season_names import Season
from ...strings.seed_names import SVESeed
from ...strings.skill_names import Skill
from ...strings.monster_names import ModMonster, MonsterCategory
from ...strings.tool_names import Tool, ToolMaterial
from ...strings.villager_names import ModNPC
from ...strings.wallet_item_names import Wallet

# Used to adapt content not yet moved to content packs to easily detect when SVE and Ginger Island are both enabled.
SVE_GINGER_ISLAND_PACK = ModNames.sve + "+" + ginger_island_content_pack.name


class SVEContentPack(ContentPack):

    def fish_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            content.fishes.pop(fish_data.baby_lunaloo.name)
            content.fishes.pop(fish_data.barred_knifejaw.name)
            content.fishes.pop(fish_data.blue_tang.name)
            content.fishes.pop(fish_data.clownfish.name)
            content.fishes.pop(fish_data.lunaloo.name)
            content.fishes.pop(fish_data.ocean_sunfish.name)
            content.fishes.pop(fish_data.seahorse.name)
            content.fishes.pop(fish_data.shark.name)
            content.fishes.pop(fish_data.shiny_lunaloo.name)
            content.fishes.pop(fish_data.starfish.name)
            content.fishes.pop(fish_data.sea_sponge.name)

            # Remove Highlands fishes at it requires 2 Lance hearts for the quest to access it
            content.fishes.pop(fish_data.daggerfish.name)
            content.fishes.pop(fish_data.diamond_carp.name)
            content.fishes.pop(fish_data.fiber_goby.name)
            content.fishes.pop(fish_data.gemfish.name)
            content.fishes.pop(fish_data.highlands_bass.name)

            # Remove Fable Reef fishes at it requires 8 Lance hearts for the event to access it
            content.fishes.pop(fish_data.arrowhead_shark.name)
            content.fishes.pop(fish_data.torpedo_trout.name)
            content.fishes.pop(fish_data.turretfish.name)
            content.fishes.pop(fish_data.viper_eel.name)

    def villager_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            # Remove Lance if Ginger Island is not in content since he is first encountered in Volcano Forge
            content.villagers.pop(villagers_data.lance.name)

#    def dl_yes_recipe_hook(self, content: StardewContent):
#        if ModNames.distant_lands in content.registered_packs:
#            content.game_items.pop(ModEdible.sve_marsh_tonic)

#    def dl_no_recipe_hook(self, content: StardewContent):
#        if not ModNames.distant_lands in content.registered_packs:
#            content.game_items.pop(ModEdible.svedl_marsh_tonic)

    def harvest_source_hook(self, content: StardewContent):
        content.untag_item(SVESeed.shrub, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.fungus, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.slime, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.stalk, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.void, tag=ItemTag.CROPSANITY_SEED)
        content.untag_item(SVESeed.ancient_fern, tag=ItemTag.CROPSANITY_SEED)
        if ginger_island_content_pack.name not in content.registered_packs:
            # Remove Highlands seeds as these are behind Lance existing.
            content.game_items.pop(SVESeed.void)
            content.game_items.pop(SVEVegetable.void_root)
            content.game_items.pop(SVESeed.stalk)
            content.game_items.pop(SVEFruit.monster_fruit)
            content.game_items.pop(SVESeed.fungus)
            content.game_items.pop(SVEVegetable.monster_mushroom)
            content.game_items.pop(SVESeed.slime)
            content.game_items.pop(SVEFruit.slime_berry)

    def forage_source_hook(selfself, content: StardewContent):
        #content.untag_item(SVEForage.shark_tooth, tag=ItemTag.)  #commenting this line for now because I don't know what tags shark tooth will have
        if ginger_island_content_pack.name not in content.registered_packs:
            # remove highlands/fable reef forage because Lance doesn't exist
            content.game_items.pop(SVEForage.shark_tooth)
            content.game_items.pop(SVEForage.diamond_flower)

    def finalize_hook(self, content: StardewContent):
        if ginger_island_content_pack.name in content.registered_packs:
            content.registered_packs.add(SVE_GINGER_ISLAND_PACK)

#elites
# some of these are technically already accounted for in monster_data.py, but I'll probs try to make these unique kills too instead of just adding new locations for them
# commenting them out for now
sve_swamp_golem = create_monster(ModMonster.sve_swamp_golem, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_swamp_lurk = create_monster(ModMonster.sve_swamp_lurk, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_swamp_putrid_ghost = create_monster(ModMonster.sve_swamp_putrid_ghost, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_swamp_flower_crab = create_monster(ModMonster.sve_swamp_flower_crab, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_poltergeist = create_monster(ModMonster.sve_poltergeist, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_toxic_bubble = create_monster(ModMonster.sve_toxic_bubble, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.galaxy, content_pack=ModNames.sve)
sve_fallen_adventurer = create_monster(ModMonster.sve_fallen_adventurer, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
sve_badlands_serpent = create_monster(ModMonster.sve_badlands_serpent, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
#sve_corrupt_mummy = create_monster(ModMonster.sve_corrupt_mummy, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve) #mummy dangerous I think
#sve_corrupt_spirit = create_monster(ModMonster.sve_corrupt_spirit, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
sve_corrupt_serpent = create_monster(ModMonster.sve_corrupt_serpent, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
#sve_royal_badlands_serpent = create_monster(ModMonster.sve_royal_badlands_serpent, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
sve_sand_scorpion = create_monster(ModMonster.sve_sand_scorpion, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
#sve_dust_spirit = create_monster(ModMonster.sve_dust_spirit, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve) #this doesn't look like a dust spirit anymore, probs needs a rename
#sve_badlands_skeleton = create_monster(ModMonster.sve_badlands_skeleton, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve) #from sprite to stone golem I cut the word dangerous because there weren't other versions anyways
#sve_badlands_skeleton_mage = create_monster(ModMonster.sve_badlands_skeleton_mage, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.galaxy, content_pack=ModNames.sve)
#sve_highlands_shadow_brute = create_monster(ModMonster.sve_highlands_shadow_brute, MonsterCategory.modded, (SVERegion.highlands_cavern,), Performance.galaxy, content_pack=ModNames.sve)
#sve_highlands_shadow_shaman = create_monster(ModMonster.sve_highlands_shadow_shaman, MonsterCategory.modded, (SVERegion.highlands_cavern,), Performance.galaxy, content_pack=ModNames.sve)
sve_highlands_golem = create_monster(ModMonster.sve_highlands_golem, MonsterCategory.modded, (SVERegion.highlands_cavern, SVERegion.highlands_outside), Performance.galaxy, content_pack=ModNames.sve)
sve_gold_crab = create_monster(ModMonster.sve_gold_crab, MonsterCategory.modded, (SVERegion.highlands_cavern,), Performance.galaxy, content_pack=ModNames.sve)
sve_iron_crab = create_monster(ModMonster.sve_iron_crab, MonsterCategory.modded, (SVERegion.highlands_cavern,), Performance.galaxy, content_pack=ModNames.sve)
sve_copper_crab = create_monster(ModMonster.sve_copper_crab, MonsterCategory.modded, (SVERegion.highlands_cavern,), Performance.galaxy, content_pack=ModNames.sve)

#bosses
sve_apophis = create_monster(ModMonster.sve_apophis, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.maximum, content_pack=ModNames.sve)
sve_bully_rex = create_monster(ModMonster.sve_bully_rex, MonsterCategory.modded, (SVERegion.highlands_pond,), Performance.maximum, content_pack=ModNames.sve)
sve_legendary_purple_mushroom = create_monster(ModMonster.sve_legendary_purple_mushroom, MonsterCategory.modded, (SVERegion.forbidden_maze,), Performance.maximum, content_pack=ModNames.sve)
sve_legendary_gold_slime = create_monster(ModMonster.sve_legendary_gold_slime, MonsterCategory.modded, (SVERegion.highlands_pond,), Performance.maximum, content_pack=ModNames.sve)
sve_legendary_sand_scorpion = create_monster(ModMonster.sve_legendary_sand_scorpion, MonsterCategory.modded, (SVERegion.crimson_badlands,), Performance.maximum, content_pack=ModNames.sve)

register_mod_content_pack(SVEContentPack(
    ModNames.sve,
    weak_dependencies=(
        ginger_island_content_pack.name,
        ModNames.jasper,  # To override Marlon and Gunther
        #ModNames.distant_lands, # for the marsh tonic recipe
    ),
    shop_sources={
        SVEGift.aged_blue_moon_wine: (ShopSource(price=28000, shop_region=SVERegion.blue_moon_vineyard),),
        SVEGift.blue_moon_wine: (ShopSource(price=3000, shop_region=SVERegion.blue_moon_vineyard),),
        ModEdible.lightning_elixir: (ShopSource(price=12000, shop_region=SVERegion.galmoran_outpost),),
        ModEdible.barbarian_elixir: (ShopSource(price=22000, shop_region=SVERegion.galmoran_outpost),),
        ModEdible.gravity_elixir: (ShopSource(price=4000, shop_region=SVERegion.galmoran_outpost),),
        SVEMeal.grampleton_orange_chicken: (ShopSource(price=650,
                                                       shop_region=Region.saloon,
                                                       other_requirements=(SpecificFriendRequirement(ModNPC.sophia, 6),)),),
        ModEdible.hero_elixir: (ShopSource(price=8000, shop_region=SVERegion.isaac_shop),),
        ModEdible.aegis_elixir: (ShopSource(price=28000, shop_region=SVERegion.galmoran_outpost),),
        SVEBeverage.sports_drink: (ShopSource(price=750, shop_region=Region.hospital),),
        SVEMeal.stamina_capsule: (ShopSource(price=4000, shop_region=Region.hospital),),
        SVESeed.butternut_squash: (ShopSource(price=90, shop_region=Region.pierre_store),),
        SVESeed.cucumber: (ShopSource(price=150, shop_region=Region.pierre_store),),
        SVESeed.nectarine: (ShopSource(price=6000, shop_region=Region.pierre_store),),
        SVESeed.pear: (ShopSource(price=3200, shop_region=Region.pierre_store),),
        SVESeed.persimmon: (ShopSource(price=8000, shop_region=Region.pierre_store),),
        SVESeed.sweet_potato: (ShopSource(price=134, shop_region=Region.pierre_store),),
        SVESeed.gold_carrot: (ShopSource(items_price=((3, MetalBar.gold),), shop_region=Region.desert),),
        SVESeed.tree_coin: (ShopSource(items_price=((20, ModLoot.supernatural_goo),), shop_region=SVERegion.henchman_backyard),),
    },
    harvest_sources={
        Mushroom.red: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.summer, Season.fall)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.purple: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)),
            ForagingSource(regions=(SVERegion.sprite_spring_cave, SVERegion.junimo_woods), )
        ),
        Mushroom.morel: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.chanterelle: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Flower.tulip: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.blue_jazz: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.summer_spangle: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.sunflower: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.fairy_rose: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.fall,)),),
        Fruit.ancient_fruit: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=Season.not_winter, other_requirements=(YearRequirement(3),)),
            ForagingSource(regions=(SVERegion.sprite_spring_cave,)),
        ),
        Fruit.sweet_gem_berry: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=Season.not_winter, other_requirements=(YearRequirement(3),)),
        ),

        # New items

        ModLoot.green_mushroom: (ForagingSource(regions=(SVERegion.highlands_pond,), seasons=Season.not_winter),),
        ModLoot.ornate_treasure_chest: (ForagingSource(regions=(SVERegion.highlands_outside,),
                                                       other_requirements=(CombatRequirement(Performance.galaxy),
                                                                           ToolRequirement(Tool.axe, ToolMaterial.iron))),),
        ModLoot.swirl_stone: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.galaxy),)),),
        ModLoot.void_soul: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEForage.winter_star_rose: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.winter,)),),
        SVEForage.bearberry: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.winter,)),),
        SVEForage.poison_mushroom: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.summer, Season.fall)),),
        SVEForage.red_baneberry: (ForagingSource(regions=(Region.secret_woods,), seasons=(Season.summer, Season.summer)),),
        SVEForage.ferngill_primrose: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.spring,)),),
        SVEForage.goldenrod: (ForagingSource(regions=(SVERegion.summit,), seasons=(Season.summer, Season.fall)),),
        SVEForage.conch: (ForagingSource(regions=(Region.beach, SVERegion.fable_reef,)),),
        SVEForage.dewdrop_berry: (ForagingSource(regions=(SVERegion.enchanted_grove,)),),
        SVEForage.sand_dollar: (ForagingSource(regions=(Region.beach, SVERegion.fable_reef,), seasons=(Season.spring, Season.summer)),),
        SVEForage.golden_ocean_flower: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        SVEForage.four_leaf_clover: (ForagingSource(regions=(Region.secret_woods, SVERegion.forest_west,), seasons=(Season.summer, Season.fall)),),
        SVEForage.mushroom_colony: (ForagingSource(regions=(Region.secret_woods, SVERegion.junimo_woods, SVERegion.forest_west,), seasons=(Season.fall,)),),
        SVEForage.rusty_blade: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.great),)),),
        SVEForage.rafflesia: (ForagingSource(regions=(Region.secret_woods,), seasons=Season.not_winter),),
        SVEForage.thistle: (ForagingSource(regions=(SVERegion.summit,)),),
        SVEForage.shark_tooth: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        SVEForage.diamond_flower: (ForagingSource(regions=(SVERegion.diamond_cavern,)),),
        SVEForage.swamp_flower: (ForagingSource(regions=(SVERegion.forbidden_maze,), other_requirements =(CombatRequirement(Performance.great),)),),
        ModLoot.void_pebble: (ForagingSource(regions=(SVERegion.crimson_badlands,), other_requirements=(CombatRequirement(Performance.great),)),),
        ModLoot.void_shard: (ForagingSource(regions=(SVERegion.crimson_badlands,),
                                            other_requirements=(CombatRequirement(Performance.galaxy),
                                                                SkillRequirement(Skill.combat, 10),
                                                                YearRequirement(3),)),),
        SVEWaterItem.dulse_seaweed: (ForagingSource(regions=(Region.beach,), other_requirements=(FishingRequirement(Region.beach),)),),

        # Fable Reef
        WaterItem.coral: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        Forageable.rainbow_shell: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        WaterItem.sea_urchin: (ForagingSource(regions=(SVERegion.fable_reef,)),),

        # Crops
        SVESeed.shrub: (ForagingSource(regions=(Region.secret_woods,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.salal_berry: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.shrub, seasons=(Season.spring,)),),
        SVESeed.slime: (ForagingSource(regions=(SVERegion.highlands_outside,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.slime_berry: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.slime, seasons=(Season.spring,)),),
        SVESeed.ancient_fern: (ForagingSource(regions=(Region.secret_woods,)),),
        SVEVegetable.ancient_fiber: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.ancient_fern, seasons=(Season.summer,)),),
        SVESeed.stalk: (ForagingSource(regions=(SVERegion.highlands_outside,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEFruit.monster_fruit: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.stalk, seasons=(Season.summer,)),),
        SVESeed.fungus: (ForagingSource(regions=(SVERegion.highlands_pond,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEVegetable.monster_mushroom: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.fungus, seasons=(Season.fall,)),),
        SVESeed.void: (ForagingSource(regions=(SVERegion.highlands_cavern,), other_requirements=(CombatRequirement(Performance.good),)),),
        SVEVegetable.void_root: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.void, seasons=(Season.winter,)),),
        SVEVegetable.butternut_squash: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.butternut_squash, seasons=(Season.summer,)),),
        SVEVegetable.cucumber: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.cucumber, seasons=(Season.spring,)),),
        SVEFruit.nectarine: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.nectarine, seasons=(Season.summer,)),),
        SVEFruit.pear: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.pear, seasons=(Season.spring,)),),
        SVEFruit.persimmon: (Tag(ItemTag.FRUIT), HarvestCropSource(seed=SVESeed.persimmon, seasons=(Season.fall,)),),
        SVEVegetable.sweet_potato: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.sweet_potato, seasons=(Season.fall,)),),
        SVEVegetable.gold_carrot: (Tag(ItemTag.VEGETABLE), HarvestCropSource(seed=SVESeed.gold_carrot, seasons=(Season.spring,Season.summer,Season.fall,)),),
        SVEFruit.money_bag: (HarvestCropSource(seed=SVESeed.tree_coin, seasons=(Season.spring,Season.summer,Season.fall,Season.winter,)),),

    },
    fishes=(
        fish_data.alligator,
        fish_data.arrowhead_shark, #removed when no ginger island
        fish_data.baby_lunaloo,  # Removed when no ginger island
        fish_data.barred_knifejaw,
        fish_data.blue_tang,
        fish_data.bonefish,
        fish_data.bull_trout,
        fish_data.butterfish,
        fish_data.clownfish,  # Removed when no ginger island
        fish_data.daggerfish,
        fish_data.diamond_carp, #removed when no ginger island
        fish_data.fiber_goby,
        fish_data.frog,
        fish_data.gar,
        fish_data.gemfish,
        fish_data.goldenfish,
        fish_data.goldfish,
        fish_data.grass_carp,
        fish_data.highlands_bass,
        fish_data.king_salmon,
        fish_data.kittyfish,
        fish_data.lunaloo,  # Removed when no ginger island
        fish_data.meteor_carp,
        fish_data.minnow,
        fish_data.ocean_sunfish, #removed when no ginger island
        fish_data.puppyfish,
        fish_data.radioactive_bass,
        fish_data.seahorse,  # Removed when no ginger island
        fish_data.shark, #removed when no ginger island
        fish_data.shiny_lunaloo,  # Removed when no ginger island
        fish_data.snatcher_worm,
        fish_data.starfish,  # Removed when no ginger island
        fish_data.swamp_crab,
        fish_data.tadpole,
        fish_data.torpedo_trout,
        fish_data.turretfish,  #removed when no ginger island
        fish_data.undeadfish,
        fish_data.viper_eel,  #removed when no ginger island
        fish_data.void_eel,
        fish_data.water_grub,
        fish_data.wolf_snapper,
        fish_data.sea_sponge,  # Removed when no ginger island

    ),
    villagers=(
        villagers_data.claire,
        villagers_data.lance,  # Removed when no ginger island
        villagers_data.mommy,
        villagers_data.sophia,
        villagers_data.victor,
        villagers_data.andy,
        villagers_data.apples,
        villagers_data.gunther,
        villagers_data.martin,
        villagers_data.marlon,
        villagers_data.morgan,
        villagers_data.scarlett,
        villagers_data.susan,
        villagers_data.morris,
        villagers_data.henchman,
        override(villagers_data.wizard, bachelor=True, mod_name=ModNames.sve),
    ),
    farm_buildings=(
        Building(
            ModBuilding.sve_winery,
            sources=(
                CustomRuleSource(create_rule=lambda logic: logic.shipping.can_ship(ArtisanGood.wine) & logic.time.has_lived_months(8)),
                ShopSource(
                    shop_region=Region.carpenter,
                    price=500_000,
                    items_price=((25, MetalBar.iridium), (200, Material.hardwood), (30, Machine.keg)),
                ),
            ),
        ),
        Building(
            ModBuilding.sve_premium_barn,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=250_000,
                    items_price=((30, ModArtisanGood.sve_fir_wax), (200, Material.hardwood), (950, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.deluxe_barn,
        ),
        Building(
            ModBuilding.sve_premium_coop,
            sources=(
                ShopSource(
                    shop_region=Region.carpenter,
                    price=200_000,
                    items_price=((20, ModArtisanGood.sve_fir_wax), (125, Material.hardwood), (600, Material.stone))
                ),
            ),
            upgrade_from=BuildingNames.deluxe_coop,
        ),
    ),
    animals=(
        Animal(AnimalName.sve_camel,
               required_building=ModBuilding.sve_premium_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, price=24000),
               )),
        Animal(AnimalName.sve_bear,
               required_building=ModBuilding.sve_premium_barn,
               sources=(
                    CustomRuleSource(create_rule=lambda logic: logic.received(Wallet.bears_knowledge) & logic.bundle.can_complete_community_center
                                                               & logic.money.can_have_earned_total(5000000)),
                    ShopSource(shop_region=Region.ranch, price=28000),
               )),
        Animal(AnimalName.sve_goose,
               required_building=ModBuilding.sve_premium_coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, price=12000),
               )),
    )
))
