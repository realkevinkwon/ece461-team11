import pytest
from ..src.url.responsive_maintainer import *


USERNAME = 'realkevinkwon'
TOKEN = 'token'


@pytest.mark.url
def test_parse_url():
    owner, repo = parse_url(
        url='https://github.com/cloudinary/cloudinary_npm'
    )

    assert owner == 'cloudinary'
    assert repo == 'cloudinary_npm'

    owner, repo = parse_url(
        url='https://github.com/nullivex/nodist'
    )

    assert owner == 'nullivex'
    assert repo == 'nodist'

    owner, repo = parse_url(
        url='https://github.com/lodash/lodash'
    )

    assert owner == 'lodash'
    assert repo == 'lodash'


@pytest.mark.subscores
def test_get_yearly_commits_subscore():
    session = requests.Session()
    session.auth = (USERNAME, TOKEN)

    yearly_commits_subscore = get_yearly_commits_subscore(
        session=session,
        # owner='openai',
        # repo='openai-cookbook'
        # owner='nodejs',
        # repo='node'
        # owner='LAION-AI',
        # repo='Open-Assistant'
        owner='facebook',
        repo='react'
        # owner='audacity',
        # repo='audacity'
    )

    assert type(yearly_commits_subscore) == float
    assert yearly_commits_subscore >= 0.0
    # assert yearly_commits_subscore <= 1.0

    print(yearly_commits_subscore)


@pytest.mark.subscores
def test_get_weekly_adds_and_dels_subscore():
    session = requests.Session()
    session.auth = (USERNAME, TOKEN)

    weekly_adds_and_dels_subscore = get_weekly_adds_and_dels_subscore(
        session=session,
        # owner='openai',
        # repo='openai-cookbook'
        # owner='nodejs',
        # repo='node'
        # owner='LAION-AI',
        # repo='Open-Assistant'
        owner='facebook',
        repo='react'
        # owner='audacity',
        # repo='audacity'
    )

    assert type(weekly_adds_and_dels_subscore) == float
    assert weekly_adds_and_dels_subscore >= 0.0
    # assert weekly_adds_and_dels_subscore <= 1.0

    print(weekly_adds_and_dels_subscore)


@pytest.mark.score
def test_get_responsive_maintainer_score():
    responsive_maintainer_score = get_responsive_maintainer_score(
        username=USERNAME,
        token=TOKEN,
        url='https://github.com/cloudinary/cloudinary_npm'
    )

    assert type(responsive_maintainer_score) == float
    assert responsive_maintainer_score >= 0.0
    assert responsive_maintainer_score <= 1.0

    print(responsive_maintainer_score)