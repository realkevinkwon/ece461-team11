import github as Github
from url import ramp_up
import ctypes
rustLib = ctypes.CDLL("target/debug/rustlib.dll")

def busFactor(URL, token):
    if "npmjs.com" in URL:
        URL = ramp_up.npm_to_git_rep(URL)
    URL = URL.replace("https://github.com/","")
    # URL = "https://github.com/Chise7/ECE461_Team11"
    g = Github(token) #figure out how to provide gittokens :( <- GITTOKEN HERE?
    repo = g.get_repo(URL)
    commits = repo.get_commits()
    authors = []
    for commit in commits:
        if commit.author.name not in authors: authors.append(commit.author.name)
    numOfAuthors = len(authors)
    busFunc = rustLib.bus_score
    return(busFunc(numOfAuthors))

if __name__ == "__main__":
    busFactor()