from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle, NamedRange, Range


class Goal(Choice):
    """
    Goal for this playthrough.
    """
    internal_name = "goal"
    display_name = "Goal"
    default = 3
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


class ShuffleFighters(Choice):
    """
    None: Fighters all start unlocked, there are no locations for using specific ones
    Fighters: One fighter starts unlocked, the rest must be received. There is one location for winning once with each character. A fighter's lucky paw unlocks with it
    Fighters and Paws: Also shuffles the lucky paws as items. You can play higher difficulties as soon as you have [1-2-3] paws
    """
    internal_name = "shuffle_fighters"
    display_name = "Shuffle Fighters"
    default = 2
    option_none = 0
    option_fighters = 1
    option_fighters_and_paws = 2


class ShuffleCombatItems(Toggle):
    """
    All combat items start out locked, and you need to unlock them. Not all combat items will be in your item pool.
    You can pick from your unlocked combat items what to start each run with. Each two copies of the same item turns into an upgraded item.
    You receive "Combat Inventory Size" items to increase the number of items you can start each run with
    """
    internal_name = "shuffle_combat_items"
    display_name = "Shuffle Combat Items"
    default = Toggle.option_true


class ShufflePerks(Toggle):
    """
    You start with no Perks, and will unlock some, but not all of them, over the course of the run
    You can pick from your unlocked perks what to start each run with
    You receive "Perk Inventory Size" items to increase the number of perks you can equip at once
    """
    internal_name = "shuffle_perks"
    display_name = "Shuffle Perks"
    default = Toggle.option_true


class ExtraInventorySizes(Range):
    """
    You will start with a limited inventory size for starting items and perks, and earn this many extras from your item pool
    If you set a too low value, and get unlucky and have bad items, you might be unable to beat your game.
    """
    internal_name = "extra_inventory_sizes"
    display_name = "Extra Inventory Sizes"
    default = 10
    range_start = 0
    range_end = 30


class Enemysanity(Toggle):
    """
    Killing each monster type is a check. Turning this off significantly reduces the number of checks, and subsequently increases difficulty by a lot.
    """
    internal_name = "enemysanity"
    display_name = "EnemySanity"
    default = Toggle.option_true


class MaximumCombatItems(Range):
    """
    A hard cap on the number of combat items that can generate for your slot.
    If you set a low value, and get unlucky and have bad items, you might be unable to beat your game.
    This is an upper limit, not a guarantee, depending on other settings, you might get less than what you set here.
    """
    internal_name = "max_combat_items"
    display_name = "Maximum Combat Items"
    default = 100
    range_start = 20
    range_end = 250


class MaximumPerks(Range):
    """
    A hard cap on the number of perks that can generate for your slot.
    If you set a low value, and get unlucky and have bad perks, you might be unable to beat your game.
    This is an upper limit, not a guarantee, depending on other settings, you might get less than what you set here.
    """
    internal_name = "max_perks"
    display_name = "Maximum Perks"
    default = 100
    range_start = 20
    range_end = 250


class TrapDifficulty(Choice):
    """
    Enable traps, and how punishing should they be?
    Traps, and other fillers, will only roll if you have free space in the item pool after generating the real items
    On some settings, you might get no traps regardless.
    For example, on easy, a "Spike Trap" only spawns one spike in your next Claw Machine.
    But on Nightmare, it might spawn 16 spikes.
    """
    internal_name = "trap_difficulty"
    display_name = "Trap Difficulty"
    default = 2
    option_no_traps = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_hell = 4
    option_nightmare = 5


class DungeonClawlerDeathlink(Choice):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    If set to "Claw", receiving a deathlink will simply skip your next next claw, instead of killing you, because dying is very punishing in Dungeon Clawler
    You send a deathlink when you die, and also when you fail at using a claw and grab zero items
    """
    internal_name = "death_link"
    display_name = "DeathLink"
    default = 0
    option_disabled = 0
    option_claw = 1
    option_death = 2


@dataclass
class DungeonClawlerOptions(PerGameCommonOptions):
    goal: Goal
    shuffle_fighters: ShuffleFighters
    shuffle_combat_items: ShuffleCombatItems
    shuffle_perks: ShufflePerks
    extra_inventory_sizes: ExtraInventorySizes
    enemysanity: Enemysanity
    maximum_combat_items: MaximumCombatItems
    maximum_perks: MaximumPerks
    trap_difficulty: TrapDifficulty
    death_link: DungeonClawlerDeathlink
