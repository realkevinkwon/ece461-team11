import sys
import re
import requests

def npm_to_git(repo):
    url = f"https://registry.npmjs.org/{repo}"
    getGit = requests.get(url)
    if getGit.status_code == 200:
        gitURL = getGit.json()["repository"]["url"]
        if "github" in gitURL:
            result = re.search(r"/([\w]+)/([\w]+)", gitURL.lower())
            git_owner = ""
            if result is not None:
                git_owner = result[1]
            return git_owner 
        else:
            return "guh"

    else:
        return "guh"

if __name__ == "__main__":
    owner = npm_to_git(sys.argv[1])
    print(owner, end="")