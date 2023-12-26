from typing import Union

from ..mod_data import ModNames
from ... import options
from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...logic.option_logic import OptionLogicMixin
from ...logic.received_logic import ReceivedLogicMixin
from ...stardew_rule import StardewRule, true_


class ModElevatorLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elevator = ModElevatorLogic(*args, **kwargs)


class ModElevatorLogic(BaseLogic[Union[ReceivedLogicMixin, OptionLogicMixin]]):
    def has_skull_cavern_elevator_to_floor(self, floor: int) -> StardewRule:
        rule = self.logic.option.choice(options.ElevatorProgression,
                                        value=options.ElevatorProgression.option_vanilla,
                                        match=true_,
                                        no_match=self.logic.received("Progressive Skull Cavern Elevator", floor // 25))

        return self.logic.option.contains_choice_or_true(options.Mods,
                                                         value=ModNames.skull_cavern_elevator,
                                                         match=rule)
