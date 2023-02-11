import requests
import ctypes
from git import Repo
import os
import stat
import shutil

def get_downloads(owner_repo, git_token):
    api_Url = f"https://api.github.com/repos/{owner_repo}/releases"
    headers = {"Authorization": f"{git_token}"}
    downloads_request = requests.get(api_Url, headers=headers)
    releases = downloads_request.json()
    downloads_score = 0
    release_count = len(releases)
    if(downloads_request.status_code == 200):
        try: # Try to see if it exists
            if("download_count" in releases[0]["assets"][0]): 
                for version in range(0, release_count - 1):
                    downloads_score += int(releases[version]["assets"][0]["download_count"])
                if(downloads_score > 1000):
                    downloads_score = 0.10
                else:
                    downloads_score = 0
        except:
            downloads_score = 0

    else:
        downloads_score = 0

    return downloads_score

def get_doc(owner_repo, git_token):
    api_Url = f"https://api.github.com/repos/{owner_repo}/readme"
    headers = {"Authorization": f"{git_token}"}
    get_readme = requests.get(api_Url, headers=headers)
    if(get_readme.status_code == 200):
        doc_score = 0.20
    else:
        doc_score = 0

    return doc_score

def get_stars(owner_repo, git_token):
    api_Url = f"https://api.github.com/repos/{owner_repo}"
    headers = {"Authorization": f"{git_token}"}
    star_request = requests.get(api_Url, headers=headers)
    
    if(star_request.status_code == 200):
        star_count = int(star_request.json()["stargazers_count"])
        if(star_count > 1000):
            stars_score = 0.10
        else:
            stars_score = 0
    else:
        stars_score = 0

    return stars_score

# https://stackoverflow.com/questions/1889597/deleting-read-only-directory-in-python/1889686#1889686
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
    return 0

def get_tags(url):
    path = "URL_Fields/LR-Test"
    if(os.path.isdir(path)):
        shutil.rmtree(path, onerror=remove_readonly)
    repository = Repo.clone_from(url, path)
        
    tag_list = []
    tag_not_committed = []
    
    for tag in repository.tags:
        tag_list.append(tag.name)
        if tag.commit not in repository.iter_commits():
            tag_not_committed.append(tag.name)
    
    #If more than 95% of Commits are Tagged, get full score
    if((len(tag_list) - len(tag_not_committed)) / len(tag_list) > 0.95):
        tags_score = 0.10
    else:
        tags_score = 0

    return tags_score



def get_issues(owner_repo, git_token):
    # Base API Call for Total Issues Open and Closed
    api_Url_open = f"https://api.github.com/search/issues?q=repo:{owner_repo}%20is:issue%20is:open&per_page=1"
    api_Url_closed = f"https://api.github.com/search/issues?q=repo:{owner_repo}%20is:issue%20is:closed&per_page=1"
    headers = {"Authorization": f"{git_token}"}
    
    # Get both Open and Closed Issues Count
    open_issues_request = requests.get(api_Url_open, headers=headers)
    closed_issues_request = requests.get(api_Url_closed, headers=headers)
    
    if(closed_issues_request.status_code == 200 and open_issues_request.status_code == 200):
        total_count = int(open_issues_request.json()["total_count"]) + int(closed_issues_request.json()["total_count"])
        if(total_count > 100):
            issues_score = 0.10
        else:
            issues_score = 0
    else:
        issues_score = 0
    
    return issues_score

def get_pr(owner_repo, git_token):
    # Base API Call for Total Pull Requests Open and Closed
    api_Url_open = f"https://api.github.com/search/issues?q=repo:{owner_repo}%20is:pr%20is:open&per_page=1"
    api_Url_closed = f"https://api.github.com/search/issues?q=repo:{owner_repo}%20is:pr%20is:closed&per_page=1"
    headers = {"Authorization": f"{git_token}"}
    
    # Get both Open and Closed Issues Count
    open_pr_request = requests.get(api_Url_open, headers=headers)
    closed_pr_request = requests.get(api_Url_closed, headers=headers)
    
    if(open_pr_request.status_code == 200 and closed_pr_request.status_code == 200):
        total_count = int(open_pr_request.json()["total_count"]) + int(closed_pr_request.json()["total_count"])
        if(total_count > 50):
            pr_score = 0.10
        else:
            pr_score = 0
    else:
        pr_score = 0
    
    return pr_score

def get_Resp_Maintainer(rm_score):  # This code can maybe be done in Rust
    rust_lib = ctypes.CDLL('target/debug/rustlib.dll')
    maintainer_score = rm_score # This will be passed as an arguement depending on the Resp Maintainer Code
    resp_maint_score = ctypes.c_int(int(rm_score * 10))
    rm_score = rust_lib.get_rm_score(resp_maint_score)/ 100
    return rm_score