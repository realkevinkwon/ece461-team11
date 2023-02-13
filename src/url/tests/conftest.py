import os

result = os.getenv('GITHUB_TOKEN')
TOKEN = result if result is not None else ""
VALID_TEST_CASES = [
    ("https://www.npmjs.com/package/even", "jonschlinkert", "even"),
    ("https://github.com/jonschlinkert/even", "jonschlinkert", "even"),
    ("https://github.com/SonarSource/chocolatey-packages", "SonarSource", "chocolatey-packages"),
    ("https://github.com/PSOPT/psopt", "PSOPT", "psopt"),
    ("https://github.com/nullivex/nodist", "nullivex", "nodist"),
    ("https://www.npmjs.com/package/express", "expressjs", "express"),
    ("https://www.npmjs.com/package/browserify", "browserify", "browserify"),
    ("https://github.com/cloudinary/cloudinary_npm ", "cloudinary", "cloudinary_npm"),
    ("https://github.com/lodash/lodash", "lodash", "lodash"),
    ("https://github.com/PC192/ChubbyChecker", "PC192", "ChubbyChecker"), # Increase code coverage (missing items in valid repo)
    ("https://github.com/apache/airflow", "apache", "airflow") # Increase code coverage (too many items in valid repo)
]
INVALID_TEST_CASES = [
    ("https://www.github.com/lodash/lodash", "unga", "lodash"), # incorrect owner
    ("https://www.github.com/lodash/lodash", "lodash", "bunga"), # incorrect repo
    ("https://www.github.com/lodash/lodash", "unga", "bunga"), # incorrect owner and repo
]

# Testcases = [('Chise7', 'ECE461_Team11'),('words', 'double-metaphone'),('jonschlinkert', 'even'), ('apache', 'airflow'),('PSOPT', 'psopt'),('nullivex','nodist'),('cloudinary','cloudinary_npm'), ('PC192','ChubbyChecker')]