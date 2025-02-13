from typing import List


class EnemyDifficulty:
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    easy_boss = "EasyBoss"
    medium_boss = "MediumBoss"
    hard_boss = "HardBoss"
    final_boss = "Final Boss"


class EnemyData:
    name: str
    difficulty: str
    is_boss: bool

    def __init__(self, name: str, difficulty: str, is_boss: bool = False):
        self.name = name
        self.difficulty = difficulty
        self.is_boss = is_boss
        all_enemies.append(self)


all_enemies: List[EnemyData] = []


class Enemy:
    lava_slime = EnemyData("Lava Slime", EnemyDifficulty.easy)
    plant_slime = EnemyData("Plant Slime", EnemyDifficulty.easy)
    ice_slime = EnemyData("Ice Slime", EnemyDifficulty.easy)

    bootshroom = EnemyData("Bootshroom", EnemyDifficulty.medium)
    bugabooh = EnemyData("Bugabooh", EnemyDifficulty.medium)
    burple = EnemyData("Burple", EnemyDifficulty.medium)
    barrakiddo = EnemyData("Barrakiddo", EnemyDifficulty.medium)
    groaker = EnemyData("Groaker", EnemyDifficulty.medium)
    gunrat = EnemyData("Gunrat", EnemyDifficulty.medium)
    fluffster = EnemyData("Fluffster", EnemyDifficulty.medium)
    wizzclops = EnemyData("Wizzclops", EnemyDifficulty.medium)
    inky = EnemyData("Inky", EnemyDifficulty.medium)
    monohive = EnemyData("Monohive", EnemyDifficulty.medium)
    purrpurr = EnemyData("Purrpurr", EnemyDifficulty.medium)
    thornweed = EnemyData("Thornweed", EnemyDifficulty.medium)
    spookolotl = EnemyData("Spookolotl", EnemyDifficulty.medium)

    robo_bomb = EnemyData("Robo-bomb", EnemyDifficulty.hard)
    bullhog = EnemyData("Bullhog", EnemyDifficulty.hard)
    bushling = EnemyData("Bushling", EnemyDifficulty.hard)
    avoidini = EnemyData("Avoidini", EnemyDifficulty.hard)
    sproing = EnemyData("Sproing", EnemyDifficulty.hard)
    dynamic_duo = EnemyData("Dynamic Duo", EnemyDifficulty.hard)
    fleye = EnemyData("Fleye", EnemyDifficulty.hard)
    stabigator = EnemyData("Stabigator", EnemyDifficulty.hard)
    slimy = EnemyData("Slimy", EnemyDifficulty.hard)
    defendalot_knight = EnemyData("Defendalot Knight", EnemyDifficulty.hard)
    punchy = EnemyData("Punchy", EnemyDifficulty.hard)

    prickwood = EnemyData("Prickwood", EnemyDifficulty.easy_boss)

    knight_commander = EnemyData("Knight Commander of the Order of Defendalot", EnemyDifficulty.medium_boss)

    goobert = EnemyData("Goobert, King of Slimes", EnemyDifficulty.hard_boss)
    lord_squidula = EnemyData("Lord Squidula", EnemyDifficulty.hard_boss)
    melimon = EnemyData("Melimon", EnemyDifficulty.hard_boss)
    mothilda = EnemyData("Mothilda", EnemyDifficulty.hard_boss)
    queen_beeatrice = EnemyData("Queen Beeatrice", EnemyDifficulty.hard_boss)
    walwrath = EnemyData("Walwrath the Blubbarian", EnemyDifficulty.hard_boss)

    squalo = EnemyData("Squalo \"The Loan\" Fishetti", EnemyDifficulty.final_boss)

