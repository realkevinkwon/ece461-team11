import pytest
from url.tests.conftest import *
from url.responsive_maintainer import *
from github import Github


@pytest.mark.valid
@pytest.mark.weekly
def test_get_weekly_subscore_valid():
    print("\n\ntesting get_weekly_subscore() with valid test cases")

    g = Github(TOKEN)
    for url, owner, repo in VALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")
        
        git_repo = g.get_repo(f"{owner}/{repo}")
        weekly_subscore = get_weekly_subscore(git_repo)

        assert type(weekly_subscore) == float
        assert weekly_subscore >= 0.0
        assert weekly_subscore <= 1.0


@pytest.mark.invalid
@pytest.mark.weekly
def test_get_weekly_subscore_invalid():
    print("\n\ntesting get_weekly_subscore() with invalid test cases")

    g = Github(TOKEN)
    for url, owner, repo in INVALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")
        
        git_repo = g.get_repo(f"{owner}/{repo}")
        weekly_subscore = get_weekly_subscore(git_repo)

        assert type(weekly_subscore) == float
        assert weekly_subscore >= 0.0
        assert weekly_subscore <= 1.0


@pytest.mark.valid
@pytest.mark.yearly
def test_get_yearly_subscore_valid():
    print("\n\ntesting get_yearly_subscore() with valid test cases")

    g = Github(TOKEN)
    for url, owner, repo in VALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        git_repo = g.get_repo(f"{owner}/{repo}")
        yearly_subscore = get_yearly_subscore(git_repo)

        assert type(yearly_subscore) == float
        assert yearly_subscore >= 0.0
        assert yearly_subscore <= 1.0
        

@pytest.mark.invalid
@pytest.mark.yearly
def test_get_yearly_subscore_invalid():
    print("\n\ntesting get_yearly_subscore() with invalid test cases")

    g = Github(TOKEN)
    for url, owner, repo in INVALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        git_repo = g.get_repo(f"{owner}/{repo}")
        yearly_subscore = get_yearly_subscore(git_repo)

        assert type(yearly_subscore) == float
        assert yearly_subscore >= 0.0
        assert yearly_subscore <= 1.0


@pytest.mark.valid
@pytest.mark.rm
def test_get_rm_score_valid():
    print("\n\ntesting get_rm_score() with valid test cases")
    for url, owner, repo in VALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        rm_score = get_rm_score(owner, repo, TOKEN)

        assert type(rm_score) == float
        assert rm_score >= 0.0
        assert rm_score <= 1.0


@pytest.mark.invalid
@pytest.mark.rm
def test_get_rm_score_invalid():
    print("\n\ntesting get_rm_score() with invalid test cases")
    for url, owner, repo in INVALID_TEST_CASES:
        print(f"test case: ({url}, {owner}, {repo})")

        rm_score = get_rm_score(owner, repo, TOKEN)

        assert type(rm_score) == float
        assert rm_score >= 0.0
        assert rm_score <= 1.0