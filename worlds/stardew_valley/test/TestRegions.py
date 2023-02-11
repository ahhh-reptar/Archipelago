import pytest

from . import SVTestBase
from .. import options
from ..regions import stardew_valley_regions, mandatory_connections


@pytest.mark.parametrize("region_and_exits", stardew_valley_regions, ids=[region for region, exits in stardew_valley_regions])
def test_region_exits_lead_somewhere(region_and_exits):
    connections = dict(mandatory_connections)
    for region_exit in region_and_exits[1]:
        assert region_exit in connections

# def test_all_mandatory_connections_lead_somewhere(self):
#     summer = self.get_item_by_name("Summer")
#     self.multiworld.state.collect(summer, event=True)
#     assert not self.world.logic.has("Sturgeon")(self.multiworld.state)
#     self.remove(summer)
