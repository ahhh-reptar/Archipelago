import itertools

import pytest

from BaseClasses import ItemClassification
from Options import SpecialRange
from worlds.stardew_valley import StardewValleyWorld, StardewItem
from . import setup_solo_multiworld
from ..options import Goal, BackpackProgression, SeasonRandomization, StardewOption, stardew_valley_option_classes, ToolProgression

SEASONS = {"Spring", "Summer", "Fall", "Winter"}
TOOLS = {"Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can", "Fishing Rod"}


@pytest.mark.parametrize("option, value", [(option, value)
                                           for option in stardew_valley_option_classes
                                           if issubclass(option, SpecialRange)
                                           for value in option.special_range_names])
def test_given_special_range_when_generate_then_can_generate(option: (SpecialRange, StardewOption), value):
    multi_world = setup_solo_multiworld(StardewValleyWorld, {option.internal_name: option.special_range_names[value]})

    assert StardewItem("Victory", ItemClassification.progression, None, 1) in multi_world.get_items()


@pytest.mark.parametrize("option, value", [(option, value)
                                           for option in stardew_valley_option_classes
                                           if option not in {Goal, SeasonRandomization, BackpackProgression, ToolProgression}
                                           if option.options
                                           for value in option.options])
def test_given_choice_when_generate_then_can_generate(option, value):
    multi_world = setup_solo_multiworld(StardewValleyWorld, {option.internal_name: option.options[value]})

    assert StardewItem("Victory", ItemClassification.progression, None, 1) in multi_world.get_items()


class TestGoal:
    @pytest.mark.parametrize("goal,location", [("community_center", "Complete Community Center"),
                                               ("grandpa_evaluation", "Succeed Grandpa's Evaluation"),
                                               ("bottom_of_the_mines", "Reach the Bottom of The Mines"),
                                               ("cryptic_note", "Complete Quest Cryptic Note"),
                                               ("master_angler", "Catch Every Fish")])
    def test_given_goal_when_generate_then_victory_is_in_correct_location(self, goal, location):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {Goal.internal_name: Goal.options[goal]})
        victory = multi_world.find_item("Victory", 1)

        assert victory.name == location


class TestSeasonRandomization:
    def test_given_disabled_when_generate_then_all_seasons_are_precollected(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {SeasonRandomization.internal_name: SeasonRandomization.option_disabled})

        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        assert all([season in precollected_items for season in SEASONS])

    @pytest.mark.parametrize("value", [value for value in SeasonRandomization.options if "randomized" in value])
    def test_given_randomized_when_generate_then_all_seasons_are_in_the_pool_or_precollected(self, value):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {SeasonRandomization.internal_name: SeasonRandomization.options[value]})

        precollected_items = {item.name for item in multi_world.precollected_items[1]}
        items = {item.name for item in multi_world.get_items()} | precollected_items
        assert all([season in items for season in SEASONS])
        assert len(SEASONS.intersection(precollected_items)) == 1

    def test_given_progressive_when_generate_then_3_progressive_seasons_are_in_the_pool(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {SeasonRandomization.internal_name: SeasonRandomization.option_progressive})

        items = [item.name for item in multi_world.get_items()]
        assert items.count("Progressive Season") == 3


class TestBackpackProgression:
    def test_given_vanilla_when_generate_then_no_backpack_in_pool(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {BackpackProgression.internal_name: BackpackProgression.option_vanilla})

        assert "Progressive Backpack" not in {item.name for item in multi_world.get_items()}

    @pytest.mark.parametrize("value", [value for value in BackpackProgression.options if "progressive" in value])
    def test_given_progressive_when_generate_then_progressive_backpack_is_in_pool_two_times(self, value):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {BackpackProgression.internal_name: BackpackProgression.options[value]})

        items = [item.name for item in multi_world.get_items()]
        assert items.count("Progressive Backpack") == 2

    @pytest.mark.parametrize("value", [value for value in BackpackProgression.options if "progressive" in value])
    def test_given_progressive_when_generate_then_backpack_upgrades_are_locations(self, value):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {BackpackProgression.internal_name: BackpackProgression.options[value]})

        locations = {locations.name for locations in multi_world.get_locations(1)}
        assert "Large Pack" in locations
        assert "Deluxe Pack" in locations

    def test_given_early_progressive_when_generate_then_progressive_backpack_is_in_early_pool(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {BackpackProgression.internal_name: BackpackProgression.option_early_progressive})

        assert "Progressive Backpack" in multi_world.early_items[1]


class TestToolProgression:
    def test_given_vanilla_when_generate_then_no_tool_in_pool(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {ToolProgression.internal_name: ToolProgression.option_vanilla})

        items = {item.name for item in multi_world.get_items()}
        for tool in TOOLS:
            assert tool not in items

    def test_given_progressive_when_generate_then_progressive_tool_of_each_is_in_pool_four_times(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {ToolProgression.internal_name: ToolProgression.option_progressive})

        items = [item.name for item in multi_world.get_items()]
        for tool in TOOLS:
            assert items.count("Progressive " + tool) == 4

    def test_given_progressive_when_generate_then_tool_upgrades_are_locations(self):
        multi_world = setup_solo_multiworld(StardewValleyWorld, {ToolProgression.internal_name: ToolProgression.option_progressive})

        locations = {locations.name for locations in multi_world.get_locations(1)}
        for material, tool in itertools.product(["Copper", "Iron", "Gold", "Iridium"], ["Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can"]):
            assert f"{material} {tool} Upgrade" in locations
        assert "Purchase Training Rod" in locations
        assert "Bamboo Pole Cutscene" in locations
        assert "Purchase Fiberglass Rod" in locations
        assert "Purchase Iridium Rod" in locations
