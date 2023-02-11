from urllib.parse import urlparse
from url import license
from url import correctness
from url import bus_factor
import sys
import ndjson
import os
import ctypes
rustLib = ctypes.CDLL("target/debug/rustlib.dll")
netFunc = rustLib.net_score

def main_driver():
    token = os.getenv('GITHUB_TOKEN')
    URLList = []
    URL_FILE = open(sys.argv[1])
    urlLines = URL_FILE.readlines()
    for URL in urlLines:
        # Parse the URL to get to the absolute Webpage name
        url_domain = urlparse(URL).netloc.split('.')
        
        # Gets Github Repo from NPM API
        if("npmjs" in url_domain):
            URL = license.npm_to_git(URL)
    
        # Get Repo Name and Owner    
        owner_repo = license.get_owner_repo(URL)
        
        responsive = 0
        busScore = bus_factor.busFactor(URL,token)
        correct = correctness_func(owner_repo, token, URL)
        rampUp = 0
        licenseScore = license_func(owner_repo, token)
        net_score = netFunc(busScore,correct,responsive,rampUp,licenseScore)#sum(busScore, correct, responsive, rampUp, licenseScore) / 5
        URLList.append({URL:{"TotalScore": net_score, "License": licenseScore, "RampUp": rampUp, "BusFactor": busScore, "ResponsiveMaintainers": responsive, "Correct": correct}})
    with open("output.NDJSON", "w") as out:
        ndjson.dumps(URLList,out)
    out.close()    

def license_func(owner_repo, git_token):
    
    # Get list of possible licenses from Github
    licenseList = license.getLicensesList(git_token)
    
    licenseName = license.githubLicense(owner_repo, git_token, licenseList)

    # Assigns a score according to the license
    scoreLicense = license.rustScore(licenseName, licenseList)
    return scoreLicense
 
def correctness_func(owner_repo, git_token, url):
    
    correcntessList = [
        #correctnessScore.get_Resp_Maintainer(),   # Still needs Resp Maintainer Score
        correctness.get_tags(url),
        correctness.get_downloads(owner_repo, git_token),    
        correctness.get_doc(owner_repo, git_token),
        correctness.get_stars(owner_repo, git_token),
        correctness.get_issues(owner_repo, git_token),
        correctness.get_pr(owner_repo, git_token)]
    
    return sum(correcntessList)
    
if __name__ == "__main__":
    main_driver()