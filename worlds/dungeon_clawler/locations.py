from BaseClasses import Location, MultiWorld, Region, ItemClassification
from . import DungeonClawlerItem
from .constants.fighters import all_fighters
from .constants.difficulties import all_difficulties, Difficulty
from .constants.enemies import all_enemies, EnemyDifficulty
from .constants.perks import all_perk_items, max_perk_stack
from .options import DungeonClawlerOptions, Goal, Enemysanity, ShufflePerks, ShuffleFighters
from .constants.world_strings import GAME_NAME


class DungeonClawlerLocation(Location):
    game: str = GAME_NAME


class LocationData():
    name: str
    id_without_offset: int
    region: str

    def __init__(self, name: str, region: str, id_without_offset: int = -1):
        self.name = name
        self.id_without_offset = id_without_offset
        self.region = region


def floor_location_name(floor: int, difficulty: str) -> str:
    return f"Complete Floor {floor} - {difficulty}"


def character_location_name(character: str) -> str:
    return f"Win a game with {character}"


def perk_location_name(perk_name: str, level: int) -> str:
    return f"{perk_name} - Level {level}"


def floor_region_name(floor: int, difficulty: str) -> str:
    return f"Floor {floor} - {difficulty}"


def beat_floor_entrance_name(floor: int, difficulty: str) -> str:
    return f"Beat Floor {floor} - {difficulty}"


offset = 0

floor_locations = []
for floor in range(1, 21):
    for difficulty in all_difficulties:
        floor_locations.append(LocationData(floor_location_name(floor, difficulty), floor_region_name(floor+1, difficulty)))

character_win_locations = []
for character in all_fighters:
    character_win_locations.append(LocationData(character_location_name(character.name), floor_region_name(21, Difficulty.hard)))


enemy_locations = []
for enemy in all_enemies:
    for difficulty in all_difficulties:
        if enemy.difficulty == EnemyDifficulty.easy:
            floor = 2
        elif enemy.difficulty == EnemyDifficulty.medium:
            floor = 6
        elif enemy.difficulty == EnemyDifficulty.hard:
            floor = 12
        elif enemy.difficulty == EnemyDifficulty.easy_boss:
            floor = 5
        elif enemy.difficulty == EnemyDifficulty.medium_boss:
            floor = 10
        elif enemy.difficulty == EnemyDifficulty.hard_boss:
            floor = 15
        elif enemy.difficulty == EnemyDifficulty.final_boss:
            floor = 20
        else:
            floor = 30
        region = f"Floor {floor} - {difficulty}"
        enemy_locations.append(LocationData(f"Kill {enemy.name} - {difficulty}", region))

perk_locations = []
for perk in all_perk_items:
    for level in range(1, min(max_perk_stack, perk.max_stack)+1):
        if level <= 2:
            difficulty = Difficulty.normal
        elif level <= 4:
            difficulty = Difficulty.hard
        elif level <= 6:
            difficulty = Difficulty.very_hard
        else:
            difficulty = Difficulty.nightmare
        region = f"Floor {level*4} - {difficulty}"
        perk_locations.append(LocationData(perk_location_name(perk.name, level), region))

all_locations = []
for i, mission_location in enumerate(floor_locations):
    mission_location.id_without_offset = 1 + i
    all_locations.append(mission_location)

for i, character_win_location in enumerate(character_win_locations):
    character_win_location.id_without_offset = 501 + i
    all_locations.append(character_win_location)

for i, enemy_location in enumerate(enemy_locations):
    enemy_location.id_without_offset = 1001 + i
    all_locations.append(enemy_location)

for i, perk_location in enumerate(perk_locations):
    perk_location.id_without_offset = 1501 + i
    all_locations.append(perk_location)

location_table = dict()

location_table.update({location_data.name: offset + location_data.id_without_offset for location_data in all_locations})


def create_locations(multiworld: MultiWorld, player: int, world_options: DungeonClawlerOptions) -> None:
    victory_location = ""
    if world_options.goal == Goal.option_beat_normal:
        victory_location = floor_location_name(20, Difficulty.normal)
    elif world_options.goal == Goal.option_beat_hard:
        victory_location = floor_location_name(20, Difficulty.hard)
    elif world_options.goal == Goal.option_beat_very_hard:
        victory_location = floor_location_name(20, Difficulty.very_hard)
    elif world_options.goal == Goal.option_beat_nightmare:
        victory_location = floor_location_name(20, Difficulty.nightmare)
    else:

        if world_options.goal == Goal.option_beat_floor_25:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.normal), player)
        elif world_options.goal == Goal.option_beat_floor_30:
            region_victory = multiworld.get_region(floor_region_name(30, Difficulty.normal), player)
        elif world_options.goal == Goal.option_beat_floor_35:
            region_victory = multiworld.get_region(floor_region_name(35, Difficulty.normal), player)
        elif world_options.goal == Goal.option_beat_floor_40:
            region_victory = multiworld.get_region(floor_region_name(40, Difficulty.normal), player)
        elif world_options.goal == Goal.option_beat_floor_45:
            region_victory = multiworld.get_region(floor_region_name(45, Difficulty.normal), player)
        elif world_options.goal == Goal.option_beat_floor_50:
            region_victory = multiworld.get_region(floor_region_name(50, Difficulty.normal), player)
        # These goals will have slightly stricter logic to make it not too much of an RNG pain
        elif world_options.goal == Goal.option_beat_normal_with_all_characters:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.hard), player)
        elif world_options.goal == Goal.option_beat_hard_with_all_characters:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.very_hard), player)
        elif world_options.goal == Goal.option_beat_very_hard_with_all_characters:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.nightmare), player)
        elif world_options.goal == Goal.option_beat_nightmare_with_all_characters:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.nightmare), player)
        else:
            region_victory = multiworld.get_region(floor_region_name(25, Difficulty.normal), player)
        create_victory_event(region_victory, player)

    create_floor_locations(multiworld, player, victory_location)
    create_character_win_locations(multiworld, player, world_options)
    create_enemy_locations(multiworld, player, world_options)
    create_perk_locations(multiworld, player, world_options)


def create_floor_locations(multiworld: MultiWorld, player: int, victory_location: str) -> None:
    for location_data in floor_locations:
        region = multiworld.get_region(location_data.region, player)
        if location_data.name == victory_location:
            create_victory_event(region, player)
            continue

        name = location_data.name
        location = DungeonClawlerLocation(player, name, location_table[name], region)
        region.locations.append(location)


def create_character_win_locations(multiworld: MultiWorld, player: int, world_options: DungeonClawlerOptions) -> None:
    if world_options.shuffle_fighters == ShuffleFighters.option_none:
        return
    for location_data in character_win_locations:
        region = multiworld.get_region(location_data.region, player)
        name = location_data.name
        location = DungeonClawlerLocation(player, name, location_table[name], region)
        region.locations.append(location)


def create_enemy_locations(multiworld: MultiWorld, player: int, world_options: DungeonClawlerOptions) -> None:
    if world_options.enemysanity == Enemysanity.option_false:
        return

    for location_data in enemy_locations:
        region = multiworld.get_region(location_data.region, player)
        name = location_data.name
        location = DungeonClawlerLocation(player, name, location_table[name], region)
        region.locations.append(location)


def create_perk_locations(multiworld: MultiWorld, player: int, world_options: DungeonClawlerOptions) -> None:
    if world_options.shuffle_perks == ShufflePerks.option_false:
        return

    for location_data in perk_locations:
        region = multiworld.get_region(location_data.region, player)
        name = location_data.name
        location = DungeonClawlerLocation(player, name, location_table[name], region)
        region.locations.append(location)


def create_victory_event(region: Region, player: int):
    location_victory = DungeonClawlerLocation(player, "Victory", None, region)
    region.locations.append(location_victory)
    location_victory.place_locked_item(create_event_item(player, "Victory"))


def create_event_item(player, event: str) -> DungeonClawlerItem:
    return DungeonClawlerItem(event, ItemClassification.progression, None, player)
