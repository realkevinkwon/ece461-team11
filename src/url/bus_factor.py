import sys
from github import Github

def get_bus_factor_score(owner, repo, token):
    repo_dir = f"{owner}/{repo}"
    g = Github(token)
    # try: git_repo = g.get_repo(repo_dir)
    # except: return -1.0
    git_repo = g.get_repo(repo_dir)
    commits = git_repo.get_commits()
    authors = []
    for commit in commits:
        if commit is not None and commit.author is not None and commit.author.name not in authors: authors.append(commit.author.name)
        if len(authors) == 100: return 1.0
    num_of_authors = len(authors)
    if num_of_authors >= 5 and num_of_authors < 100: return 0.75
    elif num_of_authors >= 100: return 1.0
    else: return 0.0

if __name__ == "__main__":
    bus_factor_score = get_bus_factor_score(sys.argv[1], sys.argv[2], sys.argv[3])
    print(bus_factor_score, end="")