# git-geo
Identify geographic location of GitHub committers associated with python packages

## Why use git-geo?
- Curiosity
- Open source software community managemenet
- IT security compliance
- Research on open source software ecosystem

Usage (requires internet connection):

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

```bash
python main.py --package [package_name]
```

Run tests:

```bash
pytest
```

## Roadmap

- Add capability to specify a github repo directly, not just python package
- Add country text extraction capability - e.g. "Virginia, USA" --> "USA"
- Add scan of top X PyPI packages capability
