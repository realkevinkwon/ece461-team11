import pytest
from url.tests.conftest import *
from url.ramp_up import *


@pytest.mark.valid
@pytest.mark.ramp
def test_get_ramp_up_score_valid():
    print("\n\ntesting get_ramp_up_score() with valid test cases")
    for url, owner, repo in VALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        ramp_up_score = get_ramp_up_score(owner, repo, TOKEN)

        assert type(ramp_up_score) == float
        assert ramp_up_score >= 0.0
        assert ramp_up_score <= 1.0

@pytest.mark.invalid
@pytest.mark.ramp
def test_get_ramp_up_score_invalid():
    print("\n\ntesting get_ramp_up_score() with invalid test cases")
    for url, owner, repo in INVALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        ramp_up_score = get_ramp_up_score(owner, repo, TOKEN)

        assert type(ramp_up_score) == float
        assert ramp_up_score < 0.0