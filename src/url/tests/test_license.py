import pytest
from url.tests.conftest import *
from url.license import *

sample_approved_license_list = ['GNU Lesser General Public License v2.1', 'Apache License 2.0', 'BSD 2-Clause "Simplified" License', 'BSD 3-Clause "New" or "Revised" License', 'Boost Software License 1.0', 'MIT License', 'The Unlicense']
headers = {"Authorization": f"token {TOKEN}"}
all_github_licenses = ['GNU Affero General Public License v3.0', 'Apache License 2.0', 'BSD 2-Clause "Simplified" License', 'BSD 3-Clause "New" or "Revised" License', 'Boost Software License 1.0', 'Creative Commons Zero v1.0 Universal', 'Eclipse Public License 2.0', 'GNU General Public License v2.0', 'GNU General Public License v3.0', 'GNU Lesser General Public License v2.1', 'MIT License', 'Mozilla Public License 2.0', 'The Unlicense']
license_api_url = f"https://api.github.com/licenses"

# This tests get_license_list and approved_licenses
@pytest.mark.valid
@pytest.mark.license
def test_get_license_list():
    list_of_licenses = get_license_list(TOKEN)
    assert(list_of_licenses == sample_approved_license_list)

@pytest.mark.valid
@pytest.mark.license
def test_license_score():
    license_name = "MIT License" 
    score = license_score(license_name, sample_approved_license_list)
    assert(score == 1)
    assert(score != 0)

    license_name = 'BSD 2-Clause "Simplified" License'
    score = license_score(license_name, sample_approved_license_list)
    assert(score == 1)
    assert(score != 0)

    license_name = 'GNU Affero General Public License v3.0'
    score = license_score(license_name, sample_approved_license_list)
    assert(score == 0)
    assert(score != 1)

@pytest.mark.valid
@pytest.mark.license
def test_github_license():
    # Sample Approved License List Added to avoid overhead
    name_license = github_license("cloudinary", "cloudinary_npm", TOKEN, sample_approved_license_list)
    assert(name_license == "MIT License" or name_license == "mit license")
    
    name_license = github_license("PSOPT", "psopt", TOKEN, sample_approved_license_list)
    assert(name_license == "GNU Lesser General Public License v2.1" or name_license == "gnu lesser general public license v2.1")
    assert(name_license != "MIT License" and name_license != "mit license")
    
    name_license = github_license("nullivex", "nodist", TOKEN, sample_approved_license_list)
    assert(name_license == "MIT License" or name_license == "mit license")
    
    name_license = github_license("apache", "airflow", TOKEN, sample_approved_license_list)
    assert(name_license == "Apache License 2.0" or name_license == "apache license 2.0")
    assert(name_license != "MIT License" and name_license != "mit license")

@pytest.mark.valid
@pytest.mark.license
def test_search_readme():
    api_Url = f"https://api.github.com/repos/jonschlinkert/even/license"
    name = search_readme(api_Url, headers, TOKEN)
    assert(name == "mit license")
    
    # This Repo doesn't have the License in it's readme
    api_Url = f"https://api.github.com/repos/apache/airflow/license"
    name = search_readme(api_Url, headers, TOKEN)
    assert(name != "apache license 2.0")
    assert(name == "No License")