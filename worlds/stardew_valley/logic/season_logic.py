from typing import Iterable, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .option_logic import OptionLogicMixin
from .received_logic import ReceivedLogicMixin
from .time_logic import TimeLogicMixin
from ..options import SeasonRandomization
from ..stardew_rule import StardewRule, True_, Or
from ..strings.generic_names import Generic
from ..strings.season_names import Season

seasons_order = [Season.spring, Season.summer, Season.fall, Season.winter]


class SeasonLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.season = SeasonLogic(*args, **kwargs)


class SeasonLogic(BaseLogic[Union[SeasonLogicMixin, TimeLogicMixin, ReceivedLogicMixin, OptionLogicMixin]]):

    @cache_self1
    def has(self, season: str) -> StardewRule:
        if season == Generic.any:
            return True_()

        return self.logic.option.choose(SeasonRandomization, {
            SeasonRandomization.option_disabled: True_() if season == Season.spring else self.logic.time.has_lived_months(1),
            SeasonRandomization.option_progressive: self.logic.received(Season.progressive, seasons_order.index(season)),
            SeasonRandomization.option_randomized: self.logic.received(season),
            SeasonRandomization.option_randomized_not_winter: self.logic.received(season),
        })

    def has_any(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        return Or(*(self.logic.season.has(season) for season in seasons))

    def has_any_not_winter(self):
        return self.logic.season.has_any([Season.spring, Season.summer, Season.fall])
