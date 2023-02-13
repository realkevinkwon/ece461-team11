import sys
import requests
import base64

# Request to get Github Repo License
def github_license(owner, repo, token, license_list):
    api_Url = f"https://api.github.com/repos/{owner}/{repo}/license"
    headers = {"Authorization": f"token {token}"}
    get_license = requests.get(api_Url, headers=headers)
    # Checks if the API call was successful for the License File, else looks through README
    if(get_license.status_code != 200):
        readmeLicense = search_readme(api_Url, headers, token)
        licenseName = "License Error"
        if(readmeLicense != "No License"):
            licenseName = readmeLicense
        return licenseName
    else:
        licenseName = get_license.json()["license"]["name"]
        # Second way of checking for license if there was a Null Name for License
        if(licenseName not in license_list):
            readmeLicense = search_readme(api_Url, headers, token)
            if(readmeLicense != "No License"): licenseName = readmeLicense
        return licenseName
    
# Gets Github lists of Approved Licenses with LGPL v2.1
def get_license_list(git_token):
    licenseNames = []
    licenses_url = f"https://api.github.com/licenses"
    headers = {"Authorization": f"token {git_token}"}
    licenseList = requests.get(licenses_url, headers=headers)
    if(licenseList.status_code == 200):
        licenseList = licenseList.json()
        licenseNames = approved_licenses(licenseList,licenses_url, headers)
        return licenseNames
    
    else: return "API request Error getLicensesList"

def approved_licenses(license_list, api_url, headers):
    new_list = ["GNU Lesser General Public License v2.1"]  # Original License to Account
    copyleft = []
    for license in license_list:
        url = api_url + "/" + license["key"]
        license_list = requests.get(url, headers=headers)
        if(license_list.status_code == 200):
            license_list = license_list.json()
            description = license_list['description']
            if("permissive" in description):
                new_list.append(license["name"])
            elif("no conditions" in description):
                new_list.append(license["name"])
            if("GNU Lesser General Public License v2.1" or "LGPL v2.1" in license_list['body']):
                copyleft.append(license["name"])
        #else:
            #print("API Error")
    return new_list

# Searches for any License mentioned in the README
def search_readme(url, headers, git_token):
    url = url.rsplit("/", 1)[0] + "/readme"
    getReadme = requests.get(url, headers=headers)
    
    if(getReadme.status_code != 200): return "No License, API Failed"
    
    else:
        readmeContent = getReadme.json()["content"].encode("utf-8")
        readmeContent = base64.b64decode(readmeContent)
        readmeContent = str(readmeContent).lower()
        licenseList = get_license_list(git_token)
        licenseList = [i.lower() for i in licenseList]

        for gitLicense in licenseList:
            if gitLicense in readmeContent: return gitLicense
        return "No License"   

def license_score(license_name, license_list):
    if license_name in license_list: return 1.0
    else: return 0.0

def license_func(owner, repo, token):
    license_list = get_license_list(token)
    
    license_name = github_license(owner, repo, token, license_list).lower()

    license_list = ", ".join(license_list).lower()    
    return license_score(license_name, license_list)

if __name__ == "__main__":
    license_score = license_func(sys.argv[1], sys.argv[2], sys.argv[3])
    print(license_score, end="")