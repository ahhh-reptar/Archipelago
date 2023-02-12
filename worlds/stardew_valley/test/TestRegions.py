import pytest

from ..regions import stardew_valley_regions, mandatory_connections

connections_by_name = {connection.name for connection in mandatory_connections}
regions_by_name = {region[0] for region in stardew_valley_regions}


@pytest.mark.parametrize("region", stardew_valley_regions, ids=[region for region, _ in stardew_valley_regions])
def test_region_exits_lead_somewhere(region):
    region, exits = region
    for exit in exits:
        assert exit in connections_by_name, f"{region} is leading to {exit} but it does not exist."


@pytest.mark.parametrize("connection", mandatory_connections, ids=[connection.name for connection in mandatory_connections])
def test_region_exits_lead_somewhere(connection):
    assert connection.destination in regions_by_name, f"{connection.name} is leading to {connection.destination} but it does not exist."
