from .. import SVTestBase
from ... import options
from ...mods.mod_data import ModNames


class TestVanillaSkillProgression(SVTestBase):
    options = {
        options.SkillProgression.internal_name: options.SkillProgression.option_vanilla,
        options.Mods.internal_name: ModNames.archaeology
    }

    def test_no_archeology_level_location(self):
        self.assertNotIn("Level 1 Archaeology", self.multiworld.regions.location_cache[1])


class TestProgressiveSkillProgression(SVTestBase):
    options = {
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.Mods.internal_name: ModNames.archaeology
    }

    def test_no_archeology_level_location(self):
        self.assertIn("Level 1 Archaeology", self.multiworld.regions.location_cache[1])
