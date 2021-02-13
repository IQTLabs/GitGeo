![GitHub Actions Unit Tests](https://github.com/IQTLabs/GitGeo/workflows/Python%20package/badge.svg)
[![codecov](https://codecov.io/gh/IQTLabs/GitGeo/branch/main/graph/badge.svg?token=W5DVGL0VMN)](https://codecov.io/gh/IQTLabs/GitGeo)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5eb7fb4f74b04e83b0ce967a75b460f5)](https://app.codacy.com/gh/IQTLabs/GitGeo?utm_source=github.com&utm_medium=referral&utm_content=IQTLabs/GitGeo&utm_campaign=Badge_Grade)
![pylint Score](https://mperlet.github.io/pybadge/badges/10.svg)
![Python Versions Supported](https://github.com/IQTLabs/GitGeo/blob/main/badges/python_versions_supported.svg)
![CodeQL](https://github.com/IQTLabs/GitGeo/workflows/CodeQL/badge.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# GitGeo
Discover the geography of open-source software. Explore the geographic locations of software developers associated with a GitHub repository or a Python (PyPI) package.

## Why use GitGeo?
-  Curiosity
-  Open source software community management
-  Research on open source software ecosystem
-  IT security compliance

## Installation

```bash
git clone https://github.com/IQTLabs/GitGeo
cd GitGeo
pip install -r requirements.txt
```

## Usage

(requires internet connection)

```python main.py --package [package_name]```
```python main.py --repo [github_repo_url]```

For example:

```>>> python main.py --package requests```

```
-----------------
PACKAGE: requests
-----------------
CONTRIBUTOR, LOCATION
* indicates PyPI maintainer
---------------------
kennethreitz42 | Virginia, USA
Lukasa * | London, England
sigmavirus24 | Madison, WI
nateprewitt * | None
slingamn | None
BraulioVM | Malaga & Granada, Spain
dpursehouse | Kawasaki
jgorset | Oslo, Norway
...
```

Or:

```>>> python main.py --repo www.github.com/psf/requests```

```
-----------------
GITHUB REPO: psf/requests
-----------------
CONTRIBUTOR, LOCATION
---------------------
kennethreitz42 | Virginia, USA | United States
Lukasa | London, England | United Kingdom
sigmavirus24 | Madison, WI | United States
nateprewitt | None | None
...
```

There are other command line options too:

Add ```--summary``` to get the results summarized by country. e.g.

```>>> python main.py --package requests --summary```

```
-----------------
PACKAGE: requests
GITHUB REPO: psf/requests
-----------------
COUNTRY | # OF CONTRIBUTORS
---------------------------
United States 37
None 23
United Kingdom 4
Canada 4
Germany 4
Switzerland 4
Spain 2
Russia 2
...
```

Add ```--map``` when using the ```--repo``` option to create an html map
saved in the results folder. See image above for static example. Real map
includes zooming and tooltip capability.

Add ```--ouput_csv``` to output csv of results to results folder.

To create a csv of contributors from many repositories, enter repositories
on separate lines in the repos.txt file. Then use the ```--multirepo``` flag.


### Advanced usage to increase number of GitHub API calls allowed per hour:

- First, create a [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

- Second, run these commands in the command line:
```bash
export GITHUB_USERNAME='[github_username]'
export GITHUB_TOKEN='[github_token]'
```

- Third, run one of these commands.

```bash
python main.py --package [python_package_name]
```

```bash
python main.py --repo [github_repo_name]
```

### Run tests:

```bash
pytest
```

## Roadmap

-  Investigate capability of predicting location via a model given only timestamp from commit and commit-related data. (Kinga)
-  Common developer feature: Add capability to count number of repos associated with each contributor given results of multi-repo scan. (JSM)
-  Add capability for accessing top 500 contributors via GitHub API.
-  Investigate GitHub API for examining merges and who has merge rights.
-  Add capability of reading through commits and, specifically, (1) determine if GitHub commit rights can be inferred.
-  Investigate capability to determine authenticity of location information
-  Investigate possibility of geographic diversity score for a repo or package
-  Investigate possibility of linking emails in commits to email breach lists.
-  Investigate possibility of determining whether a project is a "hobby" project (outside of working hours) or a "work" project (within working hours)?
-  Investigate possibility of using NLP to determine codebase specialties of each contributor. e.g.
  This person is the "auth" person.
-  Investigate over time commit analysis visualization
-  Investigate multi-token capability, i.e. storing multiple tokens to increase API usage per hour.
-  Add dump multirepo results (or similar aggregate scan) to s3 capability
-  Investigate diff to tweet capability. Reveal major contributor changes in critical projects to an open feed.
-  Investigate switching ownership data. Would be interesting to alert users to this.
-  Investigate by user capability. Determine all repo's a user has contributed to. Do a quick git blame for a user.

## Rainy Day Options

-  Access commercial API's to enrich data on GitHub usernames or, if included in GitHub profile, email handles, etc.(MK)

## Potential Research Questions

- Are there places in the world with unrecognized pockets of software developers?
- Where are maintainers associated with the most critical python packages?
	- Who are the maintainers that are associated with multiple critical python packages?
	- What about contribution-related weighting?
- Where are the maintainers associated with the top GitHub packages by stars? Top data science packages? Etc?
	- Then do sub-analysis that asks on what repos or types of repos developers of a given country are most active
- What predicts the number of top python packages software developers by country?
	- Total number of coders per country?
	- Total number of python coders per country?
	- GDP per capita per country?
- Is it possible to "verify" user information?

## Known bugs

## Want to contribute?

- Open a PR. We are glad to accept pull requests. We use black and pylint, though we
  are glad to help if you haven't used those tools before.
- Open an issue. Tell us your problem or a functionality you want.
- Want to help build a community related to GitGeo and similar open source software
  ecosystem exploration tools? Please send an email to jmeyers@iqt.org.
