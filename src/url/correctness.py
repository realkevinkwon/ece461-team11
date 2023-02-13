import sys
import requests
import git
import os, shutil


def get_downloads(owner, repo, token):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"token {token}"}
    downloads_request = requests.get(api_url, headers=headers)
    releases = downloads_request.json()
    downloads_score = 0.0
    release_count = len(releases)
    if(downloads_request.status_code == 200):
        try: # Try to see if it exists
            if("download_count" in releases[0]["assets"][0]): 
                for version in range(0, release_count - 1):
                    downloads_score += releases[version]["assets"][0]["download_count"]
                if(downloads_score > 1000):
                    downloads_score = 0.10
        except:
            downloads_score = 0.0

    return downloads_score

def get_doc(owner, repo, token):
    api_Url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Authorization": f"token {token}"}
    get_readme = requests.get(api_Url, headers=headers)
    doc_score = 0.0
    
    if(get_readme.status_code == 200): doc_score = 0.20

    return doc_score

def get_stars(owner, repo, token):
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {token}"}
    star_request = requests.get(api_url, headers=headers)
    
    stars_score = 0.0
    if(star_request.status_code == 200):
        star_count = int(star_request.json()["stargazers_count"])
        
        if(star_count > 1000): stars_score = 0.10

    return stars_score

def get_tags(url):
    path = "Repo-Analysis"
    if(os.path.isdir(path)):
        shutil.rmtree(path)
        
    repository = git.Repo.clone_from(url, path)
        
    tag_list = []
    tag_not_committed = []
    
    for tag in repository.tags:
        tag_list.append(tag.name)
        if tag.commit not in repository.iter_commits():
            tag_not_committed.append(tag.name)
    
    tags_score = 0.0
    if(len(tag_list) != 0):
        #If more than 95% of Commits are Tagged, get full score
        if((len(tag_list) - len(tag_not_committed)) / len(tag_list) > 0.95):
            tags_score = 0.10
    else: tags_score = 0.10
    return tags_score

def get_issues(owner, repo, token):
    # Base API Call for Total Issues Open and Closed
    api_url_open = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}%20is:issue%20is:open&per_page=1"
    api_url_closed = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}%20is:issue%20is:closed&per_page=1"
    headers = {"Authorization": f"token {token}"}
    
    # Get both Open and Closed Issues Count
    open_issues_request = requests.get(api_url_open, headers=headers)
    closed_issues_request = requests.get(api_url_closed, headers=headers)
    
    issues_score = 0.0
    if(closed_issues_request.status_code == 200 and open_issues_request.status_code == 200):
        total_count = int(open_issues_request.json()["total_count"]) + int(closed_issues_request.json()["total_count"])
        if(total_count > 100): issues_score = 0.10
    
    return issues_score

def get_pr(owner, repo, token):
    # Base API Call for Total Pull Requests Open and Closed
    api_url_open = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}%20is:pr%20is:open&per_page=1"
    api_url_closed = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}%20is:pr%20is:closed&per_page=1"
    headers = {"Authorization": f"token {token}"}
    
    # Get both Open and Closed Issues Count
    open_pr_request = requests.get(api_url_open, headers=headers)
    closed_pr_request = requests.get(api_url_closed, headers=headers)
    
    pr_score = 0.0
    # More than 100 Pull Requests Made (Open and Closed)
    if(open_pr_request.status_code == 200 and closed_pr_request.status_code == 200):
        total_count = int(open_pr_request.json()["total_count"]) + int(closed_pr_request.json()["total_count"])
        if(total_count > 100): pr_score = 0.10
    
    return pr_score

def correctness_func(owner, repo, token, responsive_maintainer_score):
    url = f"https://github.com/{owner}/{repo}"

    total_score = \
        1.0 * get_tags(url) + \
        1.0 * get_downloads(owner, repo, token) + \
        1.0 * get_doc(owner, repo, token) + \
        1.0 * get_stars(owner, repo, token) + \
        1.0 * get_issues(owner, repo, token) + \
        1.0 * get_pr(owner, repo, token)+ \
        0.3 * responsive_maintainer_score

    return round(total_score, 2)

if __name__ == "__main__":
    correctness_score = correctness_func(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]))
    print(correctness_score, end="")