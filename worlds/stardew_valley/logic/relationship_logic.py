import math
from typing import Union, Collection

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .building_logic import BuildingLogicMixin
from .gift_logic import GiftLogicMixin
from .has_logic import HasLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from .time_logic import TimeLogicMixin
from .. import options
from ..data.villagers_data import all_villagers_by_name, Villager
from ..stardew_rule import StardewRule, True_, And, Or, Count
from ..strings.ap_names.mods.mod_items import SVEQuestItem
from ..strings.crop_names import Fruit
from ..strings.generic_names import Generic
from ..strings.gift_names import Gift
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.villager_names import NPC, ModNPC

possible_kids = ("Cute Baby", "Ugly Baby")


def npc_is_in_current_slot(name: str, enabled_mods: Collection[str]) -> bool:
    npc = all_villagers_by_name[name]
    mod = npc.mod_name
    return mod is None or mod in enabled_mods


def heart_item_name(npc: Union[str, Villager]) -> str:
    if isinstance(npc, Villager):
        npc = npc.name

    return f"{npc} <3"


class RelationshipLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relationship = RelationshipLogic(*args, **kwargs)


class RelationshipLogic(BaseLogic[Union[RelationshipLogicMixin, BuildingLogicMixin, SeasonLogicMixin, TimeLogicMixin, GiftLogicMixin, RegionLogicMixin,
ReceivedLogicMixin, HasLogicMixin, OptionLogicMixin]]):

    def can_date(self, npc: str) -> StardewRule:
        return self.logic.relationship.has_hearts(npc, 8) & self.logic.has(Gift.bouquet)

    def can_marry(self, npc: str) -> StardewRule:
        return self.logic.relationship.has_hearts(npc, 10) & self.logic.has(Gift.mermaid_pendant)

    def can_get_married(self) -> StardewRule:
        return self.logic.relationship.has_hearts(Generic.bachelor, 10) & self.logic.has(Gift.mermaid_pendant)

    def has_children(self, number_children: int) -> StardewRule:
        assert number_children >= 0, "Can't have a negative amount of children."
        if number_children == 0:
            return True_()

        return self.logic.option.choice(options.Friendsanity,
                                        value=options.Friendsanity.option_none,
                                        match=self.logic.relationship.can_reproduce(number_children),
                                        no_match=self.logic.received(possible_kids, number_children) & self.logic.building.has_house(2))

    def can_reproduce(self, number_children: int = 1) -> StardewRule:
        if number_children <= 0:
            return True_()
        baby_rules = [self.logic.relationship.can_get_married(), self.logic.building.has_house(2), self.logic.relationship.has_hearts(Generic.bachelor, 12),
                      self.logic.relationship.has_children(number_children - 1)]
        return And(*baby_rules)

    # Should be cached
    def has_hearts(self, npc: str, hearts: int = 1) -> StardewRule:
        # FIXME this should be split in smaller methods to it can all fit in a single human brain
        def create_rule(friendsanity, enabled_mods):
            if hearts <= 0:
                return True_()

            if friendsanity == options.Friendsanity.option_none:
                return self.logic.relationship.can_earn_relationship(npc, hearts)

            if npc not in all_villagers_by_name:

                if npc == Generic.any or npc == Generic.bachelor:
                    possible_friends = []
                    for name in all_villagers_by_name:
                        if not npc_is_in_current_slot(name, enabled_mods):
                            continue

                        if npc == Generic.any or all_villagers_by_name[name].bachelor:
                            possible_friends.append(self.logic.relationship.has_hearts(name, hearts))

                    return Or(*possible_friends)

                if npc == Generic.all:
                    mandatory_friends = []
                    for name in all_villagers_by_name:
                        if not npc_is_in_current_slot(name, enabled_mods):
                            continue

                        mandatory_friends.append(self.logic.relationship.has_hearts(name, hearts))

                    return And(*mandatory_friends)

                if npc.isnumeric():
                    possible_friends = []
                    for name in all_villagers_by_name:
                        if not npc_is_in_current_slot(name, enabled_mods):
                            continue
                        possible_friends.append(self.logic.relationship.has_hearts(name, hearts))

                    return Count(int(npc), possible_friends)

                return self.can_earn_relationship(npc, hearts)

            if not npc_is_in_current_slot(npc, enabled_mods):
                return True_()

            villager = all_villagers_by_name[npc]

            if friendsanity == options.Friendsanity.option_bachelors and not villager.bachelor:
                return self.logic.relationship.can_earn_relationship(npc, hearts)

            if friendsanity == options.Friendsanity.option_starting_npcs and not villager.available:
                return self.logic.relationship.can_earn_relationship(npc, hearts)

            is_capped_at_8 = villager.bachelor and friendsanity != options.Friendsanity.option_all_with_marriage
            if is_capped_at_8 and hearts > 8:
                return self.logic.relationship.received_hearts(villager.name, 8) & self.logic.relationship.can_earn_relationship(npc, hearts)

            return self.logic.relationship.received_hearts(villager.name, hearts)

        return self.logic.option.custom_rule(options.Friendsanity, options.Mods, rule_factory=create_rule)

    # Should be cached
    def received_hearts(self, npc: str, hearts: int) -> StardewRule:
        return self.logic.option.received(options.FriendsanityHeartSize,
                                          heart_item_name(npc),
                                          lambda friendsanity_heart_size: math.ceil(hearts / friendsanity_heart_size))

    @cache_self1
    def can_meet(self, npc: str) -> StardewRule:
        def create_rule(enabled_mods):
            if npc not in all_villagers_by_name or not npc_is_in_current_slot(npc, enabled_mods):
                return True_()

            villager = all_villagers_by_name[npc]
            rules = [self.logic.region.can_reach_any(villager.locations)]

            if npc == NPC.kent:
                rules.append(self.logic.time.has_year_two)

            elif npc == NPC.leo:
                rules.append(self.logic.received("Island West Turtle"))

            elif npc == ModNPC.lance:
                rules.append(self.logic.region.can_reach(Region.volcano_floor_10))

            elif npc == ModNPC.apples:
                rules.append(self.logic.has(Fruit.starfruit))

            elif npc == ModNPC.scarlett:
                scarlett_job = self.logic.received(SVEQuestItem.scarlett_job_offer)
                scarlett_spring = self.logic.season.has(Season.spring) & self.can_meet(ModNPC.andy)
                scarlett_summer = self.logic.season.has(Season.summer) & self.can_meet(ModNPC.susan)
                scarlett_fall = self.logic.season.has(Season.fall) & self.can_meet(ModNPC.sophia)
                rules.append(scarlett_job & (scarlett_spring | scarlett_summer | scarlett_fall))

            elif npc == ModNPC.morgan:
                rules.append(self.logic.received(SVEQuestItem.morgan_schooling))

            return And(*rules)

        return self.logic.option.custom_rule(options.Mods, rule_factory=create_rule)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        def create_rule(enabled_mods):
            rules = []
            for npc in all_villagers_by_name:
                if not npc_is_in_current_slot(npc, enabled_mods):
                    continue
                meet_rule = self.logic.relationship.can_meet(npc)
                rules.append(meet_rule)
            rules.append(self.logic.gifts.has_any_universal_love)
            return And(*rules)

        return self.logic.option.custom_rule(options.Mods, rule_factory=create_rule)

    # Should be cached
    def can_earn_relationship(self, npc: str, hearts: int = 0) -> StardewRule:
        if hearts <= 0:
            return True_()

        def create_rule(friendsanity_heart_size, enabled_mods):
            previous_heart = hearts - friendsanity_heart_size
            previous_heart_rule = self.logic.relationship.has_hearts(npc, previous_heart)

            if npc not in all_villagers_by_name or not npc_is_in_current_slot(npc, enabled_mods):
                return previous_heart_rule

            rules = [previous_heart_rule, self.logic.relationship.can_meet(npc)]
            villager = all_villagers_by_name[npc]
            if hearts > 2 or hearts > friendsanity_heart_size:
                rules.append(self.logic.season.has(villager.birthday))

            if villager.bachelor:
                if hearts > 8:
                    rules.append(self.logic.relationship.can_date(npc))
                if hearts > 10:
                    rules.append(self.logic.relationship.can_marry(npc))

            return And(*rules)

        return self.logic.option.custom_rule(options.FriendsanityHeartSize, options.Mods, rule_factory=create_rule)
