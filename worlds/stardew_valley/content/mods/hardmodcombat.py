from ... import StardewContent
from .. import ContentPack
from ...data import fish_data
from ...data.game_item import GameItem
from ...data.museum_data import Mineral
from ...mods.mod_data import ModNames
from ...strings.crop_names import SVEFruit, SVEVegetable
from ...strings.forageable_names import SVEForage
from ...strings.monster_drop_names import ModLoot
from ...strings.quest_names import ModQuest
from ...strings.seed_names import SVESeed
from ...strings.special_order_names import ModSpecialOrder


class HardModCombatResources(ContentPack):
    def sve_resources_hook(self, content: StardewContent):
        if ModNames.sve in content.registered_packs:
            content.game_items.pop(SVEForage.swamp_flower)
            content.fishes.pop(fish_data.alligator.name)
            content.fishes.pop(fish_data.bonefish.name)
            content.fishes.pop(fish_data.fiber_goby.name)
            content.fishes.pop(fish_data.highlands_bass.name)
            content.fishes.pop(fish_data.swamp_crab.name)
            content.fishes.pop(fish_data.undeadfish.name)
            content.game_items.pop(SVESeed.tree_coin)  # FIXME add to frontier farm check when that's supported
            content.game_items.pop(ModLoot.green_mushroom)
            content.game_items.pop(ModLoot.ornate_treasure_chest)
            content.game_items.pop(ModLoot.void_soul)
            content.game_items.pop(ModLoot.void_pebble)
            content.game_items.pop(ModLoot.void_shard)
            content.game_items.pop(ModLoot.supernatural_goo)
            content.game_items.pop(ModLoot.swamp_essence)
            content.game_items.pop(SVESeed.shrub)
            content.game_items.pop(SVEFruit.salal_berry)
            content.game_items.pop(SVESeed.slime)
            content.game_items.pop(SVEFruit.slime_berry)
            content.game_items.pop(SVESeed.stalk)
            content.game_items.pop(SVEFruit.monster_fruit)
            content.game_items.pop(SVESeed.fungus)
            content.game_items.pop(SVEVegetable.monster_mushroom)
            content.game_items.pop(SVESeed.void)
            content.game_items.pop(SVEVegetable.void_root)
            content.game_items.pop(SVEFruit.money_bag) #FIXME add to frontier farm section when that's supported
            content.quests.pop(ModSpecialOrder.goblin_in_need)


class HardModCombatElites(ContentPack):
    def elite_drops_hook(self, content: StardewContent):
        if ModNames.sve in content.registered_packs:
            content.game_items.pop(SVEForage.rusty_blade)
            content.game_items.pop(ModLoot.swirl_stone)

class HardModCombatBosses(ContentPack):
    def boss_drops_hook(self, content: StardewContent):
        if ModNames.sve in content.registered_packs:
            content.game_items.pop(Mineral.galdoran_gem.name)
            content.game_items.pop(ModLoot.magic_lamp)
            content.game_items.pop(ModLoot.gold_slime_egg)
            content.game_items.pop(ModLoot.mega_purple_mushroom)
            content.quests.pop(ModQuest.LegendaryTrio)