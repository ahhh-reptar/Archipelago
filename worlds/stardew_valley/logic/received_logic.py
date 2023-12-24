from typing import Union, Optional, Tuple, Type

from .base_logic import BaseLogic
from ..options import StardewValleyOption
from ..stardew_rule import StardewRule, True_, Received, And, Or, TotalReceived
from ..stardew_rule.option import OptionReceived


class ReceivedLogicMixin(BaseLogic[None]):

    # Should be cached
    def received(self, items: Union[str, Tuple[str, ...]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            return Received(items, count)

        if count is None:
            return And(*(self.received(item) for item in items))

        if count == 1:
            return Or(*(self.received(item) for item in items))

        return TotalReceived(count, items)

    @staticmethod
    def option_received(item: str, option: Type[StardewValleyOption]) -> StardewRule:
        return OptionReceived(option, item)  # noqa
