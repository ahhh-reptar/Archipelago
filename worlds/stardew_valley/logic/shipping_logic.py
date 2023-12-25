from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .. import options
from ..locations import LocationTags, locations_by_tag
from ..stardew_rule import StardewRule, And
from ..strings.ap_names.event_names import Event
from ..strings.building_names import Building

shipsanity_prefix = "Shipsanity: "


class ShippingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shipping = ShippingLogic(*args, **kwargs)


class ShippingLogic(BaseLogic[Union[ReceivedLogicMixin, ShippingLogicMixin, BuildingLogicMixin, RegionLogicMixin, HasLogicMixin, OptionLogicMixin]]):

    @cached_property
    def can_use_shipping_bin(self) -> StardewRule:
        return self.logic.building.has_building(Building.shipping_bin)

    @cache_self1
    def can_ship(self, item: str) -> StardewRule:
        return self.logic.received(Event.can_ship_items) & self.logic.has(item)

    def can_ship_everything(self) -> StardewRule:
        def create_rule(exclude_ginger_island, special_order_locations, mods):
            all_items_to_ship = []
            exclude_island = exclude_ginger_island == options.ExcludeGingerIsland.option_true
            exclude_qi = special_order_locations != options.SpecialOrderLocations.option_board_qi
            mod_list = mods
            for location in locations_by_tag[LocationTags.SHIPSANITY_FULL_SHIPMENT]:
                if exclude_island and LocationTags.GINGER_ISLAND in location.tags:
                    continue
                if exclude_qi and LocationTags.REQUIRES_QI_ORDERS in location.tags:
                    continue
                if location.mod_name and location.mod_name not in mod_list:
                    continue
                all_items_to_ship.append(location.name[len(shipsanity_prefix):])
            return self.logic.building.has_building(Building.shipping_bin) & And(*(self.logic.has(item) for item in all_items_to_ship))

        return self.logic.option.custom_rule(options.ExcludeGingerIsland, options.SpecialOrderLocations, options.Mods,
                                             rule_factory=create_rule)
