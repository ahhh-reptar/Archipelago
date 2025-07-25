from . import content_packs
from .feature import cropsanity, friendsanity, fishsanity, booksanity, building_progression, skill_progression, tool_progression, hatsanity, museumsanity
from .game_content import ContentPack, StardewContent, StardewFeatures
from .unpacking import unpack_content
from .. import options
from ..strings.building_names import Building


def create_content(player_options: options.StardewValleyOptions) -> StardewContent:
    active_packs = choose_content_packs(player_options)
    features = choose_features(player_options)
    return unpack_content(features, active_packs)


def choose_content_packs(player_options: options.StardewValleyOptions):
    active_packs = [content_packs.pelican_town, content_packs.the_desert, content_packs.the_farm, content_packs.the_mines]

    if player_options.exclude_ginger_island == options.ExcludeGingerIsland.option_false:
        active_packs.append(content_packs.ginger_island_content_pack)

        if player_options.special_order_locations & options.SpecialOrderLocations.value_qi:
            active_packs.append(content_packs.qi_board_content_pack)

    for mod in sorted(player_options.mods.value):
        active_packs.append(content_packs.by_mod[mod])

    return active_packs


def choose_features(player_options: options.StardewValleyOptions) -> StardewFeatures:
    return StardewFeatures(
        choose_booksanity(player_options.booksanity),
        choose_building_progression(player_options.building_progression, player_options.farm_type),
        choose_cropsanity(player_options.cropsanity),
        choose_fishsanity(player_options.fishsanity),
        choose_friendsanity(player_options.friendsanity, player_options.friendsanity_heart_size),
        choose_hatsanity(player_options.hatsanity),
        choose_museumsanity(player_options.museumsanity),
        choose_skill_progression(player_options.skill_progression),
        choose_tool_progression(player_options.tool_progression, player_options.skill_progression),
    )


booksanity_by_option = {
    options.Booksanity.option_none: booksanity.BooksanityDisabled(),
    options.Booksanity.option_power: booksanity.BooksanityPower(),
    options.Booksanity.option_power_skill: booksanity.BooksanityPowerSkill(),
    options.Booksanity.option_all: booksanity.BooksanityAll(),
}


def choose_booksanity(booksanity_option: options.Booksanity) -> booksanity.BooksanityFeature:
    booksanity_feature = booksanity_by_option.get(booksanity_option)

    if booksanity_feature is None:
        raise ValueError(f"No booksanity feature mapped to {str(booksanity_option.value)}")

    return booksanity_feature


def choose_building_progression(building_option: options.BuildingProgression,
                                farm_type_option: options.FarmType) -> building_progression.BuildingProgressionFeature:
    starting_buildings = {Building.farm_house, Building.pet_bowl, Building.shipping_bin}

    if farm_type_option == options.FarmType.option_meadowlands:
        starting_buildings.add(Building.coop)

    if (building_option == options.BuildingProgression.option_vanilla
            or building_option == options.BuildingProgression.option_vanilla_cheap
            or building_option == options.BuildingProgression.option_vanilla_very_cheap):
        return building_progression.BuildingProgressionVanilla(
            starting_buildings=starting_buildings,
        )

    starting_buildings.remove(Building.shipping_bin)
    starting_buildings.remove(Building.pet_bowl)

    if (building_option == options.BuildingProgression.option_progressive
            or building_option == options.BuildingProgression.option_progressive_cheap
            or building_option == options.BuildingProgression.option_progressive_very_cheap):
        return building_progression.BuildingProgressionProgressive(
            starting_buildings=starting_buildings,
        )

    raise ValueError(f"No building progression feature mapped to {str(building_option.value)}")


cropsanity_by_option = {
    options.Cropsanity.option_disabled: cropsanity.CropsanityDisabled(),
    options.Cropsanity.option_enabled: cropsanity.CropsanityEnabled(),
}


def choose_cropsanity(cropsanity_option: options.Cropsanity) -> cropsanity.CropsanityFeature:
    cropsanity_feature = cropsanity_by_option.get(cropsanity_option)

    if cropsanity_feature is None:
        raise ValueError(f"No cropsanity feature mapped to {str(cropsanity_option.value)}")

    return cropsanity_feature


fishsanity_by_option = {
    options.Fishsanity.option_none: fishsanity.FishsanityNone(),
    options.Fishsanity.option_legendaries: fishsanity.FishsanityLegendaries(),
    options.Fishsanity.option_special: fishsanity.FishsanitySpecial(),
    options.Fishsanity.option_randomized: fishsanity.FishsanityAll(randomization_ratio=0.4),
    options.Fishsanity.option_all: fishsanity.FishsanityAll(),
    options.Fishsanity.option_exclude_legendaries: fishsanity.FishsanityExcludeLegendaries(),
    options.Fishsanity.option_exclude_hard_fish: fishsanity.FishsanityExcludeHardFish(),
    options.Fishsanity.option_only_easy_fish: fishsanity.FishsanityOnlyEasyFish(),
}


def choose_fishsanity(fishsanity_option: options.Fishsanity) -> fishsanity.FishsanityFeature:
    fishsanity_feature = fishsanity_by_option.get(fishsanity_option)

    if fishsanity_feature is None:
        raise ValueError(f"No fishsanity feature mapped to {str(fishsanity_option.value)}")

    return fishsanity_feature


def choose_friendsanity(friendsanity_option: options.Friendsanity, heart_size: options.FriendsanityHeartSize) -> friendsanity.FriendsanityFeature:
    if friendsanity_option == options.Friendsanity.option_none:
        return friendsanity.FriendsanityNone()

    if friendsanity_option == options.Friendsanity.option_bachelors:
        return friendsanity.FriendsanityBachelors(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_starting_npcs:
        return friendsanity.FriendsanityStartingNpc(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all:
        return friendsanity.FriendsanityAll(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all_with_marriage:
        return friendsanity.FriendsanityAllWithMarriage(heart_size.value)

    raise ValueError(f"No friendsanity feature mapped to {str(friendsanity_option.value)}")


def choose_hatsanity(hat_option: options.Hatsanity) -> hatsanity.HatsanityFeature:
    if hat_option == options.Hatsanity.option_none:
        return hatsanity.HatsanityNone()

    if hat_option == options.Hatsanity.option_easy:
        return hatsanity.HatsanityEasy()

    if hat_option == options.Hatsanity.option_tailoring:
        return hatsanity.HatsanityTailoring()

    if hat_option == options.Hatsanity.option_easy_tailoring:
        return hatsanity.HatsanityEasyTailoring()

    if hat_option == options.Hatsanity.option_medium:
        return hatsanity.HatsanityMedium()

    if hat_option == options.Hatsanity.option_difficult:
        return hatsanity.HatsanityDifficult()

    if hat_option == options.Hatsanity.option_near_perfection:
        return hatsanity.HatsanityNearPerfection()

    if hat_option == options.Hatsanity.option_post_perfection:
        return hatsanity.HatsanityPostPerfection()

    raise ValueError(f"No hatsanity feature mapped to {str(hat_option.value)}")


def choose_museumsanity(museumsanity_option: options.Museumsanity) -> museumsanity.MuseumsanityFeature:
    if museumsanity_option == options.Museumsanity.option_none:
        return museumsanity.MuseumsanityNone()

    if museumsanity_option == options.Museumsanity.option_milestones:
        return museumsanity.MuseumsanityMilestones()

    if museumsanity_option == options.Museumsanity.option_randomized:
        return museumsanity.MuseumsanityRandomized()

    if museumsanity_option == options.Museumsanity.option_all:
        return museumsanity.MuseumsanityAll()

    raise ValueError(f"No museumsanity feature mapped to {str(museumsanity_option.value)}")


skill_progression_by_option = {
    options.SkillProgression.option_vanilla: skill_progression.SkillProgressionVanilla(),
    options.SkillProgression.option_progressive: skill_progression.SkillProgressionProgressive(),
    options.SkillProgression.option_progressive_with_masteries: skill_progression.SkillProgressionProgressiveWithMasteries(),
}


def choose_skill_progression(skill_progression_option: options.SkillProgression) -> skill_progression.SkillProgressionFeature:
    skill_progression_feature = skill_progression_by_option.get(skill_progression_option)

    if skill_progression_feature is None:
        raise ValueError(f"No skill progression feature mapped to {str(skill_progression_option.value)}")

    return skill_progression_feature


def choose_tool_progression(tool_option: options.ToolProgression, skill_option: options.SkillProgression) -> tool_progression.ToolProgressionFeature:
    if tool_option.is_vanilla:
        return tool_progression.ToolProgressionVanilla()

    if tool_option.is_progressive:
        starting_tools, tools_distribution = tool_progression.get_tools_distribution(
            progressive_tools_enabled=True,
            skill_masteries_enabled=skill_option == options.SkillProgression.option_progressive_with_masteries,
            no_starting_tools_enabled=bool(tool_option & options.ToolProgression.value_no_starting_tools),
        )

        return tool_progression.ToolProgressionProgressive(starting_tools, tools_distribution)

    raise ValueError(f"No tool progression feature mapped to {str(tool_option.value)}")
