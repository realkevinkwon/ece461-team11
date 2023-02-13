import sys
import re
import requests

def npm_to_git(repo):
    url = f"https://registry.npmjs.org/{repo}"
    getGit = requests.get(url)
    if getGit.status_code == 200:
        if "repository" in getGit.json() or "url" in getGit.json():
            gitURL = getGit.json()["repository"]["url"]
            if "github" in gitURL:
                result = re.search(r"/([\w-]+)/([\w-]+)", gitURL.lower())
                git_owner = ""
                if result is not None:
                    git_owner = result[1]
                else: git_owner = "guh"
                return git_owner
    return "guh"

if __name__ == "__main__": # pragma: no cover
    owner = npm_to_git(sys.argv[1])
    print(owner, end="")