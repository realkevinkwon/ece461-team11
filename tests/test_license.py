import sys
sys.path.insert(1, '../src/license')
import license

# Arguements to Simplify Testing
git_token = ""
all_licenses_list = []
sample_approved_license_list = ['GNU Lesser General Public License v2.1', 'Apache License 2.0', 'BSD 2-Clause "Simplified" License', 'BSD 3-Clause "New" or "Revised" License', 'Boost Software License 1.0', 'MIT License', 'The Unlicense']
headers = {"Authorization": f"{git_token}"}
all_github_licenses = ['GNU Affero General Public License v3.0', 'Apache License 2.0', 'BSD 2-Clause "Simplified" License', 'BSD 3-Clause "New" or "Revised" License', 'Boost Software License 1.0', 'Creative Commons Zero v1.0 Universal', 'Eclipse Public License 2.0', 'GNU General Public License v2.0', 'GNU General Public License v3.0', 'GNU Lesser General Public License v2.1', 'MIT License', 'Mozilla Public License 2.0', 'The Unlicense']
license_api_url = f"https://api.github.com/licenses"


def test_get_owner_repo():
    owner_repo = license.get_owner_repo("https://github.com/nullivex/nodist.git")
    assert(owner_repo == 'nullivex/nodist')
    # Check to see if it returns both user and repo together
    owner_repo = license.get_owner_repo("https://github.com/cloudinary/cloudinary_npm")
    assert(owner_repo == "cloudinary/cloudinary_npm")
    assert(owner_repo != "cloudinary_npm" and owner_repo != "cloudinary")

def test_npm_to_git():
    url = license.npm_to_git("https://www.npmjs.com/package/express")
    assert(url == "https://github.com/expressjs/express.git")
    assert(url != "https://www.npmjs.com/package/express")
    
    url = license.npm_to_git("https://www.npmjs.com/package/browserify")
    assert(url == "https://github.com/browserify/browserify.git")
    assert(url != "https://www.npmjs.com/package/browserify")
    
    url = license.npm_to_git("https://www.npmjs.com/package/even")
    assert(url == "https://github.com/jonschlinkert/even.git")
    assert(url != "https://www.npmjs.com/package/even")

def test_getLicensesList():
    list_of_licenses = license.getLicensesList(git_token)
    assert(list_of_licenses == sample_approved_license_list)

def test_approved_licenses():
    approved = license.approved_licenses(all_github_licenses, license_api_url, headers)
    assert(approved == sample_approved_license_list)

def test_githubLicense():
    # Sample Approved License List Added to avoid overhead
    name_license = license.githubLicense("cloudinary/cloudinary_npm", git_token, sample_approved_license_list)
    assert(name_license == "MIT License")
    
    name_license = license.githubLicense("PSOPT/psopt", git_token, sample_approved_license_list)
    assert(name_license == "GNU Lesser General Public License v2.1")
    assert(name_license != "MIT License")

    
    name_license = license.githubLicense("nullivex/nodist", git_token, sample_approved_license_list)
    assert(name_license == "MIT License")
    
    name_license = license.githubLicense("lodash/lodash", git_token, sample_approved_license_list)
    assert(name_license == "MIT License")

"""
def test_searchReadme():
    pass

def test_fail_rustScore():
    pass

def test_pass_rustScore():
    pass
"""