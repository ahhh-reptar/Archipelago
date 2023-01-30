from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Union, Optional, Iterable, Sized, Tuple, List

from BaseClasses import CollectionState, ItemClassification
from . import options
from .bundle_data import BundleItem
from .items import all_items, Group, item_table
from .options import StardewOptions

MISSING_ITEM = "THIS ITEM IS MISSING"

tool_materials = {
    "Copper": 1,
    "Iron": 2,
    "Gold": 3,
    "Iridium": 4
}

tool_prices = {
    "Copper": 2000,
    "Iron": 5000,
    "Gold": 10000,
    "Iridium": 25000
}

skill_level_per_season = {
    "Spring": {
        "Farming": 2,
        "Fishing": 2,
        "Foraging": 2,
        "Mining": 2,
        "Combat": 2,
    },
    "Summer": {
        "Farming": 4,
        "Fishing": 4,
        "Foraging": 4,
        "Mining": 4,
        "Combat": 3,
    },
    "Fall": {
        "Farming": 7,
        "Fishing": 5,
        "Foraging": 5,
        "Mining": 5,
        "Combat": 4,
    },
    "Winter": {
        "Farming": 7,
        "Fishing": 7,
        "Foraging": 6,
        "Mining": 7,
        "Combat": 5,
    },
    "Year Two": {
        "Farming": 10,
        "Fishing": 10,
        "Foraging": 10,
        "Mining": 10,
        "Combat": 10,
    },
}
season_per_skill_level: Dict[Tuple[str, int], str] = {}
season_per_total_level: Dict[int, str] = {}


def initialize_season_per_skill_level():
    current_level = {
        "Farming": 0,
        "Fishing": 0,
        "Foraging": 0,
        "Mining": 0,
        "Combat": 0,
    }
    for season, skills in skill_level_per_season.items():
        for skill, expected_level in skills.items():
            for level_up in range(current_level[skill] + 1, expected_level + 1):
                skill_level = (skill, level_up)
                if skill_level not in season_per_skill_level:
                    season_per_skill_level[skill_level] = season
        level_up = 0
        for level_up in range(level_up + 1, sum(skills.values()) + 1):
            if level_up not in season_per_total_level:
                season_per_total_level[level_up] = season


initialize_season_per_skill_level()


class StardewRule:
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other) -> StardewRule:
        if isinstance(other, _Or):
            return _Or(self, *other.rules)

        return _Or(self, other)

    def __and__(self, other) -> StardewRule:
        if isinstance(other, _And):
            return _And(other.rules.union({self}))

        return _And(self, other)

    def get_difficulty(self):
        raise NotImplementedError

    def simplify(self) -> StardewRule:
        return self


class _True(StardewRule):

    def __new__(cls, _cache=[]):  # noqa
        if not _cache:
            _cache.append(super(_True, cls).__new__(cls))
        return _cache[0]

    def __call__(self, state: CollectionState) -> bool:
        return True

    def __or__(self, other) -> StardewRule:
        return self

    def __and__(self, other) -> StardewRule:
        return other

    def __repr__(self):
        return "True"

    def get_difficulty(self):
        return 0


class _False(StardewRule):

    def __new__(cls, _cache=[]):  # noqa
        if not _cache:
            _cache.append(super(_False, cls).__new__(cls))
        return _cache[0]

    def __call__(self, state: CollectionState) -> bool:
        return False

    def __or__(self, other) -> StardewRule:
        return other

    def __and__(self, other) -> StardewRule:
        return self

    def __repr__(self):
        return "False"

    def get_difficulty(self):
        return 999999999


class _Or(StardewRule):
    rules: frozenset[StardewRule]

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = set()
        if isinstance(rule, Iterable):
            rules_list.update(rule)
        else:
            rules_list.add(rule)

        if rules is not None:
            rules_list.update(rules)

        assert rules_list, "Can't create a Or conditions without rules"

        new_rules = set()
        for rule in rules_list:
            if isinstance(rule, _Or):
                new_rules.update(rule.rules)
            else:
                new_rules.add(rule)
        rules_list = new_rules

        self.rules = frozenset(rules_list)

    def __call__(self, state: CollectionState) -> bool:
        return any(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' | '.join(repr(rule) for rule in self.rules)})"

    def __or__(self, other):
        if isinstance(other, _True):
            return other
        if isinstance(other, _False):
            return self
        if isinstance(other, _Or):
            return _Or(self.rules.union(other.rules))

        return _Or(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return min(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if any(isinstance(rule, _True) for rule in self.rules):
            return _True()

        simplified_rules = {rule.simplify() for rule in self.rules}
        simplified_rules = {rule for rule in simplified_rules if rule is not _False()}

        if not simplified_rules:
            return _False()

        if len(simplified_rules) == 1:
            return next(iter(simplified_rules))

        return _Or(simplified_rules)


class _And(StardewRule):
    rules: frozenset[StardewRule]

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = set()
        if isinstance(rule, Iterable):
            rules_list.update(rule)
        else:
            rules_list.add(rule)

        if rules is not None:
            rules_list.update(rules)

        assert rules_list, "Can't create a And conditions without rules"

        new_rules = set()
        for rule in rules_list:
            if isinstance(rule, _And):
                new_rules.update(rule.rules)
            else:
                new_rules.add(rule)
        rules_list = new_rules

        self.rules = frozenset(rules_list)

    def __call__(self, state: CollectionState) -> bool:
        return all(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' & '.join(repr(rule) for rule in self.rules)})"

    def __and__(self, other):
        if isinstance(other, _True):
            return self
        if isinstance(other, _False):
            return other
        if isinstance(other, _And):
            return _And(self.rules.union(other.rules))

        return _And(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return max(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if any(isinstance(rule, _False) for rule in self.rules):
            return _False()

        simplified_rules = {rule.simplify() for rule in self.rules}
        simplified_rules = {rule for rule in simplified_rules if rule is not _True()}

        if not simplified_rules:
            return _True()

        if len(simplified_rules) == 1:
            return next(iter(simplified_rules))

        return _And(simplified_rules)


class _Count(StardewRule):
    count: int
    rules: List[StardewRule]

    def __init__(self, count: int, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = []
        if isinstance(rule, Iterable):
            rules_list.extend(rule)
        else:
            rules_list.append(rule)

        if rules is not None:
            rules_list.extend(rules)

        assert rules_list, "Can't create a Count conditions without rules"
        assert len(rules_list) >= count, "Count need at least as many rules at the count"

        self.rules = rules_list
        self.count = count

    def __call__(self, state: CollectionState) -> bool:
        c = 0
        for r in self.rules:
            if r(state):
                c += 1
            if c >= self.count:
                return True
        return False

    def __repr__(self):
        return f"Received {self.count} {repr(self.rules)}"

    def get_difficulty(self):
        rules_sorted_by_difficulty = sorted(self.rules, key=lambda x: x.get_difficulty())
        easiest_n_rules = rules_sorted_by_difficulty[0:self.count]
        return max(rule.get_difficulty() for rule in easiest_n_rules)

    def simplify(self):
        return _Count(self.count, [rule.simplify() for rule in self.rules])


class _TotalReceived(StardewRule):
    count: int
    items: Iterable[str]
    player: int

    def __init__(self, count: int, items: Union[str, Iterable[str]], player: int):
        items_list = []
        if isinstance(items, Iterable):
            items_list.extend(items)
        else:
            items_list.append(items)

        assert items_list, "Can't create a Total Received conditions without items"
        for item in items_list:
            assert item_table[item].classification & ItemClassification.progression, \
                "Item has to be progression to be used in logic"

        self.player = player
        self.items = items_list
        self.count = count

    def __call__(self, state: CollectionState) -> bool:
        c = 0
        for item in self.items:
            c += state.count(item, self.player)
            if c >= self.count:
                return True
        return False

    def __repr__(self):
        return f"Received {self.count} {self.items}"

    def get_difficulty(self):
        return self.count


@dataclass(frozen=True)
class _Received(StardewRule):
    item: str
    player: int
    count: int

    def __post_init__(self):
        assert item_table[self.item].classification & ItemClassification.progression, \
            "Item has to be progression to be used in logic"

    def __call__(self, state: CollectionState) -> bool:
        return state.has(self.item, self.player, self.count)

    def __repr__(self):
        if self.count == 1:
            return f"Received {self.item}"
        return f"Received {self.count} {self.item}"

    def get_difficulty(self):
        if self.item == "Spring":
            return 0
        if self.item == "Summer":
            return 1
        if self.item == "Fall":
            return 2
        if self.item == "Winter":
            return 3
        if self.item == "Year Two":
            return 4
        return self.count


@dataclass(frozen=True)
class _Reach(StardewRule):
    spot: str
    resolution_hint: str
    player: int

    def __call__(self, state: CollectionState) -> bool:
        return state.can_reach(self.spot, self.resolution_hint, self.player)

    def __repr__(self):
        return f"Reach {self.resolution_hint} {self.spot}"

    def get_difficulty(self):
        return 1


@dataclass(frozen=True)
class _Has(StardewRule):
    item: str
    # For sure there is a better way than just passing all the rules everytime
    other_rules: Dict[str, StardewRule]

    def __call__(self, state: CollectionState) -> bool:
        if isinstance(self.item, str):
            return self.other_rules[self.item](state)

    def __repr__(self):
        if not self.item in self.other_rules:
            return f"Has {self.item} -> {MISSING_ITEM}"
        return f"Has {self.item} -> {repr(self.other_rules[self.item])}"

    def get_difficulty(self):
        return self.other_rules[self.item].get_difficulty() + 1

    def __hash__(self):
        return hash(self.item)

    def simplify(self) -> StardewRule:
        return self.other_rules[self.item].simplify()


@dataclass(frozen=True)
class StardewLogic:
    player: int
    options: StardewOptions

    item_rules: Dict[str, StardewRule] = field(default_factory=dict)
    building_rules: Dict[str, StardewRule] = field(default_factory=dict)
    quest_rules: Dict[str, StardewRule] = field(default_factory=dict)

    def __post_init__(self):
        self.item_rules.update({
            "Aged Roe": self.has("Preserves Jar") & self.has("Roe"),
            "Albacore": (self.received("Fall") | self.received("Winter")) & self.can_fish(60),
            "Algae Soup": self.can_cook() & self.has("Green Algae") & self.can_have_relationship("Clint", 3),
            "Amaranth": self.received("Fall"),
            "Amethyst": self.can_mine_in_the_mines_floor_1_40(),
            "Anchovy": self.can_fish(30) & (self.received("Spring") | self.received("Fall")),
            "Ancient Drum": self.has("Frozen Geode"),
            "Any Egg": self.has("Chicken Egg") | self.has("Duck Egg"),
            "Apple": self.received("Fall"),
            "Apricot": self.received("Year Two"),
            "Aquamarine": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Artichoke": self.received("Year Two") & self.received("Fall"),
            "Bait": self.has_skill_level("Fishing", 2),
            "Bat Wing": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Battery Pack": self.has("Lightning Rod"),
            "Bee House": self.has_skill_level("Farming", 3) & self.has("Iron Bar") & self.has("Maple Syrup"),
            "Beer": (self.has("Keg") & self.has("Wheat")) | self.can_spend_money(400),
            "Beet": self.received("Fall") & self.can_reach_region("The Desert"),
            "Blackberry": self.received("Fall"),
            "Blue Jazz": self.received("Spring"),
            "Blueberry": self.received("Summer"),
            "Blueberry Tart": self.has("Blueberry") & self.has("Any Egg") & self.can_have_relationship("Pierre", 3),
            "Bok Choy": self.received("Fall"),
            "Bouquet": self.can_have_relationship("Any", 8),
            "Bread": self.can_spend_money(120) | (self.can_spend_money(100) & self.can_cook()),
            "Bream": self.can_fish(35),
            "Broken CD": self.can_crab_pot(),
            "Broken Glasses": self.can_crab_pot(),
            "Bug Meat": self.can_mine_in_the_mines_floor_1_40(),
            "Bullhead": self.can_fish(46),
            "Cactus Fruit": self.can_reach_region("The Desert"),
            "Carp": self.can_fish(15) & (self.received("Spring") | self.received("Summer") | self.received("Fall") |
                                         self.can_reach_region("Secret Woods")),
            "Catfish": self.can_fish(75) & (self.received("Spring") |
                                            self.received("Fall") |
                                            (self.received("Summer") & self.can_reach_region("Secret Woods")) |
                                            (self.received("Winter") & self.has("Rain Totem"))),
            "Cauliflower": self.received("Spring"),
            "Cave Carrot": self.has_mine_elevator_to_floor(10),
            "Caviar": self.has("Preserves Jar") & self.has("Sturgeon Roe"),
            "Chanterelle": self.received("Fall") & self.can_reach_region("Secret Woods"),
            "Cheese Press": self.has_skill_level("Farming", 6) & self.has("Hardwood") & self.has("Copper Bar"),
            "Cheese": (self.has("Cow Milk") & self.has("Cheese Press")) |
                      (self.can_reach_region("The Desert") & self.has("Emerald")),
            "Cheese Cauliflower": self.has(["Cheese", "Cauliflower"]) & self.can_have_relationship("Pam", 3) &
                                  self.can_cook(),
            "Cherry": self.received("Year Two"),
            "Chicken": self.has_building("Coop"),
            "Chicken Egg": self.has(["Egg", "Egg (Brown)", "Large Egg", "Large Egg (Brown)"], 1),
            "Chowder": self.can_cook() & self.can_have_relationship("Willy", 3) & self.has(["Clam", "Cow Milk"]),
            "Chub": self.can_fish(35),
            "Clam": _True(),
            "Clay": _True(),
            "Cloth": (self.has("Wool") & self.has("Loom")) |
                     (self.can_reach_region("The Desert") & self.has("Aquamarine")),
            "Coal": _True(),
            "Cockle": _True(),
            "Coconut": self.can_reach_region("The Desert"),
            "Coffee": (self.has("Keg") & self.has("Coffee Bean")) | self.has("Coffee Maker") |
                      self.can_spend_money(300) | self.has("Hot Java Ring"),
            "Coffee Bean": (self.received("Spring") | self.received("Summer")) &
                           (self.can_mine_in_the_mines_floor_41_80() | _True()),  # Travelling merchant
            "Coffee Maker": _False(),
            "Common Mushroom": self.received("Fall") |
                               (self.received("Spring") & self.can_reach_region("Secret Woods")),
            "Copper Bar": self.can_smelt("Copper Ore"),
            "Copper Ore": self.can_mine_in_the_mines_floor_1_40() | self.can_mine_in_the_skull_cavern(),
            "Coral": self.can_reach_region("Tide Pools") | self.received("Summer"),
            "Corn": self.received("Summer") | self.received("Fall"),
            "Cow": self.has_building("Barn"),
            "Cow Milk": self.has("Milk") | self.has("Large Milk"),
            "Crab": self.can_crab_pot(),
            "Crab Pot": self.has_skill_level("Fishing", 3),
            "Cranberries": self.received("Fall"),
            "Crayfish": self.can_crab_pot(),
            "Crocus": self.received("Winter"),
            "Crystal Fruit": self.received("Winter"),
            "Daffodil": self.received("Spring"),
            "Dandelion": self.received("Spring"),
            "Dish O' The Sea": self.can_cook() & self.has_skill_level("Fishing", 3) &
                               self.has(["Sardine", "Hashbrowns"]),
            "Dorado": self.can_fish(78) & self.received("Summer"),
            "Dried Starfish": self.can_fish(),
            "Driftwood": self.can_crab_pot(),
            "Duck Egg": self.has("Duck"),
            "Duck Feather": self.has("Duck"),
            "Duck": self.has_building("Big Coop"),
            "Dwarf Scroll I": self.can_mine_in_the_mines_floor_1_40(),
            "Dwarf Scroll II": self.can_mine_in_the_mines_floor_1_40(),
            "Dwarf Scroll III": self.can_mine_in_the_mines_floor_1_40(),
            "Dwarf Scroll IV": self.can_mine_in_the_mines_floor_81_120(),
            "Earth Crystal": self.can_mine_in_the_mines_floor_1_40(),
            "Eel": self.can_fish(70) & (self.received("Spring") | self.received("Fall")),
            "Egg": self.has("Chicken"),
            "Egg (Brown)": self.has("Chicken"),
            "Eggplant": self.received("Fall"),
            "Elvish Jewelry": self.can_fish(),
            "Emerald": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Fairy Rose": self.received("Fall"),
            "Farmer's Lunch": self.can_cook() & self.has_skill_level("Farming", 3) & self.has("Omelet") & self.has(
                "Parsnip"),
            "Fiber": _True(),
            "Fiddlehead Fern": self.can_reach_region("Secret Woods") & self.received("Summer"),
            "Fire Quartz": self.can_mine_in_the_mines_floor_81_120(),
            "Flounder": self.can_fish(50),
            "Fried Egg": self.can_cook() & self.has("Any Egg"),
            "Fried Mushroom": self.can_cook() & self.can_have_relationship("Demetrius", 3) & self.has(
                "Morel") & self.has("Common Mushroom"),
            "Frozen Geode": self.can_mine_in_the_mines_floor_41_80(),
            "Frozen Tear": self.can_mine_in_the_mines_floor_41_80(),
            "Furnace": self.has("Stone") & self.has("Copper Ore"),
            "Geode": self.can_mine_in_the_mines_floor_1_40(),
            "Ghostfish": self.can_fish(50) & (
                    self.has_mine_elevator_to_floor(20) | self.has_mine_elevator_to_floor(60)),
            "Goat Cheese": self.has("Goat Milk") & self.has("Cheese Press"),
            "Goat Milk": self.has("Goat"),
            "Goat": self.has_building("Big Barn"),
            "Gold Bar": self.can_smelt("Gold Ore"),
            "Gold Ore": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Grape": self.received("Summer"),
            "Green Algae": self.can_fish(),
            "Green Bean": self.received("Spring"),
            "Halibut": self.can_fish(50) & (
                    self.received("Spring") | self.received("Summer") | self.received("Winter")),
            "Hardwood": self.has_tool("Axe", "Copper"),
            "Hashbrowns": self.can_cook() & self.can_spend_money(50) & self.has("Potato"),
            "Hazelnut": self.received("Fall"),
            "Herring": self.can_fish(25) & (self.received("Spring") | self.received("Winter")),
            "Holly": self.received("Winter"),
            "Honey": self.can_reach_region("The Desert") |
                     (self.has("Bee House") &
                      (self.received("Spring") | self.received("Summer") | self.received("Fall"))),
            "Hops": self.received("Summer"),
            "Hot Java Ring": self.can_reach_region("Ginger Island"),
            "Hot Pepper": self.received("Summer"),
            "Ice Pip": self.can_fish(85),
            "Iridium Bar": self.can_smelt("Iridium Ore"),
            "Iridium Ore": self.can_mine_in_the_skull_cavern(),
            "Iron Bar": self.can_smelt("Iron Ore"),
            "Iron Ore": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Jade": self.can_mine_in_the_mines_floor_41_80(),
            "Jelly": self.has("Preserves Jar"),
            "JotPK Small Buff": self.has_jotpk_power_level(2),
            "JotPK Medium Buff": self.has_jotpk_power_level(4),
            "JotPK Big Buff": self.has_jotpk_power_level(7),
            "JotPK Max Buff": self.has_jotpk_power_level(9),
            "Juice": self.has("Keg"),
            "Junimo Kart Small Buff": self.has_junimo_kart_power_level(2),
            "Junimo Kart Medium Buff": self.has_junimo_kart_power_level(4),
            "Junimo Kart Big Buff": self.has_junimo_kart_power_level(5),
            "Junimo Kart Max Buff": self.has_junimo_kart_power_level(6),
            "Kale": self.received("Spring"),
            "Keg": self.has_skill_level("Farming", 8) & self.has("Iron Bar") & self.has("Copper Bar") & self.has(
                "Oak Resin"),
            "Largemouth Bass": self.can_fish(50),
            "Large Egg": self.has("Chicken"),
            "Large Egg (Brown)": self.has("Chicken"),
            "Large Goat Milk": self.has("Goat"),
            "Large Milk": self.has("Cow"),
            "Lava Eel": self.can_mine_to_floor(100) & self.can_fish(90),
            "Leek": self.received("Spring"),
            "Lightning Rod": self.has_skill_level("Foraging", 6),
            "Lingcod": self.can_fish(85) & self.received("Winter"),
            "Lobster": self.can_crab_pot(),
            "Loom": self.has_skill_level("Farming", 7) & self.has("Pine Tar"),
            "Magma Geode": self.can_mine_in_the_mines_floor_81_120() |
                           (self.has("Lava Eel") & self.has_building("Fish Pond")),
            "Maki Roll": self.can_cook() & self.can_fish(),
            "Maple Syrup": self.has("Tapper"),
            "Mead": self.has("Keg") & self.has("Honey"),
            "Melon": self.received("Summer"),
            "Midnight Carp": self.can_fish(55) & (self.received("Fall") | self.received("Winter")),
            "Milk": self.has("Cow"),
            "Miner's Treat": self.can_cook() & self.has_skill_level("Mining", 3) & self.has("Cow Milk") & self.has(
                "Cave Carrot"),
            "Morel": self.can_reach_region("Secret Woods") & self.received("Year Two"),
            "Mussel": _True(),
            "Nautilus Shell": self.received("Winter"),
            "Oak Resin": self.has("Tapper"),
            "Octopus": self.can_fish(95) & self.received("Summer"),
            "Oil Maker": self.has_skill_level("Farming", 8) & self.has("Hardwood") & self.has("Gold Bar"),
            "Omelet": self.can_cook() & self.can_spend_money(100) & self.has("Any Egg") & self.has("Cow Milk"),
            "Omni Geode": self.can_mine_in_the_mines_floor_41_80() |
                          self.can_reach_region("The Desert") |
                          self.can_do_panning() |
                          self.received("Rusty Key") |
                          (self.has("Octopus") & self.has_building("Fish Pond")) |
                          self.can_reach_region("Ginger Island"),
            "Orange": self.received("Summer"),
            "Ostrich": self.has_building("Barn"),
            "Oyster": _True(),
            "Pale Ale": self.has("Keg") & self.has("Hops"),
            "Pale Broth": self.can_cook() & self.can_have_relationship("Marnie", 3) & self.has("White Algae"),
            "Pancakes": self.can_cook() & self.can_spend_money(100) & self.has("Any Egg"),
            "Parsnip": self.received("Spring"),
            "Parsnip Soup": self.can_cook() & self.can_have_relationship("Caroline", 3) & self.has(
                "Parsnip") & self.has("Cow Milk"),
            "Peach": self.received("Summer"),
            "Pepper Poppers": self.can_cook() & self.has("Cheese") & self.has(
                "Hot Pepper") & self.can_have_relationship("Shane", 3),
            "Perch": self.can_fish(35) & self.received("Winter"),
            "Periwinkle": self.can_crab_pot(),
            "Pickles": self.has("Preserves Jar"),
            "Pig": self.has_building("Deluxe Barn"),
            "Pike": self.can_fish(60) & (self.received("Summer") | self.received("Winter")),
            "Pine Tar": self.has("Tapper"),
            "Pizza": self.can_spend_money(600),
            "Pomegranate": self.received("Fall"),
            "Poppy": self.received("Summer"),
            "Potato": self.received("Spring"),
            "Preserves Jar": self.has_skill_level("Farming", 4),
            "Prismatic Shard": self.received("Year Two"),
            "Pufferfish": self.can_fish(80) & self.received("Summer"),
            "Pumpkin": self.received("Fall"),
            "Purple Mushroom": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Quartz": self.can_mine_in_the_mines_floor_1_40(),
            "Rabbit": self.has_building("Deluxe Coop"),
            "Rabbit's Foot": self.has("Rabbit"),
            "Radish": self.received("Summer"),
            "Rainbow Shell": self.received("Summer"),
            "Rainbow Trout": self.can_fish(45) & self.received("Summer"),
            "Rain Totem": self.has_skill_level("Foraging", 9),
            "Recycling Machine": self.has_skill_level("Fishing", 4) & self.has("Wood") &
                                 self.has("Stone") & self.has("Iron Bar"),
            "Red Cabbage": self.received("Year Two"),
            "Red Mullet": self.can_fish(55) & (self.received("Summer") | self.received("Winter")),
            "Red Mushroom": self.can_reach_region("Secret Woods") & (self.received("Summer") | self.received("Fall")),
            "Red Snapper": self.can_fish(40) & (self.received("Summer") | self.received("Fall")),
            "Refined Quartz": self.has("Quartz") | self.has("Fire Quartz") |
                              (self.has("Recycling Machine") & (self.has("Broken CD") | self.has("Broken Glasses"))),
            "Rhubarb": self.received("Spring") & self.can_reach_region("The Desert"),
            "Roe": self.can_fish() & self.has_building("Fish Pond"),
            "Roots Platter": self.can_cook() & self.has_skill_level("Combat", 3) &
                             self.has("Cave Carrot") & self.has("Winter Root"),
            "Ruby": self.can_mine_in_the_mines_floor_81_120() | self.can_do_panning(),
            "Salad": self.can_spend_money(220) | (
                    self.can_cook() & self.can_have_relationship("Emily", 3) & self.has("Leek") & self.has(
                "Dandelion")),
            "Salmon": self.can_fish(50) & self.received("Fall"),
            "Salmonberry": self.received("Spring"),
            "Salmon Dinner": self.can_cook() & self.can_have_relationship("Gus", 3) & self.has("Salmon") & self.has(
                "Amaranth") & self.has("Kale"),
            "Sandfish": self.can_fish(65) & self.can_reach_region("The Desert"),
            "Sardine": self.can_fish(30) & (self.received("Spring") | self.received("Fall") | self.received("Winter")),
            "Sashimi": self.can_fish() & self.can_cook() & self.can_have_relationship("Linus", 3),
            "Scorpion Carp": self.can_fish(90) & self.can_reach_region("The Desert"),
            "Sea Cucumber": self.can_fish(40) & (self.received("Fall") | self.received("Winter")),
            "Sea Urchin": self.can_reach_region("Tide Pools") | self.received("Summer"),
            "Seaweed": self.can_fish() | self.can_reach_region("Tide Pools"),
            "Shad": self.can_fish(45) & (self.received("Spring") | self.received("Summer") | self.received("Fall")),
            "Sheep": self.has_building("Deluxe Barn"),
            "Shrimp": self.can_crab_pot(),
            "Slime": self.can_mine_in_the_mines_floor_1_40(),
            "Smallmouth Bass": self.can_fish(28) & (self.received("Spring") | self.received("Fall")),
            "Snail": self.can_crab_pot(),
            "Snow Yam": self.received("Winter"),
            "Soggy Newspaper": self.can_crab_pot(),
            "Solar Essence": self.can_mine_in_the_mines_floor_41_80() | self.can_mine_in_the_skull_cavern(),
            "Spaghetti": self.can_spend_money(240),
            "Spice Berry": self.received("Summer"),
            "Spring Onion": self.received("Spring"),
            "Squid": self.can_fish(75) & self.received("Winter"),
            "Staircase": self.has_skill_level("Mining", 2),
            "Starfruit": (self.received("Summer") | self.received("Greenhouse")) & self.can_reach_region("The Desert"),
            "Stone": self.has_tool("Pickaxe"),
            "Stonefish": self.can_fish(65) & self.can_mine_to_floor(20),
            "Strawberry": self.received("Spring"),
            "Sturgeon": self.can_fish(78) & (self.received("Summer") | self.received("Winter")),
            "Sturgeon Roe": self.has("Sturgeon") & self.has_building("Fish Pond"),
            "Summer Spangle": self.received("Summer"),
            "Sunfish": self.can_fish(30) & (self.received("Spring") | self.received("Summer")),
            "Sunflower": self.received("Summer") | self.received("Fall"),
            "Super Cucumber": self.can_fish(80) & (self.received("Summer") | self.received("Fall")),
            "Survival Burger": self.can_cook() & self.has_skill_level("Foraging", 2) &
                               self.has(["Bread", "Cave Carrot", "Eggplant"]),
            "Sweet Gem Berry": self.received("Fall") | self.received("Greenhouse"),
            "Sweet Pea": self.received("Summer"),
            "Tapper": self.has_skill_level("Foraging", 3),
            "Tiger Trout": self.can_fish(60) & (self.received("Fall") | self.received("Winter")),
            "Tilapia": self.can_fish(50) & (self.received("Summer") | self.received("Fall")),
            "Tomato": self.received("Summer"),
            "Topaz": self.can_mine_in_the_mines_floor_1_40(),
            "Tortilla": self.can_cook() & self.can_spend_money(100) & self.has("Corn"),
            "Trash": self.can_crab_pot(),
            "Triple Shot Espresso": (self.has("Hot Java Ring") |
                                     (self.can_cook() & self.can_spend_money(5000) & self.has("Coffee"))),
            "Truffle Oil": self.has("Truffle") & self.has("Oil Maker"),
            "Truffle": self.has("Pig") & self.received("Year Two"),
            "Tulip": self.received("Spring"),
            "Tuna": self.can_fish(70) & (self.received("Summer") | self.received("Winter")),
            "Unmilled Rice": self.received("Year Two"),
            "Void Essence": self.can_mine_in_the_mines_floor_81_120() | self.can_mine_in_the_skull_cavern(),
            "Walleye": self.can_fish(45) & (self.received("Fall") | (self.received("Winter") & self.has("Rain Totem"))),
            "Wheat": self.received("Summer") | self.received("Fall"),
            "White Algae": self.can_fish() & self.can_mine_in_the_mines_floor_1_40(),
            "Wild Horseradish": self.received("Spring"),
            "Wild Plum": self.received("Fall"),
            "Wilted Bouquet": self.has("Furnace") & self.has("Bouquet") & self.has("Coal"),
            "Wine": self.has("Keg"),
            "Winter Root": self.received("Winter"),
            "Wood": self.has_tool("Axe"),
            "Woodskip": self.can_fish(50) & self.can_reach_region("Secret Woods"),
            "Wool": self.has("Rabbit") | self.has("Sheep"),
            "Yam": self.received("Fall"),
            "Hay": self.has_building("Silo"),
        })

        self.building_rules.update({
            "Barn": self.can_spend_money(6000) & self.has(["Wood", "Stone"]),
            "Big Barn": self.can_spend_money(12000) & self.has(["Wood", "Stone"]) & self.has_building("Barn"),
            "Deluxe Barn": self.can_spend_money(25000) & self.has(["Wood", "Stone"]) & self.has_building("Big Barn"),
            "Coop": self.can_spend_money(4000) & self.has(["Wood", "Stone"]),
            "Big Coop": self.can_spend_money(10000) & self.has(["Wood", "Stone"]) & self.has_building("Coop"),
            "Deluxe Coop": self.can_spend_money(20000) & self.has(["Wood", "Stone"]) & self.has_building("Big Coop"),
            "Fish Pond": self.can_spend_money(5000) & self.has(["Stone", "Seaweed", "Green Algae"]),
            "Mill": self.can_spend_money(2500) & self.has(["Stone", "Wood", "Cloth"]),
            "Shed": self.can_spend_money(15000) & self.has("Wood"),
            "Big Shed": self.can_spend_money(20000) & self.has(["Wood", "Stone"]) & self.has_building("Shed"),
            "Silo": self.can_spend_money(100) & self.has(["Stone", "Clay", "Copper Bar"]),
            "Slime Hutch": self.can_spend_money(10000) & self.has(["Stone", "Refined Quartz", "Iridium Bar"]),
            "Stable": self.can_spend_money(10000) & self.has(["Hardwood", "Iron Bar"]),
            "Well": self.can_spend_money(1000) & self.has("Stone"),
            "Shipping Bin": self.can_spend_money(250) & self.has("Wood"),
        })

        self.quest_rules.update({
            "Introductions": _True(),
            "How To Win Friends": self.can_complete_quest("Introductions"),
            "Getting Started": self.received("Spring") & self.has_tool("Hoe") & self.has_tool("Watering Can"),
            "To The Beach": self.received("Spring"),
            "Raising Animals": self.can_complete_quest("Getting Started") & self.has_building("Coop"),
            "Advancement": self.can_complete_quest("Getting Started") & self.has_skill_level("Farming", 1),
            "Archaeology": self.has_tool("Hoe") | self.can_mine_in_the_mines_floor_1_40() | self.can_fish(),
            "Meet The Wizard": self.received("Spring") & self.can_reach_region("Community Center"),
            "Forging Ahead": self.has("Copper Ore") & self.has("Furnace"),
            "Smelting": self.has("Copper Bar"),
            "Initiation": self.can_mine_in_the_mines_floor_1_40(),
            "Robin's Lost Axe": self.received("Spring"),
            "Jodi's Request": self.received("Spring") & self.has("Cauliflower"),
            "Mayor's \"Shorts\"": self.received("Summer") & self.can_have_relationship("Marnie", 4),
            "Blackberry Basket": self.received("Fall"),
            "Marnie's Request": self.can_have_relationship("Marnie", 3) & self.has("Cave Carrot"),
            "Pam Is Thirsty": self.received("Summer") & self.has("Pale Ale"),
            "A Dark Reagent": self.received("Winter") & self.has("Void Essence"),
            "Cow's Delight": self.received("Fall") & self.has("Amaranth"),
            "The Skull Key": self.received("Skull Key") & self.can_reach_region("The Desert"),
            "Crop Research": self.received("Summer") & self.has("Melon"),
            "Knee Therapy": self.received("Summer") & self.has("Hot Pepper"),
            "Robin's Request": self.received("Winter") & self.has("Hardwood"),
            "Qi's Challenge": self.can_mine_in_the_skull_cavern(),
            "The Mysterious Qi": self.has("Battery Pack") & self.can_reach_region("The Desert") & self.has(
                "Rainbow Shell") & self.has("Beet") & self.has("Solar Essence"),
            "Carving Pumpkins": self.received("Fall") & self.has("Pumpkin"),
            "A Winter Mystery": self.received("Winter"),
            "Strange Note": self.received("Magnifying Glass") & self.can_reach_region("Secret Woods") & self.has(
                "Maple Syrup"),
            "Cryptic Note": self.received("Magnifying Glass") & self.can_mine_perfectly_in_the_skull_cavern(),
            "Fresh Fruit": self.received("Year Two") & self.has("Apricot"),
            "Aquatic Research": self.received("Year Two") & self.has("Pufferfish"),
            "A Soldier's Star": self.received("Year Two") & self.has("Starfruit"),
            "Mayor's Need": self.received("Year Two") & self.has("Truffle Oil"),
            "Wanted: Lobster": self.received("Year Two") & self.has("Lobster"),
            "Pam Needs Juice": self.received("Year Two") & self.has("Battery Pack"),
            "Fish Casserole": self.received("Year Two") & self.can_have_relationship("Jodi", 4) & self.has(
                "Largemouth Bass"),
            "Catch A Squid": self.received("Year Two") & self.has("Squid"),
            "Fish Stew": self.received("Year Two") & self.has("Albacore"),
            "Pierre's Notice": self.received("Year Two") & self.has("Sashimi"),
            "Clint's Attempt": self.received("Year Two") & self.has("Amethyst"),
            "A Favor For Clint": self.received("Year Two") & self.has("Iron Bar"),
            "Staff Of Power": self.received("Year Two") & self.has("Iridium Bar"),
            "Granny's Gift": self.received("Year Two") & self.has("Leek"),
            "Exotic Spirits": self.received("Year Two") & self.has("Coconut"),
            "Catch a Lingcod": self.received("Year Two") & self.has("Lingcod"),
        })

    def has(self, items: Union[str, (Iterable[str], Sized)], count: Optional[int] = None) -> StardewRule:
        if isinstance(items, str):
            return _Has(items, self.item_rules)

        if count is None or count == len(items):
            return _And(self.has(item) for item in items)

        if count == 1:
            return _Or(self.has(item) for item in items)

        return _Count(count, (self.has(item) for item in items))

    def received(self, items: Union[str, Iterable[str]], count: Optional[int] = 1) -> StardewRule:
        if isinstance(items, str):
            return _Received(items, self.player, count)

        if count is None:
            return _And(self.received(item) for item in items)

        if count == 1:
            return _Or(self.received(item) for item in items)

        return _TotalReceived(count, items, self.player)

    def can_reach_region(self, spot: str) -> StardewRule:
        return _Reach(spot, "Region", self.player)

    def can_reach_location(self, spot: str) -> StardewRule:
        return _Reach(spot, "Location", self.player)

    def can_reach_entrance(self, spot: str) -> StardewRule:
        return _Reach(spot, "Entrance", self.player)

    def can_have_earned_total_money(self, amount: int) -> StardewRule:
        if amount <= 10000:
            return self.received("Spring")
        elif amount <= 30000:
            return self.received("Summer")
        elif amount <= 60000:
            return self.received("Fall")
        elif amount <= 70000:
            return self.received("Winter")
        return self.received("Year Two")

    def can_spend_money(self, amount: int) -> StardewRule:
        if amount <= 2000:
            return self.received("Spring")
        elif amount <= 8000:
            return self.received("Summer")
        elif amount <= 15000:
            return self.received("Fall")
        elif amount <= 18000:
            return self.received("Winter")
        return self.received("Year Two")

    def has_tool(self, tool: str, material: str = "Basic") -> StardewRule:
        if material == "Basic":
            return _True()

        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received(f"Progressive {tool}", count=tool_materials[material])

        return self.has(f"{material} Bar") & self.can_spend_money(tool_prices[material])

    def has_skill_level(self, skill: str, level: int) -> StardewRule:
        if level == 0:
            return _True()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.received(f"Progressive {skill} Level", count=level)

        if skill == "Fishing" and self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.can_get_fishing_xp()

        return self.received(season_per_skill_level[(skill, level)])

    def has_total_skill_level(self, level: int) -> StardewRule:
        if level == 0:
            return _True()

        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            skills_items = ["Progressive Farming Level", "Progressive Mining Level", "Progressive Foraging Level",
                            "Progressive Fishing Level", "Progressive Combat Level"]
            return self.received(skills_items, count=level)

        if level > 40 and self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received(season_per_total_level[level]) & self.can_get_fishing_xp()

        return self.received(season_per_total_level[level])

    def has_building(self, building: str) -> StardewRule:
        if not self.options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
            count = 1
            if building in ["Coop", "Barn", "Shed"]:
                building = f"Progressive {building}"
            elif building.startswith("Big"):
                count = 2
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            elif building.startswith("Deluxe"):
                count = 3
                building = " ".join(["Progressive", *building.split(" ")[1:]])
            return self.received(f"Building: {building}", count)

        return _Has(building, self.building_rules)

    def can_complete_quest(self, quest: str) -> StardewRule:
        return _Has(quest, self.quest_rules)

    def can_get_fishing_xp(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.can_fish() | self.can_crab_pot()

        return self.can_fish()

    def can_fish(self, difficulty: int = 0) -> StardewRule:
        skill_required = max(0, int((difficulty / 10) - 1))
        if difficulty <= 40:
            skill_required = 0
        skill_rule = self.has_skill_level("Fishing", skill_required)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            return self.received("Progressive Fishing Rod") & skill_rule

        return skill_rule

    def can_cook(self) -> StardewRule:
        return self.has_upgraded_house(1) or self.has_skill_level("Foraging", 9)

    def can_smelt(self, item: str):
        return self.has("Furnace") & self.has(item)

    def can_crab_pot(self) -> StardewRule:
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            return self.has("Crab Pot")

        return _True()

    def can_do_panning(self) -> StardewRule:
        return self.received("Glittering Boulder Removed")

    # Regions
    def can_mine_in_the_mines_floor_1_40(self) -> StardewRule:
        return self.can_reach_region("The Mines - Floor 5")

    def can_mine_in_the_mines_floor_41_80(self) -> StardewRule:
        return self.can_reach_region("The Mines - Floor 45")

    def can_mine_in_the_mines_floor_81_120(self) -> StardewRule:
        return self.can_reach_region("The Mines - Floor 85")

    def can_mine_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(120) &
                self.can_reach_region("Skull Cavern"))

    def can_mine_perfectly_in_the_skull_cavern(self) -> StardewRule:
        return (self.can_progress_in_the_mines_from_floor(160) &
                self.can_reach_region("Skull Cavern"))

    def get_weapon_rule_for_floor_tier(self, tier: int):
        if tier >= 4:
            return self.has_galaxy_weapon()
        if tier >= 3:
            return self.has_great_weapon()
        if tier >= 2:
            return self.has_good_weapon()
        if tier >= 1:
            return self.has_decent_weapon()
        return self.has_any_weapon()

    def can_progress_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40)
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", tier))
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level("Combat", combat_tier))
        return _And(rules)

    def can_progress_easily_in_the_mines_from_floor(self, floor: int) -> StardewRule:
        tier = int(floor / 40) + 1
        rules = []
        weapon_rule = self.get_weapon_rule_for_floor_tier(tier)
        rules.append(weapon_rule)
        if self.options[options.ToolProgression] == options.ToolProgression.option_progressive:
            rules.append(self.received("Progressive Pickaxe", count=tier))
        if self.options[options.SkillProgression] == options.SkillProgression.option_progressive:
            combat_tier = min(10, max(0, tier * 2))
            rules.append(self.has_skill_level("Combat", combat_tier))
        return _And(rules)

    def has_mine_elevator_to_floor(self, floor: int) -> StardewRule:
        if (self.options[options.TheMinesElevatorsProgression] ==
                options.TheMinesElevatorsProgression.option_progressive or
                self.options[options.TheMinesElevatorsProgression] ==
                options.TheMinesElevatorsProgression.option_progressive_from_previous_floor):
            return self.received("Progressive Mine Elevator", count=int(floor / 5))
        return _True()

    def can_mine_to_floor(self, floor: int) -> StardewRule:
        previous_elevator = max(floor - 5, 0)
        previous_previous_elevator = max(floor - 10, 0)
        return ((self.has_mine_elevator_to_floor(previous_elevator) &
                 self.can_progress_in_the_mines_from_floor(previous_elevator)) |
                (self.has_mine_elevator_to_floor(previous_previous_elevator) &
                 self.can_progress_easily_in_the_mines_from_floor(previous_previous_elevator)))

    def has_jotpk_power_level(self, power_level: int) -> StardewRule:
        if self.options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
            return _True()
        jotpk_buffs = ["JotPK: Progressive Boots", "JotPK: Progressive Gun",
                       "JotPK: Progressive Ammo", "JotPK: Extra Life", "JotPK: Increased Drop Rate"]
        return self.received(jotpk_buffs, power_level)

    def has_junimo_kart_power_level(self, power_level: int) -> StardewRule:
        if self.options[options.ArcadeMachineLocations] != options.ArcadeMachineLocations.option_full_shuffling:
            return _True()
        return self.received("Junimo Kart: Extra Life", power_level)

    def can_get_married(self) -> StardewRule:
        return self.can_reach_region("Tide Pools") & self.received("Fall")

    def has_upgraded_house(self, level: int) -> StardewRule:
        return self.can_upgrade_house(level)

    def can_upgrade_house(self, level: int) -> StardewRule:
        if level == 1:
            return self.can_spend_money(10000)
        if level == 2:
            return self.can_spend_money(60000) & self.has("Hardwood")
        if level == 3:
            return self.can_spend_money(160000) & self.has("Hardwood")

    def can_have_relationship(self, npc: str, hearts: int) -> StardewRule:
        if npc == "Leo":
            return self.can_reach_region("Ginger Island")

        if npc == "Sandy":
            return self.can_reach_region("The Desert")

        if npc == "Kent":
            return self.received("Year Two")

        if hearts <= 3:
            return self.received("Spring")
        if hearts <= 6:
            return self.received("Summer")
        if hearts <= 9:
            return self.received("Fall")
        return self.received("Winter")

    def can_complete_bundle(self, bundle_requirements: list[BundleItem], number_required: int) -> StardewRule:
        item_rules = []
        for item in bundle_requirements:
            if item.id == -1:
                return self.can_spend_money(item.amount)
            else:
                item_rules.append(item.name)
        return self.has(item_rules, number_required)

    def can_complete_community_center(self) -> StardewRule:
        return (self.can_reach_location("Complete Crafts Room") &
                self.can_reach_location("Complete Pantry") &
                self.can_reach_location("Complete Fish Tank") &
                self.can_reach_location("Complete Bulletin Board") &
                self.can_reach_location("Complete Vault") &
                self.can_reach_location("Complete Boiler Room"))

    def can_finish_grandpa_evaluation(self) -> StardewRule:
        # https://stardewvalleywiki.com/Grandpa
        rules_worth_a_point = [self.can_have_earned_total_money(50000),  # 50 000g
                               self.can_have_earned_total_money(100000),  # 100 000g
                               self.can_have_earned_total_money(200000),  # 200 000g
                               self.can_have_earned_total_money(300000),  # 300 000g
                               self.can_have_earned_total_money(500000),  # 500 000g
                               self.can_have_earned_total_money(1000000),  # 1 000 000g first point
                               self.can_have_earned_total_money(1000000),  # 1 000 000g second point
                               self.has_total_skill_level(30),  # Total Skills: 30
                               self.has_total_skill_level(50),  # Total Skills: 50
                               # Completing the museum not expected
                               # Catching every fish not expected
                               # Shipping every item not expected
                               self.can_get_married() & self.has_upgraded_house(2),
                               # Married with 2 house upgrades
                               self.received("Fall"),  # 5 Friends (TODO)
                               self.received("Winter"),  # 10 friends (TODO)
                               self.received("Fall"),  # Max Pet takes 56 days min
                               self.can_complete_community_center(),  # Community Center Completion
                               self.can_complete_community_center(),  # CC Ceremony first point
                               self.can_complete_community_center(),  # CC Ceremony second point
                               self.received("Skull Key"),  # Skull Key obtained
                               # Rusty key not expected
                               ]
        return _Count(12, rules_worth_a_point)

    def has_any_weapon(self) -> StardewRule:
        return self.has_decent_weapon() | self.received(item.name for item in all_items if Group.WEAPON in item.groups)

    def has_decent_weapon(self) -> StardewRule:
        return (self.has_good_weapon() |
                self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and
                              (Group.MINES_FLOOR_50 in item.groups or Group.MINES_FLOOR_60 in item.groups)))

    def has_good_weapon(self) -> StardewRule:
        return ((self.has_great_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and
                               (Group.MINES_FLOOR_80 in item.groups or Group.MINES_FLOOR_90 in item.groups))) &
                self.received("Adventurer's Guild"))

    def has_great_weapon(self) -> StardewRule:
        return ((self.has_galaxy_weapon() |
                 self.received(item.name for item in all_items
                               if Group.WEAPON in item.groups and Group.MINES_FLOOR_110 in item.groups)) &
                self.received("Adventurer's Guild"))

    def has_galaxy_weapon(self) -> StardewRule:
        return (self.received(item.name for item in all_items
                              if Group.WEAPON in item.groups and Group.GALAXY_WEAPONS in item.groups) &
                self.received("Adventurer's Guild"))
