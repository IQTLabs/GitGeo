![GitHub Actions Unit Tests](https://github.com/IQTLabs/GitGeo/workflows/Python%20package/badge.svg)
[![codecov](https://codecov.io/gh/IQTLabs/GitGeo/branch/main/graph/badge.svg?token=W5DVGL0VMN)](https://codecov.io/gh/IQTLabs/GitGeo)
![pylint Score](https://mperlet.github.io/pybadge/badges/7.37.svg)
![Python Versions Supported](https://github.com/IQTLabs/GitGeo/blob/main/badges/python_versions_supported.svg)
![CodeQL](https://github.com/IQTLabs/GitGeo/workflows/CodeQL/badge.svg)
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
BraulioVM | M▒laga & Granada, Spain
dpursehouse | Kawasaki
jgorset | Oslo, Norway
...
```

Advanced usage to increase number of GitHub API calls allowed per hour:

- First, create a [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

```bash
export GITHUB_USERNAME='[github_username]'
```

```bash
export GITHUB_TOKEN='[github_token]'
```

- Second, run one of these commands.

```bash
python main.py --package [package_name]
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
- Add functionality to scan pypi description field for GitHub URLS if GitHub URLs not found
  in typical PyPI package metadata location
- Add scan of top X PyPI packages capability
- Add codacy integration and badge

## Want to contribute?

- Open a PR. We are glad to accept pull requests. We use black and pylint, though we
  are glad to help if you haven't used those tools before.
- Open an issue. Tell us your problem or a functionality you want.
- Want to help build a community related to GitGeo and similar open source software
  ecosystem exploration tools? Please send an email to jmeyers@iqt.org.