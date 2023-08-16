from typing import List

from BaseClasses import ItemClassification, MultiWorld, Item
from . import setup_solo_multiworld, SVTestBase
from .. import locations, items, location_table, options
from ..data.villagers_data import all_villagers_by_name, all_villagers_by_mod_by_name
from ..items import items_by_group, Group
from ..locations import LocationTags
from ..mods.mod_data import ModNames


def get_real_locations(tester: SVTestBase, multiworld: MultiWorld):
    return [location for location in multiworld.get_locations(tester.player) if not location.event]


def get_real_location_names(tester: SVTestBase, multiworld: MultiWorld):
    return [location.name for location in multiworld.get_locations(tester.player) if not location.event]


class TestBaseItemGeneration(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
    }

    def test_all_progression_items_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(weapon.name for weapon in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        items_to_ignore.extend(resource_pack.name for resource_pack in items.items_by_group[Group.RESOURCE_PACK])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = [location for location in get_real_locations(self, self.multiworld) if
                               not location.event]

        self.assertEqual(len(non_event_locations), len(self.multiworld.itempool))

    def test_does_not_create_deprecated_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for deprecated_item in items.items_by_group[items.Group.DEPRECATED]:
            with self.subTest(f"{deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for maximum_one_item in items.items_by_group[items.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_exactly_two_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for exactly_two_item in items.items_by_group[items.Group.EXACTLY_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


class TestNoGingerIslandItemGeneration(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true
    }

    def test_all_progression_items_except_island_are_added_to_the_pool(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        # Ignore all the stuff that the algorithm chooses one of, instead of all, to fulfill logical progression
        items_to_ignore = [event.name for event in items.events]
        items_to_ignore.extend(item.name for item in items.all_items if item.mod_name is not None)
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.SEASON])
        items_to_ignore.extend(season.name for season in items.items_by_group[Group.WEAPON])
        items_to_ignore.extend(baby.name for baby in items.items_by_group[Group.BABY])
        progression_items = [item for item in items.all_items if item.classification is ItemClassification.progression and item.name not in items_to_ignore]
        for progression_item in progression_items:
            with self.subTest(f"{progression_item.name}"):
                if Group.GINGER_ISLAND in progression_item.groups:
                    self.assertNotIn(progression_item.name, all_created_items)
                else:
                    self.assertIn(progression_item.name, all_created_items)

    def test_creates_as_many_item_as_non_event_locations(self):
        non_event_locations = [location for location in get_real_locations(self, self.multiworld) if
                               not location.event]

        self.assertEqual(len(non_event_locations), len(self.multiworld.itempool))

    def test_does_not_create_deprecated_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for deprecated_item in items.items_by_group[items.Group.DEPRECATED]:
            with self.subTest(f"Deprecated item: {deprecated_item.name}"):
                self.assertNotIn(deprecated_item.name, all_created_items)

    def test_does_not_create_more_than_one_maximum_one_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for maximum_one_item in items.items_by_group[items.Group.MAXIMUM_ONE]:
            with self.subTest(f"{maximum_one_item.name}"):
                self.assertLessEqual(all_created_items.count(maximum_one_item.name), 1)

    def test_does_not_create_exactly_two_items(self):
        all_created_items = [item.name for item in self.multiworld.itempool]
        for exactly_two_item in items.items_by_group[items.Group.EXACTLY_TWO]:
            with self.subTest(f"{exactly_two_item.name}"):
                count = all_created_items.count(exactly_two_item.name)
                self.assertTrue(count == 0 or count == 2)


class TestGivenProgressiveBackpack(SVTestBase):
    options = {options.BackpackProgression.internal_name: options.BackpackProgression.option_progressive}

    def test_when_generate_world_then_two_progressive_backpack_are_added(self):
        self.assertEqual(self.multiworld.itempool.count(self.world.create_item("Progressive Backpack")), 2)

    def test_when_generate_world_then_backpack_locations_are_added(self):
        created_locations = {location.name for location in self.multiworld.get_locations(1)}
        backpacks_exist = [location.name in created_locations
                           for location in locations.locations_by_tag[LocationTags.BACKPACK]
                           if location.name != "Premium Pack"]
        all_exist = all(backpacks_exist)
        self.assertTrue(all_exist)


class TestMonstersanityNone(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_none}

    def test_when_generate_world_then_5_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 5)

    def test_when_generate_world_then_zero_specific_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 0)
        self.assertEqual(item_pool.count("Progressive Club"), 0)
        self.assertEqual(item_pool.count("Progressive Dagger"), 0)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_3_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 3)


class TestMonstersanityGoals(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_goals}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)


class TestMonstersanityOnePerCategory(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_one_per_category}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)


class TestMonstersanityProgressive(SVTestBase):
    options = {options.Monstersanity.internal_name: options.Monstersanity.option_progressive_goals}

    def test_when_generate_world_then_no_generic_weapons_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Weapon"), 0)

    def test_when_generate_world_then_5_specific_weapons_of_each_type_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Sword"), 5)
        self.assertEqual(item_pool.count("Progressive Club"), 5)
        self.assertEqual(item_pool.count("Progressive Dagger"), 5)

    def test_when_generate_world_then_2_slingshots_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Slingshot"), 2)

    def test_when_generate_world_then_4_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertEqual(item_pool.count("Progressive Footwear"), 4)

    def test_when_generate_world_then_many_rings_shoes_in_the_pool(self):
        item_pool = [item.name for item in self.multiworld.itempool]
        self.assertIn("Hot Java Ring", item_pool)
        self.assertIn("Wedding Ring", item_pool)
        self.assertIn("Slime Charmer Ring", item_pool)


class TestProgressiveElevator(SVTestBase):
    options = {
        options.ElevatorProgression.internal_name: options.ElevatorProgression.option_progressive,
        options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
    }

    def test_given_access_to_floor_115_when_find_another_elevator_then_has_access_to_floor_120(self):
        items_for_115 = self.generate_items_for_mine_115()
        last_elevator = self.get_item_by_name("Progressive Mine Elevator")
        self.collect(items_for_115)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 115", self.player).can_reach(self.multiworld.state))
        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.collect(last_elevator)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.remove(items_for_115)
        self.remove(last_elevator)

    def test_given_access_to_floor_115_when_find_another_pickaxe_and_sword_then_has_access_to_floor_120(self):
        items_for_115 = self.generate_items_for_mine_115()
        items_for_120 = self.generate_items_for_extra_mine_levels("Progressive Sword")
        self.collect(items_for_115)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 115", self.player).can_reach(self.multiworld.state))
        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.collect(items_for_120)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.remove(items_for_115)
        self.remove(items_for_120)

    def test_given_access_to_floor_115_when_find_another_pickaxe_and_dagger_then_does_not_have_access_to_floor_120(self):
        items_for_115 = self.generate_items_for_mine_115()
        items_for_120 = self.generate_items_for_extra_mine_levels("Progressive Dagger")
        self.collect(items_for_115)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 115", self.player).can_reach(self.multiworld.state))
        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.collect(items_for_120)

        self.assertTrue(self.multiworld.get_region("The Mines - Floor 115", self.player).can_reach(self.multiworld.state))
        self.assertFalse(self.multiworld.get_region("The Mines - Floor 120", self.player).can_reach(self.multiworld.state))

        self.remove(items_for_115)
        self.remove(items_for_120)

    def generate_items_for_mine_115(self) -> List[Item]:
        pickaxes = [self.get_item_by_name("Progressive Pickaxe")] * 2
        elevators = [self.get_item_by_name("Progressive Mine Elevator")] * 22
        swords = [self.get_item_by_name("Progressive Sword")] * 3
        combat_levels = [self.get_item_by_name("Combat Level")] * 4
        guild = self.get_item_by_name("Adventurer's Guild")
        return [*combat_levels, *elevators, guild, *pickaxes, *swords]

    def generate_items_for_extra_mine_levels(self, weapon_name: str) -> List[Item]:
        last_pickaxe = self.get_item_by_name("Progressive Pickaxe")
        last_weapon = self.multiworld.create_item(weapon_name, self.player)
        second_last_combat_level = self.get_item_by_name("Combat Level")
        last_combat_level = self.get_item_by_name("Combat Level")
        return [last_pickaxe, last_weapon, second_last_combat_level, last_combat_level]


class TestLocationGeneration(SVTestBase):

    def test_all_location_created_are_in_location_table(self):
        for location in get_real_locations(self, self.multiworld):
            if not location.event:
                self.assertIn(location.name, location_table)


class TestLocationAndItemCount(SVTestBase):

    def test_minimal_location_maximal_items_still_valid(self):
        min_max_options = self.minimal_locations_maximal_items()
        multiworld = setup_solo_multiworld(min_max_options)
        valid_locations = get_real_locations(self, multiworld)
        self.assertGreaterEqual(len(valid_locations), len(multiworld.itempool))

    def test_allsanity_without_mods_has_at_least_locations(self):
        expected_locations = 1054
        allsanity_options = self.allsanity_options_without_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        real_locations = get_real_locations(self, multiworld)
        number_locations = len(real_locations)
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"Stardew Valley - Allsanity Locations without mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_without_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")

    def test_allsanity_with_mods_has_at_least_locations(self):
        expected_locations = 1306
        allsanity_options = self.allsanity_options_with_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        real_locations = get_real_locations(self, multiworld)
        number_locations = len(real_locations)
        self.assertGreaterEqual(number_locations, expected_locations)
        print(f"\nStardew Valley - Allsanity Locations with all mods: {number_locations}")
        if number_locations != expected_locations:
            print(f"\tNew locations detected!"
                  f"\n\tPlease update test_allsanity_with_mods_has_at_least_locations"
                  f"\n\t\tExpected: {expected_locations}"
                  f"\n\t\tActual: {number_locations}")


class TestFriendsanityNone(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_none,
    }

    def test_no_friendsanity_items(self):
        for item in self.multiworld.itempool:
            self.assertFalse(item.name.endswith(" <3"))

    def test_no_friendsanity_locations(self):
        for location_name in get_real_location_names(self, self.multiworld):
            self.assertFalse(location_name.startswith("Friendsanity"))


class TestFriendsanityBachelors(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_bachelors,
        options.FriendsanityHeartSize.internal_name: 1,
    }
    bachelors = {"Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny",
                 "Maru"}

    def test_friendsanity_only_bachelor_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertIn(villager_name, self.bachelors)

    def test_friendsanity_only_bachelor_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertIn(name, self.bachelors)
                self.assertLessEqual(int(hearts), 8)


class TestFriendsanityStartingNpcs(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_starting_npcs,
        options.FriendsanityHeartSize.internal_name: 1,
    }
    excluded_npcs = {"Leo", "Krobus", "Dwarf", "Sandy", "Kent"}

    def test_friendsanity_only_starting_npcs_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotIn(villager_name, self.excluded_npcs)

    def test_friendsanity_only_starting_npcs_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertNotIn(name, self.excluded_npcs)
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcs(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all,
        options.FriendsanityHeartSize.internal_name: 1,
    }

    def test_friendsanity_all_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcsExcludingGingerIsland(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all,
        options.FriendsanityHeartSize.internal_name: 1,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true
    }

    def test_friendsanity_all_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertNotEqual(villager_name, "Leo")
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertNotEqual(name, "Leo")
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 8)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcsWithMarriage(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 1,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        for item in self.multiworld.itempool:
            if item.name.endswith(suffix):
                villager_name = item.name[:item.name.index(suffix)]
                self.assertTrue(villager_name in all_villagers_by_mod_by_name[ModNames.vanilla] or villager_name == "Pet")

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if location_name.startswith(prefix):
                name_no_prefix = location_name[len(prefix):]
                name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
                parts = name_trimmed.split(" ")
                name = parts[0]
                hearts = parts[1]
                self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
                if name == "Pet":
                    self.assertLessEqual(int(hearts), 5)
                elif all_villagers_by_name[name].bachelor:
                    self.assertLessEqual(int(hearts), 14)
                else:
                    self.assertLessEqual(int(hearts), 10)


class TestFriendsanityAllNpcsWithMarriageHeartSize2(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 2,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 7)
            else:
                self.assertEqual(number_heart_items, 5)
        self.assertEqual(item_names.count("Pet <3"), 3)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 6 or hearts == 8 or hearts == 10 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 2 or hearts == 4 or hearts == 6 or hearts == 8 or hearts == 10)


class TestFriendsanityAllNpcsWithMarriageHeartSize3(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 3,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 5)
            else:
                self.assertEqual(number_heart_items, 4)
        self.assertEqual(item_names.count("Pet <3"), 2)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 3 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 3 or hearts == 6 or hearts == 9 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 3 or hearts == 6 or hearts == 9 or hearts == 10)


class TestFriendsanityAllNpcsWithMarriageHeartSize4(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 4,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 4)
            else:
                self.assertEqual(number_heart_items, 3)
        self.assertEqual(item_names.count("Pet <3"), 2)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 4 or hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 4 or hearts == 8 or hearts == 12 or hearts == 14)
            else:
                self.assertTrue(hearts == 4 or hearts == 8 or hearts == 10)


class TestFriendsanityAllNpcsWithMarriageHeartSize5(SVTestBase):
    options = {
        options.Friendsanity.internal_name: options.Friendsanity.option_all_with_marriage,
        options.FriendsanityHeartSize.internal_name: 5,
    }

    def test_friendsanity_all_with_marriage_items(self):
        suffix = " <3"
        item_names = [item.name for item in self.multiworld.itempool]
        for villager_name in all_villagers_by_mod_by_name[ModNames.vanilla]:
            heart_item_name = f"{villager_name}{suffix}"
            number_heart_items = item_names.count(heart_item_name)
            if all_villagers_by_name[villager_name].bachelor:
                self.assertEqual(number_heart_items, 3)
            else:
                self.assertEqual(number_heart_items, 2)
        self.assertEqual(item_names.count("Pet <3"), 1)

    def test_friendsanity_all_with_marriage_locations(self):
        prefix = "Friendsanity: "
        suffix = " <3"
        for location_name in get_real_location_names(self, self.multiworld):
            if not location_name.startswith(prefix):
                continue
            name_no_prefix = location_name[len(prefix):]
            name_trimmed = name_no_prefix[:name_no_prefix.index(suffix)]
            parts = name_trimmed.split(" ")
            name = parts[0]
            hearts = int(parts[1])
            self.assertTrue(name in all_villagers_by_mod_by_name[ModNames.vanilla] or name == "Pet")
            if name == "Pet":
                self.assertTrue(hearts == 5)
            elif all_villagers_by_name[name].bachelor:
                self.assertTrue(hearts == 5 or hearts == 10 or hearts == 14)
            else:
                self.assertTrue(hearts == 5 or hearts == 10)
