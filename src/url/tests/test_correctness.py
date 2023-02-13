import pytest
from url.tests.conftest import *
from url.correctness import *

@pytest.mark.valid
@pytest.mark.correct
def test_get_doc():
    score = get_doc("lodash", "lodash", TOKEN)
    assert(score == 0.20)
    
    score = get_doc("cloudinary", "cloudinary_npm", TOKEN)
    assert(score == 0.20)
    
    score = get_doc("nullivex", "nodist", TOKEN)
    assert(score == 0.20)
 

@pytest.mark.valid
@pytest.mark.correct
def test_get_downloads():
    # Does not have a download count
    score = get_downloads("lodash", "lodash", TOKEN)
    assert(score == 0)
    
    # Does not have a download count
    score = get_downloads("cloudinary", "cloudinary_npm", TOKEN)
    assert(score == 0)
    
    score = get_downloads("nullivex", "nodist", TOKEN)
    assert(score == 0.10)
       

@pytest.mark.valid
@pytest.mark.correct
def test_get_stars():
    score = get_stars("lodash", "lodash", TOKEN)
    assert(score == 0.10)
    
    # Star Count is below score criteria
    score = get_stars("cloudinary", "cloudinary_npm", TOKEN)
    assert(score == 0)
    
    score = get_stars("nullivex", "nodist", TOKEN)
    assert(score == 0.10)


@pytest.mark.valid
@pytest.mark.correct
def test_get_issues():
    score = get_issues("lodash", "lodash", TOKEN)
    assert(score == 0.10)
    
    score = get_issues("cloudinary", "cloudinary_npm", TOKEN)
    assert(score == 0.10)
    
    score = get_issues("nullivex", "nodist", TOKEN)
    assert(score == 0.10)


@pytest.mark.valid
@pytest.mark.correct
def test_get_pr():
    score = get_pr("lodash", "lodash", TOKEN)
    assert(score == 0.10)
    
    score = get_pr("cloudinary", "cloudinary_npm", TOKEN)
    assert(score == 0.10)
    assert(score != 0.0)
    
    score = get_pr("nullivex", "nodist", TOKEN)
    assert(score == 0.0)
    assert(score != 0.10)


@pytest.mark.valid
@pytest.mark.correct
def test_get_tags():
    tag_score = get_tags("https://github.com/jonschlinkert/even")
    assert(tag_score == 0.10)

    tag_score = get_tags("https://github.com/lodash/lodash")
    assert(tag_score == 0.0)