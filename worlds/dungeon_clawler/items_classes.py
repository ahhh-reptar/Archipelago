import enum
from dataclasses import dataclass, field
from typing import Set

from BaseClasses import Item, ItemClassification
from .constants.world_strings import GAME_NAME


class DungeonClawlerItem(Item):
    game: str = GAME_NAME


offset = 0


@dataclass(frozen=True)
class ItemData:
    code_without_offset: offset
    name: str
    classification: ItemClassification

    @property
    def code(self):
        return offset + self.code_without_offset if self.code_without_offset is not None else None
