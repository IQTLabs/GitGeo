![GitHub Actions Unit Tests](https://github.com/IQTLabs/GitGeo/workflows/Python%20package/badge.svg)
[![codecov](https://codecov.io/gh/IQTLabs/GitGeo/branch/main/graph/badge.svg?token=W5DVGL0VMN)](https://codecov.io/gh/IQTLabs/GitGeo)
![pylint Score](https://mperlet.github.io/pybadge/badges/9.97.svg)
![Python Versions Supported](https://github.com/IQTLabs/GitGeo/blob/main/badges/python_versions_supported.svg)
![CodeQL](https://github.com/IQTLabs/GitGeo/workflows/CodeQL/badge.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# GitGeo
Discover the geography of open-source software. Explore the geographic locations of software developers associated with a GitHub repository or a Python (PyPI) package.

## Why use GitGeo?
- Curiosity
- Open source software community managemenet
- IT security compliance
- Research on open source software ecosystem

## Installation

```bash
git clone https://github.com/IQTLabs/GitGeo
cd GitGeo
pip install -r requirements.txt
```

## Usage

(requires internet connection)

```python main.py --package [package_name]```

For example:

```python main.py --package requests```

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

Advanced usage to increase number of GitHub API calls allowed per hour:

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

Run tests:

```bash
pytest
```

## Roadmap

- Add country text extraction capability - e.g. "Virginia, USA" --> "USA"
	- Add country acryonym matching. e.g. USA --> "United States"
	- Assess using geolocation API's
- Add visualization capability
- Add scan of top X PyPI packages capability
- Add readin packages or repos capability
- Add codacy integration and badge
- Add capability of reading through commits and, specifically, (1) determine if GitHub commit rights can be inferred.
- Add capability of predicting location via a model given only timestamp from commit and from commit-related data.
- Investigate capability to determine authenticity of location information
- Investigate possibility of geographic diversity score for a repo or package
- Investigate possibility of linking emails in commits to email breach lists.
- Investigate possibility of determining whether a project is a "hobby" project (outside of working hours) or a "work" project (within working hours)?
- Investigate possibility of using NLP to determine codebase specialties of each contributor. e.g.
  This person is the "auth" person.
- Investigate multi-token capability, i.e. storing multiple tokens to increase API usage per hour.

## Potential Research Questions

- Are there places in the world with unrecognized pockets of software developers?
- What predicts the number of top python packages software developers by country?
	- Total number of coders per country?
	- Total number of python coders per country?
	- GDP per capita per country?

## Known bugs

## Want to contribute?

- Open a PR. We are glad to accept pull requests. We use black and pylint, though we
  are glad to help if you haven't used those tools before.
- Open an issue. Tell us your problem or a functionality you want.
- Want to help build a community related to GitGeo and similar open source software
  ecosystem exploration tools? Please send an email to jmeyers@iqt.org.
