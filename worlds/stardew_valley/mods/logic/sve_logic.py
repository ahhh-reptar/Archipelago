from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...strings.animal_names import Animal
from ...strings.animal_product_names import AnimalProduct
from ...strings.ap_names.mods.mod_items import SVELocation, SVERunes, SVEQuestItem
from ...strings.artisan_good_names import ModArtisanGood
from ...strings.machine_names import Machine
from ...strings.quest_names import Quest, ModQuest
from ...strings.region_names import Region, SVERegion
from ...strings.seed_names import SVESeed
from ...strings.skill_names import Skill
from ...strings.tool_names import Tool
from ...strings.wallet_item_names import Wallet


class SVELogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sve = SVELogic(*args, **kwargs)


class SVELogic(BaseLogic):
    def initialize_rules(self):
        self.registry.sve_location_rules.update({
            SVELocation.tempered_galaxy_sword: self.logic.money.can_spend_at(SVERegion.alesia_shop, 350000),
            SVELocation.tempered_galaxy_dagger: self.logic.money.can_spend_at(SVERegion.isaac_shop, 600000),
            SVELocation.tempered_galaxy_hammer: self.logic.money.can_spend_at(SVERegion.isaac_shop, 400000),
        })
        self.registry.item_rules.update({
            AnimalProduct.sve_goose_egg: self.logic.animal.has_animal(Animal.sve_goose),
            AnimalProduct.sve_golden_goose_egg: self.logic.animal.has_animal(Animal.sve_goose),
            AnimalProduct.sve_honey_jar: self.logic.animal.has_animal(Animal.sve_bear),
            AnimalProduct.sve_camel_fur: self.logic.animal.has_animal(Animal.sve_camel),
            ModArtisanGood.sve_fir_wax: self.logic.has(Machine.tapper),
            ModArtisanGood.sve_birch_water: self.logic.has(Machine.tapper),
            SVESeed.sve_birch_seed: self.logic.skill.has_level(Skill.foraging, 1) & self.logic.ability.can_chop_trees(),
            SVESeed.sve_fir_cone: self.logic.skill.has_level(Skill.foraging, 1) & self.logic.ability.can_chop_trees(),
        })

    def has_any_rune(self):
        rune_list = SVERunes.nexus_items
        return self.logic.or_(*(self.logic.received(rune) for rune in rune_list))

    def has_iridium_bomb(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.iridium_bomb)
        return self.logic.quest.can_complete_quest(ModQuest.RailroadBoulder)

    def has_marlon_boat(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.marlon_boat_paddle)
        return self.logic.quest.can_complete_quest(ModQuest.MarlonsBoat)

    def has_grandpa_shed_repaired(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(SVEQuestItem.grandpa_shed)
        return self.logic.quest.can_complete_quest(ModQuest.GrandpasShed)

    def has_bear_knowledge(self):
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(Wallet.bears_knowledge)
        return self.logic.quest.can_complete_quest(Quest.strange_note)

    def can_buy_bear_recipe(self):
        access_rule = (self.logic.quest.can_complete_quest(Quest.strange_note) & self.logic.tool.has_tool(Tool.axe) &
                       self.logic.tool.has_tool(Tool.pickaxe))
        forage_rule = self.logic.region.can_reach_any(Region.forest, Region.backwoods, Region.mountain)
        knowledge_rule = self.has_bear_knowledge()
        return access_rule & forage_rule & knowledge_rule
