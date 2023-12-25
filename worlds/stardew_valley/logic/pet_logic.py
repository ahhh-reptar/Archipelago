import math
from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .time_logic import TimeLogicMixin
from .tool_logic import ToolLogicMixin
from .. import options
from ..stardew_rule import StardewRule, True_
from ..strings.region_names import Region
from ..strings.villager_names import NPC

pet_heart_item_name = f"{NPC.pet} <3"


class PetLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pet = PetLogic(*args, **kwargs)


class PetLogic(BaseLogic[Union[RegionLogicMixin, ReceivedLogicMixin, TimeLogicMixin, ToolLogicMixin, OptionLogicMixin]]):
    def has_pet_hearts(self, hearts: int = 1) -> StardewRule:
        assert hearts >= 0, "You can't have negative hearts with a pet."
        if hearts == 0:
            return True_()

        return self.logic.option.choose(options.Friendsanity,
                                        choices={
                                            options.Friendsanity.option_none: self.can_befriend_pet(hearts),
                                            options.Friendsanity.option_bachelors: self.can_befriend_pet(hearts),
                                        },
                                        default=self.received_pet_hearts(hearts))

    def received_pet_hearts(self, hearts: int) -> StardewRule:
        return self.logic.option.received(options.FriendsanityHeartSize,
                                          pet_heart_item_name,
                                          lambda option_value: math.ceil(hearts / option_value))

    def can_befriend_pet(self, hearts: int) -> StardewRule:
        assert hearts >= 0, "You can't have negative hearts with a pet."
        if hearts == 0:
            return True_()

        points = hearts * 200
        points_per_month = 12 * 14
        points_per_water_month = 18 * 14
        farm_rule = self.logic.region.can_reach(Region.farm)
        time_with_water_rule = self.logic.tool.can_water(0) & self.logic.time.has_lived_months(points // points_per_water_month)
        time_without_water_rule = self.logic.time.has_lived_months(points // points_per_month)
        time_rule = time_with_water_rule | time_without_water_rule
        return farm_rule & time_rule
