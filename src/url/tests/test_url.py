import pytest
from url.tests.conftest import *
from url.url import *

@pytest.mark.valid
@pytest.mark.url
def test_get_url_valid():
    for linko in VALID_TEST_CASES:
        if "npmjs.com" in linko[0]:
            print(linko[2])
            assert (npm_to_git(linko[2]) != "guh")

@pytest.mark.invalid
@pytest.mark.url
def test_get_url_invalid():
    for linko in VALID_TEST_CASES:
        if "npmjs.com" in linko[0]:
            assert (npm_to_git(linko[2]+"jugador") == "guh")