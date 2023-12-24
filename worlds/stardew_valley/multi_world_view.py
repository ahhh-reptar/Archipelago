from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from BaseClasses import MultiWorld, Entrance, Location
from worlds.generic import Rules as MultiWorldRules
from .options import StardewValleyOptions
from .stardew_rule import StardewRule


class PlayerWorldView(Protocol):
    """
    Offers a read only view on the multi world, from the player perspective.
    """
    player: int
    options: StardewValleyOptions

    @abstractmethod
    def get_entrance(self, name: str) -> Entrance:
        ...

    @abstractmethod
    def get_location(self, name: str) -> Location:
        ...


@dataclass(frozen=True)
class PlayerMultiWorldAdapter(PlayerWorldView):
    """
    Wrap the usage of the multi world to avoid always needing to pass the player and options context.
    """
    multi_world: MultiWorld

    player: int
    options: StardewValleyOptions

    # Maybe add starting inventory

    # ---=== Entrances & Rules ===---
    def get_entrance(self, name: str) -> Entrance:
        return self.multi_world.get_entrance(name, self.player)

    def get_location(self, name: str) -> Location:
        return self.multi_world.get_location(name, self.player)

    def set_entrance_rule(self, entrance_name: str, rule: StardewRule):
        entrance = self.get_entrance(entrance_name)
        MultiWorldRules.set_rule(entrance, rule)

    def set_location_rule(self, location_name: str, rule: StardewRule):
        location = self.get_location(location_name)
        MultiWorldRules.set_rule(location, rule)

    # FIXME we should not use add, only set so we make sure to always keep the StardewRule.
    def add_entrance_rule(self, entrance_name: str, rule: StardewRule):
        entrance = self.get_entrance(entrance_name)
        MultiWorldRules.add_rule(entrance, rule)

    def add_location_rule(self, location_name: str, rule: StardewRule):
        location = self.get_location(location_name)
        MultiWorldRules.add_rule(location, rule)

    def has_mod(self, name: str) -> bool:
        return name in self.options.mods
