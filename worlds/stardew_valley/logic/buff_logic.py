from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from ..options import NumberOfMovementBuffs, NumberOfLuckBuffs
from ..stardew_rule import StardewRule
from ..strings.ap_names.buff_names import Buff


class BuffLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff = BuffLogic(*args, **kwargs)


class BuffLogic(BaseLogic[Union[ReceivedLogicMixin, OptionLogicMixin]]):
    def has_max_buffs(self) -> StardewRule:
        return self.has_max_speed() & self.has_max_luck()

    def has_max_speed(self) -> StardewRule:
        return self.logic.option.received(NumberOfMovementBuffs, Buff.movement)

    def has_max_luck(self) -> StardewRule:
        return self.logic.option.received(NumberOfLuckBuffs, Buff.luck)
