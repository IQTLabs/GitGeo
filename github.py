"""GitHub API-related functionality"""

#TODO: consider functionality that maps the free text of location
# to one country. Consider using geopy. Or geograpy.

import json
import os

import requests

# access secret token for GitHub API to increase rate limit
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


# Identify up to top 100 committers associated with a Github repo
def get_contributors(repo):
    """Generate list of up to top 100 contributors on package

    Args:
        repo: a github repo url

    Return:
        list: committer handles
    """
    # TODO: Consider looping thru pages 1-5. The github contributors API will return up
    # to 500 contributors
    response = requests.get(
        "https://api.github.com/repos/" + repo + "/contributors?page=1&per_page=100",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN),
    )

    committers = []
    if response.ok:
        repo_items = json.loads(response.text or response.content)
        for item in repo_items:
            committers.append(item["login"])

    return committers


def get_contributor_location(user):
    """Return geographic location, if present on github page, of user

    Args:
        user: the GitHub user name

    Return:
        str: a geographic location
    """
    # TODO: What to do if location is not present? What to do
    # if location is not listed in profile?
    # https://stackoverflow.com/questions/26983017/detect-ip-address-of-github-commit
    # https://gist.github.com/paulmillr/2657075
    response = requests.get(
        "https://api.github.com/users/" + user, auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )

    user_location = ""
    if response.ok:
        user_info = json.loads(response.text or response.content)
        user_location = user_info["location"]

    return user_location
