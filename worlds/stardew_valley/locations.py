from dataclasses import dataclass
from typing import Optional, Dict, Protocol

from . import options

LOCATION_CODE_OFFSET = 717000


@dataclass(frozen=True)
class LocationData:
    code_without_offset: Optional[int]
    region: str
    name: str

    @property
    def code(self) -> Optional[int]:
        return LOCATION_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


class StardewLocationCollector(Protocol):
    def __call__(self, name: str, code: Optional[int], region: str) -> None:
        raise NotImplementedError


crafts_room_bundle = [
    LocationData(1, "Crafts Room", "Spring Foraging Bundle"),
    LocationData(2, "Crafts Room", "Summer Foraging Bundle"),
    LocationData(3, "Crafts Room", "Fall Foraging Bundle"),
    LocationData(4, "Crafts Room", "Winter Foraging Bundle"),
    LocationData(5, "Crafts Room", "Construction Bundle"),
    LocationData(6, "Crafts Room", "Exotic Foraging Bundle"),
]

pantry_bundles = [
    LocationData(7, "Pantry", "Spring Crops Bundle"),
    LocationData(8, "Pantry", "Summer Crops Bundle"),
    LocationData(9, "Pantry", "Fall Crops Bundle"),
    LocationData(10, "Pantry", "Quality Crops Bundle"),
    LocationData(11, "Pantry", "Animal Bundle"),
    LocationData(12, "Pantry", "Artisan Bundle"),
]

fish_tank_bundles = [
    LocationData(13, "Fish Tank", "River Fish Bundle"),
    LocationData(14, "Fish Tank", "Lake Fish Bundle"),
    LocationData(15, "Fish Tank", "Ocean Fish Bundle"),
    LocationData(16, "Fish Tank", "Night Fishing Bundle"),
    LocationData(17, "Fish Tank", "Crab Pot Bundle"),
    LocationData(18, "Fish Tank", "Specialty Fish Bundle"),
]

boiler_room_bundles = [
    LocationData(19, "Boiler Room", "Blacksmith's Bundle"),
    LocationData(20, "Boiler Room", "Geologist's Bundle"),
    LocationData(21, "Boiler Room", "Adventurer's Bundle"),
]

bulletin_board_bundles = [
    LocationData(22, "Bulletin Board", "Chef's Bundle"),
    LocationData(23, "Bulletin Board", "Dye Bundle"),
    LocationData(24, "Bulletin Board", "Field Research Bundle"),
    LocationData(25, "Bulletin Board", "Fodder Bundle"),
    LocationData(26, "Bulletin Board", "Enchanter's Bundle"),
]

vault_bundles = [
    LocationData(27, "Vault", "2,500g Bundle"),
    LocationData(28, "Vault", "5,000g Bundle"),
    LocationData(29, "Vault", "10,000g Bundle"),
    LocationData(30, "Vault", "25,000g Bundle"),
]

community_center_bundles = [*crafts_room_bundle, *pantry_bundles, *fish_tank_bundles,
                            *boiler_room_bundles, *bulletin_board_bundles, *vault_bundles]

abandoned_jojamart_bundles = [
    LocationData(31, "Abandoned JojaMart", "The Missing Bundle"),
]

community_center_rooms = [
    LocationData(32, "Crafts Room", "Complete Crafts Room"),
    LocationData(33, "Pantry", "Complete Pantry"),
    LocationData(34, "Fish Tank", "Complete Fish Tank"),
    LocationData(35, "Boiler Room", "Complete Boiler Room"),
    LocationData(36, "Bulletin Board", "Complete Bulletin Board"),
    LocationData(37, "Vault", "Complete Vault"),
]

backpack_upgrades = [
    LocationData(101, "Pierre's General Store", "Large Pack"),
    LocationData(102, "Pierre's General Store", "Deluxe Pack"),
]

tool_upgrades = [
    LocationData(103, "Clint's Blacksmith", "Copper Hoe Upgrade"),
    LocationData(104, "Clint's Blacksmith", "Iron Hoe Upgrade"),
    LocationData(105, "Clint's Blacksmith", "Gold Hoe Upgrade"),
    LocationData(106, "Clint's Blacksmith", "Iridium Hoe Upgrade"),
    LocationData(107, "Clint's Blacksmith", "Copper Pickaxe Upgrade"),
    LocationData(108, "Clint's Blacksmith", "Iron Pickaxe Upgrade"),
    LocationData(109, "Clint's Blacksmith", "Gold Pickaxe Upgrade"),
    LocationData(110, "Clint's Blacksmith", "Iridium Pickaxe Upgrade"),
    LocationData(111, "Clint's Blacksmith", "Copper Axe Upgrade"),
    LocationData(112, "Clint's Blacksmith", "Iron Axe Upgrade"),
    LocationData(113, "Clint's Blacksmith", "Gold Axe Upgrade"),
    LocationData(114, "Clint's Blacksmith", "Iridium Axe Upgrade"),
    LocationData(115, "Clint's Blacksmith", "Copper Watering Can Upgrade"),
    LocationData(116, "Clint's Blacksmith", "Iron Watering Can Upgrade"),
    LocationData(117, "Clint's Blacksmith", "Gold Watering Can Upgrade"),
    LocationData(118, "Clint's Blacksmith", "Iridium Watering Can Upgrade"),
    LocationData(119, "Clint's Blacksmith", "Copper Trash Can Upgrade"),
    LocationData(120, "Clint's Blacksmith", "Iron Trash Can Upgrade"),
    LocationData(121, "Clint's Blacksmith", "Gold Trash Can Upgrade"),
    LocationData(122, "Clint's Blacksmith", "Iridium Trash Can Upgrade"),
    LocationData(123, "Willy's Fish Shop", "Purchase Training Rod"),
    LocationData(124, "Stardew Valley", "Bamboo Pole Cutscene"),
    LocationData(125, "Willy's Fish Shop", "Purchase Fiberglass Rod"),
    LocationData(126, "Willy's Fish Shop", "Purchase Iridium Rod"),
]

the_mines = [
    LocationData(201, "The Mines - Floor 10", "The Mines Floor 10 Treasure"),
    LocationData(202, "The Mines - Floor 20", "The Mines Floor 20 Treasure"),
    LocationData(203, "The Mines - Floor 40", "The Mines Floor 40 Treasure"),
    LocationData(204, "The Mines - Floor 50", "The Mines Floor 50 Treasure"),
    LocationData(205, "The Mines - Floor 60", "The Mines Floor 60 Treasure"),
    LocationData(206, "The Mines - Floor 70", "The Mines Floor 70 Treasure"),
    LocationData(207, "The Mines - Floor 80", "The Mines Floor 80 Treasure"),
    LocationData(208, "The Mines - Floor 90", "The Mines Floor 90 Treasure"),
    LocationData(209, "The Mines - Floor 100", "The Mines Floor 100 Treasure"),
    LocationData(210, "The Mines - Floor 110", "The Mines Floor 110 Treasure"),
    LocationData(211, "The Mines - Floor 120", "The Mines Floor 120 Treasure"),
    LocationData(212, "Quarry", "Grim Reaper statue"),
    LocationData(213, "The Mines", "The Mines Entrance Cutscene"),
]

the_mines_elevators = [
    LocationData(214, "The Mines - Floor 5", "Floor 5 Elevator"),
    LocationData(215, "The Mines - Floor 10", "Floor 10 Elevator"),
    LocationData(216, "The Mines - Floor 15", "Floor 15 Elevator"),
    LocationData(217, "The Mines - Floor 20", "Floor 20 Elevator"),
    LocationData(218, "The Mines - Floor 25", "Floor 25 Elevator"),
    LocationData(219, "The Mines - Floor 30", "Floor 30 Elevator"),
    LocationData(220, "The Mines - Floor 35", "Floor 35 Elevator"),
    LocationData(221, "The Mines - Floor 40", "Floor 40 Elevator"),
    LocationData(222, "The Mines - Floor 45", "Floor 45 Elevator"),
    LocationData(223, "The Mines - Floor 50", "Floor 50 Elevator"),
    LocationData(224, "The Mines - Floor 55", "Floor 55 Elevator"),
    LocationData(225, "The Mines - Floor 60", "Floor 60 Elevator"),
    LocationData(226, "The Mines - Floor 65", "Floor 65 Elevator"),
    LocationData(227, "The Mines - Floor 70", "Floor 70 Elevator"),
    LocationData(228, "The Mines - Floor 75", "Floor 75 Elevator"),
    LocationData(229, "The Mines - Floor 80", "Floor 80 Elevator"),
    LocationData(230, "The Mines - Floor 85", "Floor 85 Elevator"),
    LocationData(231, "The Mines - Floor 90", "Floor 90 Elevator"),
    LocationData(232, "The Mines - Floor 95", "Floor 95 Elevator"),
    LocationData(233, "The Mines - Floor 100", "Floor 100 Elevator"),
    LocationData(234, "The Mines - Floor 105", "Floor 105 Elevator"),
    LocationData(235, "The Mines - Floor 110", "Floor 110 Elevator"),
    LocationData(236, "The Mines - Floor 115", "Floor 115 Elevator"),
    LocationData(237, "The Mines - Floor 120", "Floor 120 Elevator"),
]

skills_levels = [
    LocationData(301, "Stardew Valley", "Level 1 Farming"),
    LocationData(302, "Stardew Valley", "Level 2 Farming"),
    LocationData(303, "Stardew Valley", "Level 3 Farming"),
    LocationData(304, "Stardew Valley", "Level 4 Farming"),
    LocationData(305, "Stardew Valley", "Level 5 Farming"),
    LocationData(306, "Stardew Valley", "Level 6 Farming"),
    LocationData(307, "Stardew Valley", "Level 7 Farming"),
    LocationData(308, "Stardew Valley", "Level 8 Farming"),
    LocationData(309, "Stardew Valley", "Level 9 Farming"),
    LocationData(310, "Stardew Valley", "Level 10 Farming"),
    LocationData(311, "Stardew Valley", "Level 1 Fishing"),
    LocationData(312, "Stardew Valley", "Level 2 Fishing"),
    LocationData(313, "Stardew Valley", "Level 3 Fishing"),
    LocationData(314, "Stardew Valley", "Level 4 Fishing"),
    LocationData(315, "Stardew Valley", "Level 5 Fishing"),
    LocationData(316, "Stardew Valley", "Level 6 Fishing"),
    LocationData(317, "Stardew Valley", "Level 7 Fishing"),
    LocationData(318, "Stardew Valley", "Level 8 Fishing"),
    LocationData(319, "Stardew Valley", "Level 9 Fishing"),
    LocationData(320, "Stardew Valley", "Level 10 Fishing"),
    LocationData(321, "Stardew Valley", "Level 1 Foraging"),
    LocationData(322, "Stardew Valley", "Level 2 Foraging"),
    LocationData(323, "Stardew Valley", "Level 3 Foraging"),
    LocationData(324, "Stardew Valley", "Level 4 Foraging"),
    LocationData(325, "Stardew Valley", "Level 5 Foraging"),
    LocationData(326, "Stardew Valley", "Level 6 Foraging"),
    LocationData(327, "Stardew Valley", "Level 7 Foraging"),
    LocationData(328, "Stardew Valley", "Level 8 Foraging"),
    LocationData(329, "Stardew Valley", "Level 9 Foraging"),
    LocationData(330, "Stardew Valley", "Level 10 Foraging"),
    LocationData(331, "Stardew Valley", "Level 1 Mining"),
    LocationData(332, "Stardew Valley", "Level 2 Mining"),
    LocationData(333, "Stardew Valley", "Level 3 Mining"),
    LocationData(334, "Stardew Valley", "Level 4 Mining"),
    LocationData(335, "Stardew Valley", "Level 5 Mining"),
    LocationData(336, "Stardew Valley", "Level 6 Mining"),
    LocationData(337, "Stardew Valley", "Level 7 Mining"),
    LocationData(338, "Stardew Valley", "Level 8 Mining"),
    LocationData(339, "Stardew Valley", "Level 9 Mining"),
    LocationData(340, "Stardew Valley", "Level 10 Mining"),
    LocationData(341, "Stardew Valley", "Level 1 Combat"),
    LocationData(342, "Stardew Valley", "Level 2 Combat"),
    LocationData(343, "Stardew Valley", "Level 3 Combat"),
    LocationData(344, "Stardew Valley", "Level 4 Combat"),
    LocationData(345, "Stardew Valley", "Level 5 Combat"),
    LocationData(346, "Stardew Valley", "Level 6 Combat"),
    LocationData(347, "Stardew Valley", "Level 7 Combat"),
    LocationData(348, "Stardew Valley", "Level 8 Combat"),
    LocationData(349, "Stardew Valley", "Level 9 Combat"),
    LocationData(350, "Stardew Valley", "Level 10 Combat"),
]

buildings = [
    LocationData(401, "Stardew Valley", "Coop Blueprint"),
    LocationData(402, "Stardew Valley", "Big Coop Blueprint"),
    LocationData(403, "Stardew Valley", "Deluxe Coop Blueprint"),
    LocationData(404, "Stardew Valley", "Barn Blueprint"),
    LocationData(405, "Stardew Valley", "Big Barn Blueprint"),
    LocationData(406, "Stardew Valley", "Deluxe Barn Blueprint"),
    LocationData(407, "Stardew Valley", "Well Blueprint"),
    LocationData(408, "Stardew Valley", "Silo Blueprint"),
    LocationData(409, "Stardew Valley", "Mill Blueprint"),
    LocationData(410, "Stardew Valley", "Shed Blueprint"),
    LocationData(411, "Stardew Valley", "Big Shed Blueprint"),
    LocationData(412, "Stardew Valley", "Fish Pond Blueprint"),
    LocationData(413, "Stardew Valley", "Stable Blueprint"),
    LocationData(414, "Stardew Valley", "Slime Hutch Blueprint"),
    LocationData(415, "Stardew Valley", "Shipping Bin Blueprint"),
    LocationData(416, "Stardew Valley", "House Kitchen Blueprint"),
    LocationData(417, "Stardew Valley", "House Kids Room Blueprint"),
    LocationData(418, "Stardew Valley", "House Cellar Blueprint"),
]

story_quests = [
    LocationData(501, "Stardew Valley", "Introductions"),
    LocationData(502, "Stardew Valley", "How To Win Friends"),
    LocationData(503, "Stardew Valley", "Getting Started"),
    LocationData(504, "Stardew Valley", "Raising Animals"),
    LocationData(505, "Stardew Valley", "Advancement"),
    LocationData(506, "Stardew Valley", "Archaeology"),
    LocationData(507, "Stardew Valley", "Meet The Wizard"),
    LocationData(508, "Stardew Valley", "Forging Ahead"),
    LocationData(509, "Stardew Valley", "Smelting"),
    LocationData(510, "Stardew Valley", "Initiation"),
    LocationData(511, "Stardew Valley", "Robin's Lost Axe"),
    LocationData(512, "Stardew Valley", "Jodi's Request"),
    LocationData(513, "Stardew Valley", "Mayor's \"Shorts\""),
    LocationData(514, "Stardew Valley", "Blackberry Basket"),
    LocationData(515, "Stardew Valley", "Marnie's Request"),
    LocationData(516, "Stardew Valley", "Pam Is Thirsty"),
    LocationData(517, "Stardew Valley", "A Dark Reagent"),
    LocationData(518, "Stardew Valley", "Cow's Delight"),
    LocationData(519, "Stardew Valley", "The Skull Key"),
    LocationData(520, "Stardew Valley", "Crop Research"),
    LocationData(521, "Stardew Valley", "Knee Therapy"),
    LocationData(522, "Stardew Valley", "Robin's Request"),
    LocationData(523, "Stardew Valley", "Qi's Challenge"),
    LocationData(524, "Stardew Valley", "The Mysterious Qi"),
    LocationData(525, "Stardew Valley", "Carving Pumpkins"),
    LocationData(526, "Stardew Valley", "A Winter Mystery"),
    LocationData(527, "Stardew Valley", "Strange Note"),
    LocationData(528, "Stardew Valley", "Cryptic Note"),
    LocationData(529, "Stardew Valley", "Fresh Fruit"),
    LocationData(530, "Stardew Valley", "Aquatic Research"),
    LocationData(531, "Stardew Valley", "A Soldier's Star"),
    LocationData(532, "Stardew Valley", "Mayor's Need"),
    LocationData(533, "Stardew Valley", "Wanted: Lobster"),
    LocationData(534, "Stardew Valley", "Pam Needs Juice"),
    LocationData(535, "Stardew Valley", "Fish Casserole"),
    LocationData(536, "Stardew Valley", "Catch A Squid"),
    LocationData(537, "Stardew Valley", "Fish Stew"),
    LocationData(538, "Stardew Valley", "Pierre's Notice"),
    LocationData(539, "Stardew Valley", "Clint's Attempt"),
    LocationData(540, "Stardew Valley", "A Favor For Clint"),
    LocationData(541, "Stardew Valley", "Staff Of Power"),
    LocationData(542, "Stardew Valley", "Granny's Gift"),
    LocationData(543, "Stardew Valley", "Exotic Spirits"),
    LocationData(544, "Stardew Valley", "Catch a Lingcod"),
]

arcade_machines = [
    LocationData(601, "JotPK World 1", "JotPK: Boots 1"),
    LocationData(602, "JotPK World 1", "JotPK: Boots 2"),
    LocationData(603, "JotPK World 1", "JotPK: Gun 1"),
    LocationData(604, "JotPK World 2", "JotPK: Gun 2"),
    LocationData(605, "JotPK World 2", "JotPK: Gun 3"),
    LocationData(606, "JotPK World 3", "JotPK: Super Gun"),
    LocationData(607, "JotPK World 1", "JotPK: Ammo 1"),
    LocationData(608, "JotPK World 2", "JotPK: Ammo 2"),
    LocationData(609, "JotPK World 3", "JotPK: Ammo 3"),
    LocationData(610, "JotPK World 1", "JotPK: Cowboy 1"),
    LocationData(611, "JotPK World 2", "JotPK: Cowboy 2"),
    LocationData(612, "Junimo Kart 1", "Junimo Kart: Crumble Cavern"),
    LocationData(613, "Junimo Kart 1", "Junimo Kart: Slippery Slopes"),
    LocationData(614, "Junimo Kart 2", "Junimo Kart: Secret Level"),
    LocationData(615, "Junimo Kart 2", "Junimo Kart: The Gem Sea Giant"),
    LocationData(616, "Junimo Kart 2", "Junimo Kart: Slomp's Stomp"),
    LocationData(617, "Junimo Kart 2", "Junimo Kart: Ghastly Galleon"),
    LocationData(618, "Junimo Kart 3", "Junimo Kart: Glowshroom Grotto"),
    LocationData(619, "Junimo Kart 3", "Junimo Kart: Red Hot Rollercoaster"),
]

arcade_machines_victories = [
    LocationData(620, "JotPK World 3", "Journey of the Prairie King Victory"),
    LocationData(621, "Junimo Kart 3", "Junimo Kart: Sunset Speedway (Victory)"),
]

other_locations = [
    LocationData(701, "Secret Woods", "Old Master Cannoli"),
    LocationData(702, "Stardew Valley", "Beach Bridge Repair"),
    LocationData(703, "The Desert", "Galaxy Sword Shrine"),
]

help_wanted_quests = [
    LocationData(801, "Stardew Valley", "Help Wanted: Gathering 1"),
    LocationData(802, "Stardew Valley", "Help Wanted: Gathering 2"),
    LocationData(803, "Stardew Valley", "Help Wanted: Gathering 3"),
    LocationData(804, "Stardew Valley", "Help Wanted: Gathering 4"),
    LocationData(805, "Stardew Valley", "Help Wanted: Gathering 5"),
    LocationData(806, "Stardew Valley", "Help Wanted: Gathering 6"),
    LocationData(807, "Stardew Valley", "Help Wanted: Gathering 7"),
    LocationData(808, "Stardew Valley", "Help Wanted: Gathering 8"),
    LocationData(811, "Stardew Valley", "Help Wanted: Slay Monsters 1"),
    LocationData(812, "Stardew Valley", "Help Wanted: Slay Monsters 2"),
    LocationData(813, "Stardew Valley", "Help Wanted: Slay Monsters 3"),
    LocationData(814, "Stardew Valley", "Help Wanted: Slay Monsters 4"),
    LocationData(815, "Stardew Valley", "Help Wanted: Slay Monsters 5"),
    LocationData(816, "Stardew Valley", "Help Wanted: Slay Monsters 6"),
    LocationData(817, "Stardew Valley", "Help Wanted: Slay Monsters 7"),
    LocationData(818, "Stardew Valley", "Help Wanted: Slay Monsters 8"),
    LocationData(821, "Stardew Valley", "Help Wanted: Fishing 1"),
    LocationData(822, "Stardew Valley", "Help Wanted: Fishing 2"),
    LocationData(823, "Stardew Valley", "Help Wanted: Fishing 3"),
    LocationData(824, "Stardew Valley", "Help Wanted: Fishing 4"),
    LocationData(825, "Stardew Valley", "Help Wanted: Fishing 5"),
    LocationData(826, "Stardew Valley", "Help Wanted: Fishing 6"),
    LocationData(827, "Stardew Valley", "Help Wanted: Fishing 7"),
    LocationData(828, "Stardew Valley", "Help Wanted: Fishing 8"),
    LocationData(841, "Stardew Valley", "Help Wanted: Item Delivery 1"),
    LocationData(842, "Stardew Valley", "Help Wanted: Item Delivery 2"),
    LocationData(843, "Stardew Valley", "Help Wanted: Item Delivery 3"),
    LocationData(844, "Stardew Valley", "Help Wanted: Item Delivery 4"),
    LocationData(845, "Stardew Valley", "Help Wanted: Item Delivery 5"),
    LocationData(846, "Stardew Valley", "Help Wanted: Item Delivery 6"),
    LocationData(847, "Stardew Valley", "Help Wanted: Item Delivery 7"),
    LocationData(848, "Stardew Valley", "Help Wanted: Item Delivery 8"),
    LocationData(849, "Stardew Valley", "Help Wanted: Item Delivery 9"),
    LocationData(850, "Stardew Valley", "Help Wanted: Item Delivery 10"),
    LocationData(851, "Stardew Valley", "Help Wanted: Item Delivery 11"),
    LocationData(852, "Stardew Valley", "Help Wanted: Item Delivery 12"),
    LocationData(853, "Stardew Valley", "Help Wanted: Item Delivery 13"),
    LocationData(854, "Stardew Valley", "Help Wanted: Item Delivery 14"),
    LocationData(855, "Stardew Valley", "Help Wanted: Item Delivery 15"),
    LocationData(856, "Stardew Valley", "Help Wanted: Item Delivery 16"),
    LocationData(857, "Stardew Valley", "Help Wanted: Item Delivery 17"),
    LocationData(858, "Stardew Valley", "Help Wanted: Item Delivery 18"),
    LocationData(859, "Stardew Valley", "Help Wanted: Item Delivery 19"),
    LocationData(860, "Stardew Valley", "Help Wanted: Item Delivery 20"),
    LocationData(861, "Stardew Valley", "Help Wanted: Item Delivery 21"),
    LocationData(862, "Stardew Valley", "Help Wanted: Item Delivery 22"),
    LocationData(863, "Stardew Valley", "Help Wanted: Item Delivery 23"),
    LocationData(864, "Stardew Valley", "Help Wanted: Item Delivery 24"),
    LocationData(865, "Stardew Valley", "Help Wanted: Item Delivery 25"),
    LocationData(866, "Stardew Valley", "Help Wanted: Item Delivery 26"),
    LocationData(867, "Stardew Valley", "Help Wanted: Item Delivery 27"),
    LocationData(868, "Stardew Valley", "Help Wanted: Item Delivery 28"),
    LocationData(869, "Stardew Valley", "Help Wanted: Item Delivery 29"),
    LocationData(870, "Stardew Valley", "Help Wanted: Item Delivery 30"),
    LocationData(871, "Stardew Valley", "Help Wanted: Item Delivery 31"),
    LocationData(872, "Stardew Valley", "Help Wanted: Item Delivery 32"),
]

events_locations = [
    LocationData(None, "Stardew Valley", "Succeed Grandpa's Evaluation"),
    LocationData(None, "Community Center", "Complete Community Center"),
    LocationData(None, "The Mines - Floor 120", "Reach the Bottom of The Mines"),
    LocationData(None, "Skull Cavern", "Complete Quest Cryptic Note"),
    LocationData(None, "Stardew Valley", "Summer"),
    LocationData(None, "Stardew Valley", "Fall"),
    LocationData(None, "Stardew Valley", "Winter"),
    LocationData(None, "Stardew Valley", "Year Two"),
]

all_locations = [
    *community_center_bundles,
    *community_center_rooms,
    *backpack_upgrades,
    *the_mines,
    *tool_upgrades,
    *events_locations,
    *the_mines_elevators,
    *skills_levels,
    *buildings,
    *other_locations,
    *arcade_machines,
    *arcade_machines_victories,
    *story_quests,
    *help_wanted_quests,
]
location_table: Dict[str, LocationData] = {location.name: location for location in all_locations}


def extend_help_wanted_quests(randomized_locations: list[LocationData], desired_number_of_quests: int):
    for i in range(0, desired_number_of_quests):
        batch = i // 7
        index_this_batch = i % 7
        if index_this_batch < 4:
            randomized_locations.append(location_table[f"Help Wanted: Item Delivery {(batch * 4) + index_this_batch + 1}"])
        elif index_this_batch == 4:
            randomized_locations.append(location_table[f"Help Wanted: Fishing {batch + 1}"])
        elif index_this_batch == 5:
            randomized_locations.append(location_table[f"Help Wanted: Slay Monsters {batch + 1}"])
        elif index_this_batch == 6:
            randomized_locations.append(location_table[f"Help Wanted: Gathering {batch + 1}"])


def create_locations(location_collector: StardewLocationCollector, world_options: options.StardewOptions):
    randomized_locations = []

    randomized_locations.extend(community_center_bundles)
    randomized_locations.extend(community_center_rooms)
    randomized_locations.extend(the_mines)

    if not world_options[options.BackpackProgression] == options.BackpackProgression.option_vanilla:
        randomized_locations.extend(backpack_upgrades)

    if not world_options[options.ToolProgression] == options.ToolProgression.option_vanilla:
        randomized_locations.extend(tool_upgrades)

    if not world_options[options.TheMinesElevatorsProgression] == options.TheMinesElevatorsProgression.option_vanilla:
        randomized_locations.extend(the_mines_elevators)

    if not world_options[options.SkillProgression] == options.SkillProgression.option_vanilla:
        randomized_locations.extend(skills_levels)

    if not world_options[options.BuildingProgression] == options.BuildingProgression.option_vanilla:
        randomized_locations.extend(buildings)

    if not world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_disabled:
        randomized_locations.extend(arcade_machines_victories)

    if world_options[options.ArcadeMachineLocations] == options.ArcadeMachineLocations.option_full_shuffling:
        randomized_locations.extend(arcade_machines)

    randomized_locations.extend(story_quests)
    extend_help_wanted_quests(randomized_locations, world_options[options.HelpWantedLocations])
    randomized_locations.extend(other_locations)

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)
