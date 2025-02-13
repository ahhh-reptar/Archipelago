from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle


class Goal(Choice):
    """
    Goal for this playthrough.
    """
    internal_name = "goal"
    display_name = "Goal"
    default = 0
    option_beat_normal = 0
    option_beat_hard = 1
    option_beat_very_hard = 2
    option_beat_nightmare = 3
    option_beat_normal_with_all_characters = 4
    option_beat_hard_with_all_characters = 5
    option_beat_very_hard_with_all_characters = 6
    option_beat_nightmare_with_all_characters = 7
    option_beat_floor_25 = 8
    option_beat_floor_30 = 9
    option_beat_floor_35 = 10
    option_beat_floor_40 = 11
    option_beat_floor_45 = 12
    option_beat_floor_50 = 13


class ShuffleCharacters(Toggle):
    """
    If enabled, all characters will be unlockable items
    If disabled, all characters will start unlocked
    There will be one location for finishing a run with each character
    """
    internal_name = "shuffle_characters"
    display_name = "Shuffle Characters"


class ShuffleItems(Toggle):
    """
    All items start out locked, and you need to unlock them. Not all items will be in your item pool. Includes upgrades
    """
    internal_name = "shuffle_items"
    display_name = "Shuffle Items"


class ShufflePerks(Toggle):
    """
    You start with no Perks, and will unlock some, but not all of them, to be permanently active
    """
    internal_name = "shuffle_perks"
    display_name = "Shuffle Perks"


class Enemysanity(Toggle):
    """
    Killing each monster type is a check
    """
    internal_name = "enemysanity"
    display_name = "EnemySanity"


class DungeonClawlerDeathlink(Choice):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    If set to "Claw", receiving a deathlink will simply skip your next next claw, instead of killing you, because dying is very punishing in Dungeon Clawler
    You send a deathlink when you die, and also when you fail at using a claw and grab zero items
    """
    internal_name = "dc_deathlink"
    display_name = "DeathLink"
    default = 0
    option_disabled = 0
    option_claw = 1
    option_death = 2


@dataclass
class DungeonClawlerOptions(PerGameCommonOptions):
    goal: Goal
    shuffle_characters: ShuffleCharacters
    shuffle_items: ShuffleItems
    shuffle_perks: ShufflePerks
    enemysanity: Enemysanity
    death_link: DungeonClawlerDeathlink
