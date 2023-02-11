import sys
import requests
from enum import Enum

GITHUB_API_URL = 'https://api.github.com'

class Source(Enum):
    NONE = 'none'
    GITHUB = 'github.com'
    NPM = 'npmjs.com'


# def parse_url(url: str) -> tuple[str, str]:
#     pattern = r'\S*('
#     pattern += Source.GITHUB.value
#     pattern += '|' + Source.NPM.value
#     # pattern += '|' + Source.<source_name>.value   # Add new source here
#     pattern += ')/([a-zA-Z0-9-]+)/([a-zA-Z0-9-_.]+)'

#     # Group 1: source name (including domain),
#     # Group 2: account name
#     # Group 3: repository name
#     result = re.match(pattern, url.lower())

#     owner = ''
#     repo = ''

#     if result is not None and result.lastindex == 3:
#         if result[1] == Source.GITHUB.value:
#             owner = result[2]
#             repo = result[3]
#         elif result[1] == Source.NPM.value:
#             owner = result[2]
#             repo = result[3]

#     return owner, repo


def get_yearly_commits_subscore(session: requests.Session, owner: str, repo: str) -> float:
    while True:
        response = session.get(
            url=GITHUB_API_URL+f'/repos/{owner}/{repo}/stats/commit_activity',
            # headers={
            #     'If-None-Match': 'cea248d061577674615529d3713a77b7c2b5ef361ee9406088b54584da93fdfe'
            # }
        )

        if len(response.json()) > 0:
            break

    if response.status_code != 200 and response.status_code != 202 and response.status_code != 204:
        return 0.0

    yearly_commits = 0
    for item in response.json():
        yearly_commits += item['total']

    if yearly_commits > 1000:
        return 1.0
    elif yearly_commits > 500:
        return 0.75
    elif yearly_commits > 100:
        return 0.5
    elif yearly_commits > 10:
        return 0.25
    else:
        return 0.0


def get_weekly_adds_and_dels_subscore(session: requests.Session, owner: str, repo: str) -> float:
    while True:
        response = session.get(
            url=GITHUB_API_URL+f'/repos/{owner}/{repo}/stats/code_frequency',
            # headers={
            #     'If-None-Match': 'cea248d061577674615529d3713a77b7c2b5ef361ee9406088b54584da93fdfe'
            # }
        )

        if len(response.json()) > 0:
            break

    if response.status_code != 200 and response.status_code != 202 and response.status_code != 204:
        return 0.0

    weekly_additions = 0
    weekly_deletions = 0
    for item in response.json():
        weekly_additions += item[1]
        weekly_deletions += item[2]

    weekly_adds_and_dels = float(weekly_additions - weekly_deletions)
    if weekly_adds_and_dels > 10000000:
        return 1.0
    elif weekly_adds_and_dels > 1000000:
        return 0.75
    elif weekly_adds_and_dels > 100000:
        return 0.5
    elif weekly_adds_and_dels > 10000:
        return 0.25
    else:
        return 0.0


def get_responsive_maintainer_score(owner: str, repo: str, token: str) -> float:
    # owner, repo = parse_url(url)

    session = requests.Session()
    # session.auth = (token)

    yearly_commits_subscore = get_yearly_commits_subscore(session, owner, repo)
    weekly_adds_and_dels_subscore = get_weekly_adds_and_dels_subscore(session, owner, repo)

    responsive_maintainer_score = \
        0.75 * yearly_commits_subscore + \
        0.25 * weekly_adds_and_dels_subscore

    return responsive_maintainer_score

if __name__ == "__main__":
    # responsive_maintainer_score = 0.64
    responsive_maintainer_score = get_responsive_maintainer_score(sys.argv[1], sys.argv[2], sys.argv[3])
    print(responsive_maintainer_score, end="")