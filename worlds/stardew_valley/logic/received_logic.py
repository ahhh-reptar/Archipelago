from typing import Union, Optional, Tuple

from BaseClasses import ItemClassification
from .base_logic import BaseLogic
from .. import item_table
from ..stardew_rule import StardewRule, True_, Received, And, Or, TotalReceived


class ReceivedLogicMixin(BaseLogic[None]):

    # Should be cached
    def received(self, items: Union[str, Tuple[str, ...]], count: Optional[int] = 1) -> StardewRule:
        if count <= 0 or not items:
            return True_()

        if isinstance(items, str):
            assert item_table[items].classification & ItemClassification.progression, f"Item [{items}] has to be progression to be used in logic"
            return Received(items, count)

        if count is None:
            return And(*(self.received(item) for item in items))

        if count == 1:
            return Or(*(self.received(item) for item in items))

        return TotalReceived(count, items)
