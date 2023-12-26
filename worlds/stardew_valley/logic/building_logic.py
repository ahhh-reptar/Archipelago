from typing import Dict, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .. import options
from ..stardew_rule import StardewRule, True_, Has
from ..strings.ap_names.event_names import Event
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.fish_names import WaterItem
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar


def get_progressive_building_item_name(building):
    count = 1
    if building in [Building.coop, Building.barn, Building.shed]:
        building = f"Progressive {building}"
    elif building.startswith("Big"):
        count = 2
        building = " ".join(["Progressive", *building.split(" ")[1:]])
    elif building.startswith("Deluxe"):
        count = 3
        building = " ".join(["Progressive", *building.split(" ")[1:]])
    return building, count


house_upgrade_by_level = {
    1: Building.kitchen,
    2: Building.kids_room,
    3: Building.cellar,
}


class BuildingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = BuildingLogic(*args, **kwargs)


class BuildingLogic(BaseLogic[Union[BuildingLogicMixin, MoneyLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin, OptionLogicMixin]]):
    def initialize_rules(self):
        self.registry.building_rules.update({
            # @formatter:off
            Building.barn: self.logic.money.can_spend(6000) & self.logic.has((Material.wood, Material.stone)),
            Building.big_barn: self.logic.money.can_spend(12000) & self.logic.has((Material.wood, Material.stone)) & self.logic.building.has_building(Building.barn),
            Building.deluxe_barn: self.logic.money.can_spend(25000) & self.logic.has((Material.wood, Material.stone)) & self.logic.building.has_building(Building.big_barn),
            Building.coop: self.logic.money.can_spend(4000) & self.logic.has((Material.wood, Material.stone)),
            Building.big_coop: self.logic.money.can_spend(10000) & self.logic.has((Material.wood, Material.stone)) & self.logic.building.has_building(Building.coop),
            Building.deluxe_coop: self.logic.money.can_spend(20000) & self.logic.has((Material.wood, Material.stone)) & self.logic.building.has_building(Building.big_coop),
            Building.fish_pond: self.logic.money.can_spend(5000) & self.logic.has((Material.stone, WaterItem.seaweed, WaterItem.green_algae)),
            Building.mill: self.logic.money.can_spend(2500) & self.logic.has((Material.stone, Material.wood, ArtisanGood.cloth)),
            Building.shed: self.logic.money.can_spend(15000) & self.logic.has(Material.wood),
            Building.big_shed: self.logic.money.can_spend(20000) & self.logic.has((Material.wood, Material.stone)) & self.logic.building.has_building(Building.shed),
            Building.silo: self.logic.money.can_spend(100) & self.logic.has((Material.stone, Material.clay, MetalBar.copper)),
            Building.slime_hutch: self.logic.money.can_spend(10000) & self.logic.has((Material.stone, MetalBar.quartz, MetalBar.iridium)),
            Building.stable: self.logic.money.can_spend(10000) & self.logic.has((Material.hardwood, MetalBar.iron)),
            Building.well: self.logic.money.can_spend(1000) & self.logic.has(Material.stone),
            Building.shipping_bin: self.logic.money.can_spend(250) & self.logic.has(Material.wood),
            Building.kitchen: self.logic.money.can_spend(10000) & self.logic.has(Material.wood) & self.logic.building.has_house(0),
            Building.kids_room: self.logic.money.can_spend(50000) & self.logic.has(Material.hardwood) & self.logic.building.has_house(1),
            Building.cellar: self.logic.money.can_spend(100000) & self.logic.building.has_house(2),
            # @formatter:on
        })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.registry.building_rules.update(new_rules)

    def has_carpenter_access(self) -> StardewRule:
        return self.logic.received(Event.can_construct_buildings)

    @cache_self1
    def has_building(self, building: str) -> StardewRule:
        if building is Building.shipping_bin:
            return self.has_shipping_bin()

        progressive_building_rule = self.logic.received(*get_progressive_building_item_name(building)) & self.logic.building.has_carpenter_access()
        non_progressive_building_rule = Has(building, self.registry.building_rules) & self.logic.building.has_carpenter_access()
        return self.logic.option.bitwise_choice(options.BuildingProgression,
                                                value=options.BuildingProgression.option_progressive,
                                                match=progressive_building_rule,
                                                no_match=non_progressive_building_rule)

    def has_shipping_bin(self):
        """
        Shipping bin is special. The mod auto-builds it when received, no need to go to Robin.
        """
        return self.logic.option.bitwise_choice_or_true(options.BuildingProgression,
                                                        value=options.BuildingProgression.option_progressive,
                                                        match=self.logic.received(Building.shipping_bin))

    @cache_self1
    def has_house(self, upgrade_level: int) -> StardewRule:
        assert 0 <= upgrade_level <= 3, "There is only 3 level of house upgrade."

        if upgrade_level == 0:
            return True_()

        progressive_rule = self.logic.received("Progressive House", upgrade_level) & self.logic.building.has_carpenter_access()
        non_progressive_rule = Has(house_upgrade_by_level[upgrade_level], self.registry.building_rules) & self.logic.building.has_carpenter_access()
        return self.logic.option.bitwise_choice(options.BuildingProgression,
                                                value=options.BuildingProgression.option_progressive,
                                                match=progressive_rule,
                                                no_match=non_progressive_rule)
