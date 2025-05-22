from worlds.stardew_valley.test.bases import SVTestBase
from worlds.stardew_valley.options import ExcludeGingerIsland, Booksanity, Shipsanity, Mods
from worlds.stardew_valley.strings.book_names import Book

ModSkillBooks = [Book.digging_like_worms]
ModPowerBooks = []
#ModLostBooks = [] Gonna comment out all the lost book references

class TestModBooksanityNone(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_none,
        Mods: frozenset(Mods.valid_keys)
    }

    def test_no_ModPowerBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_ModSkillBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

#    def test_no_ModLostBooks_locations(self):
#        location_names = {location.name for location in self.multiworld.get_locations()}
#        for book in ModLostBooks:
#            with self.subTest(book):
#                self.assertNotIn(f"Read {book}", location_names)

    def test_no_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertNotIn(f"Power: {book}", item_names)
#        with self.subTest(lost_book):
#            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_modbooks(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestModBooksanityPowers(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power,
        Mods: frozenset(Mods.valid_keys)
    }

    def test_all_ModPowerBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_no_ModSkillBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

 #   def test_no_ModLostBooks_locations(self):
 #       location_names = {location.name for location in self.multiworld.get_locations()}
 #       for book in ModLostBooks:
 #           with self.subTest(book):
 #               self.assertNotIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
#        with self.subTest(lost_book):
#            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityPowersAndSkills(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power_skill,
        Mods: frozenset(Mods.valid_keys)
    }

    def test_all_ModPowerBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_ModSkillBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

#    def test_no_ModLostBooks_locations(self):
#        location_names = {location.name for location in self.multiworld.get_locations()}
#        for book in ModLostBooks:
#            with self.subTest(book):
#                self.assertNotIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
#        with self.subTest(lost_book):
#            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityAll(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_all,
        Mods: frozenset(Mods.valid_keys)
    }

    def test_digging_like_worms_require_2_levels(self):
        state = self.multiworld.state
        read_location = self.world.get_location("Read Digging Like Worms")
        ship_location = self.world.get_location("Shipsanity: Digging Like Worms")
        self.collect("Shipping Bin")

        self.assertFalse(state.can_reach(read_location))
        self.assertFalse(state.can_reach(ship_location))

        self.collect("Archaeology Level")
        self.collect("Archaeology Level")

        self.assertTrue(state.can_reach(read_location))
        self.assertTrue(state.can_reach(ship_location))

    def test_all_ModPowerBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_ModSkillBooks_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

#    def test_all_ModLostBooks_locations(self):
#        location_names = {location.name for location in self.multiworld.get_locations()}
#        for book in ModLostBooks:
#            with self.subTest(book):
#                self.assertIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
#        with self.subTest(lost_book):
#            self.assertIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)
