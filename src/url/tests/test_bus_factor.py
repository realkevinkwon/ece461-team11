import pytest
from url.tests.conftest import *
from url.bus_factor import *


@pytest.mark.valid
@pytest.mark.bus
def test_get_bus_factor_score():
    #high bus score
    assert get_bus_factor_score("apache", "superset", TOKEN) == 1.0
    #medium bus score
    assert get_bus_factor_score("serenity-bdd", "serenity-junit-starter", TOKEN) == 0.75
    #low bus score
    assert get_bus_factor_score("Chise7", "ECE461_Team11", TOKEN) == 0.0