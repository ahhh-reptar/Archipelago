from typing import Iterable, Union, List


class RecipeSource:
    pass


class StarterSource(RecipeSource):
    pass


class ArchipelagoSource(RecipeSource):
    ap_item: List[str]

    def __init__(self, ap_item: Union[str, List[str]]):
        if isinstance(ap_item, str):
            ap_item = [ap_item]
        self.ap_item = ap_item


class LogicSource(RecipeSource):
    logic_rule: str

    def __init__(self, logic_rule: str):
        self.logic_rule = logic_rule


class QueenOfSauceSource(RecipeSource):
    year: int
    season: str
    day: int

    def __init__(self, year: int, season: str, day: int):
        self.year = year
        self.season = season
        self.day = day


class FriendshipSource(RecipeSource):
    friend: str
    hearts: int

    def __init__(self, friend: str, hearts: int):
        self.friend = friend
        self.hearts = hearts


class CutsceneSource(FriendshipSource):
    region: str

    def __init__(self, region: str, friend: str, hearts: int):
        super().__init__(friend, hearts)
        self.region = region


class SkillSource(RecipeSource):
    skill: str
    level: int

    def __init__(self, skill: str, level: int):
        self.skill = skill
        self.level = level


class ShopSource(RecipeSource):
    region: str
    price: int

    def __init__(self, region: str, price: int):
        self.region = region
        self.price = price


class ShopTradeSource(ShopSource):
    currency: str

    def __init__(self, region: str, currency: str, price: int):
        super().__init__(region, price)
        self.currency = currency


class SpecialOrderSource(RecipeSource):
    special_order: str

    def __init__(self, special_order: str):
        self.special_order = special_order
