from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule, True_


class BuffLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff = BuffLogic(*args, **kwargs)


class BuffLogic(BaseLogic[Union[ReceivedLogicMixin]]):
    def has_max_buffs(self) -> StardewRule:
        return self.has_max_speed() & self.has_max_luck()

    def has_max_speed(self) -> StardewRule:
        return True_()

    def has_max_luck(self) -> StardewRule:
        return True_()
