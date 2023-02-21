from argparse import Namespace
from typing import Optional, Dict

from BaseClasses import MultiWorld
from test.TestBase import WorldTestBase
from test.general import gen_steps
from .. import StardewValleyWorld
from ...AutoWorld import call_all


class SVTestBase(WorldTestBase):
    game = "Stardew Valley"
    world: StardewValleyWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        self.world = self.multiworld.worlds[self.player]


# Literally a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(world_type, test_options: Optional[Dict] = {}) -> MultiWorld:
    multiworld = MultiWorld(1)
    multiworld.game[1] = world_type.game
    multiworld.player_name = {1: "Tester"}
    multiworld.set_seed()
    args = Namespace()
    for name, option in world_type.option_definitions.items():
        value = option(test_options[name]) if name in test_options else option.from_any(option.default)
        setattr(args, name, {1: value})
    multiworld.set_options(args)
    multiworld.set_default_common_options()
    for step in gen_steps:
        call_all(multiworld, step)
    return multiworld
