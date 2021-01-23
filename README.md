# git-geo
Identify geographic location of GitHub committers associated with python packages

## Why use git-geo?
- Curiosity
- IT Security Compliance
- Research on open source software ecosystem

Usage (requires internet connection):

```python main.py --package [package_name]```

Advanced usage to increase number of GitHub API calls allowed per hour:

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

- Identify those contributors with PyPI publish rights with an asterisk
