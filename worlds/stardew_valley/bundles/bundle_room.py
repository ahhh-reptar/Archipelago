from dataclasses import dataclass
from random import Random
from typing import List

from .bundle import Bundle, BundleTemplate
from ..options import BundlePrice, StardewValleyOptions


@dataclass
class BundleRoom:
    name: str
    bundles: List[Bundle]


@dataclass
class BundleRoomTemplate:
    name: str
    bundles: List[BundleTemplate]
    number_bundles: int

    def create_bundle_room(self, bundle_price_option: BundlePrice, random: Random, options: StardewValleyOptions):
        forced_bundles = ["Legendary Fish Bundle", "Carnival Bundle", "Qi's Helper Bundle", "Gambler's Bundle", "Spring Fishing Bundle",
                          "Summer Crops Bundle", "Winter Foraging Bundle", "Clay Farmer Bundle", "MinMaxer Bundle"]
        filtered_bundles = [bundle for bundle in self.bundles if bundle.can_appear(options)]
        filtered_bundle_names = [bundle.name for bundle in filtered_bundles]
        chosen_bundles = random.sample(filtered_bundles, self.number_bundles)
        chosen_bundle_names = [bundle.name for bundle in chosen_bundles]

        all_forced_present = False
        while not all_forced_present:
            all_forced_present = True
            for forced_bundle_name in forced_bundles:
                if forced_bundle_name in filtered_bundle_names and forced_bundle_name not in chosen_bundle_names:
                    all_forced_present = False
            if not all_forced_present:
                filtered_bundles = [bundle for bundle in self.bundles if bundle.can_appear(options)]
                filtered_bundle_names = [bundle.name for bundle in filtered_bundles]
                chosen_bundles = random.sample(filtered_bundles, self.number_bundles)
                chosen_bundle_names = [bundle.name for bundle in chosen_bundles]

        return BundleRoom(self.name, [bundle.create_bundle(bundle_price_option, random, options) for bundle in chosen_bundles])
