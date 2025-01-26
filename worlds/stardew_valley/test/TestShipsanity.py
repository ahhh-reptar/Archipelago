import unittest
from typing import ClassVar, Set

from . import SVTestBase
from .assertion import WorldAssertMixin
from ..content.feature import fishsanity
from ..mods.mod_data import ModNames
from ..options import Fishsanity, ExcludeGingerIsland, Mods, SpecialOrderLocations, Goal, QuestLocations, Shipsanity
from ..strings.fish_names import Fish, SVEFish, DistantLandsFish


class TestShipsanityFishWithoutFishsanity(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_none,
    }

    def test_all_fish_shipping_locations_exist(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for fish in self.world.content.fishes:
            self.assertIn(f"Shipsanity: {fish}", location_names)


class TestShipsanityFishOnlyEasyFish(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_only_easy_fish,
    }

    def test_must_ship_only_fishsanity_fish(self):
        location_names: Set[str] = {location.name for location in self.multiworld.get_locations()}
        fishsanity_prefix = "Fishsanity: "
        fishsanity_locations: Set[str] = {location for location in location_names if location.startswith(fishsanity_prefix)}
        shipsanity_locations: Set[str] = {location for location in location_names if location.startswith("Shipsanity: ")}
        self.assertEqual(len(fishsanity_locations), len(shipsanity_locations))
        for fishsanity_location in fishsanity_locations:
            fish_name = fishsanity_location[len(fishsanity_prefix):]
            self.assertIn(f"Shipsanity: {fish_name}", shipsanity_locations)


class TestShipsanityFishExcludeHardFish(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_exclude_hard_fish,
    }

    def test_must_ship_only_fishsanity_fish(self):
        location_names: Set[str] = {location.name for location in self.multiworld.get_locations()}
        fishsanity_prefix = "Fishsanity: "
        fishsanity_locations: Set[str] = {location for location in location_names if location.startswith(fishsanity_prefix)}
        shipsanity_locations: Set[str] = {location for location in location_names if location.startswith("Shipsanity: ")}
        self.assertEqual(len(fishsanity_locations), len(shipsanity_locations))
        for fishsanity_location in fishsanity_locations:
            fish_name = fishsanity_location[len(fishsanity_prefix):]
            self.assertIn(f"Shipsanity: {fish_name}", shipsanity_locations)


class TestShipsanityFishExcludeLegendaries(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_exclude_legendaries,
    }

    def test_must_ship_only_fishsanity_fish(self):
        location_names: Set[str] = {location.name for location in self.multiworld.get_locations()}
        fishsanity_prefix = "Fishsanity: "
        fishsanity_locations: Set[str] = {location for location in location_names if location.startswith(fishsanity_prefix)}
        shipsanity_locations: Set[str] = {location for location in location_names if location.startswith("Shipsanity: ")}
        self.assertEqual(len(fishsanity_locations), len(shipsanity_locations))
        for fishsanity_location in fishsanity_locations:
            fish_name = fishsanity_location[len(fishsanity_prefix):]
            self.assertIn(f"Shipsanity: {fish_name}", shipsanity_locations)


class TestShipsanityFishOnlyLegendaries(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_legendaries,
    }

    def test_must_ship_only_fishsanity_fish(self):
        location_names: Set[str] = {location.name for location in self.multiworld.get_locations()}
        fishsanity_prefix = "Fishsanity: "
        fishsanity_locations: Set[str] = {location for location in location_names if location.startswith(fishsanity_prefix)}
        shipsanity_locations: Set[str] = {location for location in location_names if location.startswith("Shipsanity: ")}
        self.assertEqual(len(fishsanity_locations), len(shipsanity_locations))
        for fishsanity_location in fishsanity_locations:
            fish_name = fishsanity_location[len(fishsanity_prefix):]
            self.assertIn(f"Shipsanity: {fish_name}", shipsanity_locations)


class TestShipsanityFishAll(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_fish,
        Fishsanity: Fishsanity.option_all,
    }

    def test_must_ship_only_fishsanity_fish(self):
        location_names: Set[str] = {location.name for location in self.multiworld.get_locations()}
        fishsanity_prefix = "Fishsanity: "

        fishsanity_locations: Set[str] = {location for location in location_names if location.startswith(fishsanity_prefix)}
        shipsanity_locations: Set[str] = {location for location in location_names if location.startswith("Shipsanity: ")}
        self.assertEqual(len(fishsanity_locations), len(shipsanity_locations))
        for fishsanity_location in fishsanity_locations:
            fish_name = fishsanity_location[len(fishsanity_prefix):]
            self.assertIn(f"Shipsanity: {fish_name}", shipsanity_locations)
