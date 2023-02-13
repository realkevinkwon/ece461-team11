import sys
#import requests
from github import Github

def get_ramp_up_score(owner, repo, token):
    g = Github(token)
    try: git_repo = g.get_repo(f"{owner}/{repo}")
    except: return -1.0

    folder_count, folder_score = 0, 0.75
    readme_score = (1 - folder_score)
    has_readme = False

    # Loop through root contents to check for folders
    root_dir = git_repo.get_contents("")
    for objects in root_dir:
        if objects.type == "dir":
            folder_count += 1
        if "README" in objects.name or "readme" in objects.name:
            #print("README Found")
            has_readme = True

    # Scoring from overall metrics
    if folder_count <= 7: folder_score *= 1
    elif folder_count < 10: folder_score *= 0.5
    elif folder_count >= 15: folder_score *= 0

    if not has_readme: readme_score = 0

    return float(folder_score + readme_score)

if __name__ == '__main__': # pragma: no cover
    ramp_up_score = get_ramp_up_score(sys.argv[1], sys.argv[2], sys.argv[3])
    print(ramp_up_score, end="")