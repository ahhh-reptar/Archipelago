from . import DungeonClawlerTestBase
from .. import options
from ..constants.character_names import Character
from ..constants.combat_items import CombatItem
from ..locations import character_location_name


class TestAccessibilityRules(DungeonClawlerTestBase):
    options = {options.Goal.internal_name: options.Goal.option_beat_nightmare,
               options.ShuffleCharacters.internal_name: options.ShuffleCharacters.option_true,
               options.ShuffleItems.internal_name: options.ShuffleItems.option_true,
               options.ShufflePerks.internal_name: options.ShufflePerks.option_true,}

    def test_win_with_bunner(self):
        location_name = character_location_name(Character.chief_bunner.name)
        self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

        character_item = self.get_item_by_name(Character.chief_bunner.name)
        self.collect(character_item)

        self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

        self.collect([self.get_item_by_name(CombatItem.dagger.name)] * 20)

        self.assertFalse(self.multiworld.state.can_reach_location(location_name, self.player))

        self.collect(self.get_item_by_name(CombatItem.small_shield.name))
        self.collect(self.get_item_by_name(CombatItem.spikey_shield.name))
        self.collect(self.get_item_by_name(CombatItem.big_shield.name))
        self.collect(self.get_item_by_name(CombatItem.tower_shield.name))
        self.collect(self.get_item_by_name(CombatItem.metal_shield.name))

        self.assertTrue(self.multiworld.state.can_reach_location(location_name, self.player))
