from typing import Union

from .base_logic import BaseLogic, BaseLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .. import options
from ..stardew_rule import StardewRule, true_
from ..strings.region_names import Region

jotpk_buffs = ("JotPK: Progressive Boots", "JotPK: Progressive Gun", "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate")


class ArcadeLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arcade = ArcadeLogic(*args, **kwargs)


class ArcadeLogic(BaseLogic[Union[ArcadeLogicMixin, RegionLogicMixin, ReceivedLogicMixin, OptionLogicMixin]]):

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        full_shuffling_rule = self.logic.received(jotpk_buffs, power_level)
        return self.logic.option.choose(options.ArcadeMachineLocations,
                                        choices={options.ArcadeMachineLocations.option_full_shuffling: full_shuffling_rule},
                                        default=true_)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        full_shuffling_rule = self.logic.received("Junimo Kart: Extra Life", power_level)
        return self.logic.option.choose(options.ArcadeMachineLocations,
                                        choices={options.ArcadeMachineLocations.option_full_shuffling: full_shuffling_rule},
                                        default=true_)

    def has_junimo_kart_max_level(self) -> StardewRule:
        full_shuffling_rule = self.logic.arcade.has_junimo_kart_power_level(8)
        return self.logic.option.choose(options.ArcadeMachineLocations,
                                        choices={options.ArcadeMachineLocations.option_full_shuffling: full_shuffling_rule},
                                        default=self.logic.region.can_reach(Region.junimo_kart_3))
