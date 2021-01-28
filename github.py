"""GitHub API-related functionality"""

import json
import os
import re
import urllib.parse

import requests

from geographies_list import ALL_COUNTRIES, STATE_NAMES, STATE_ABBREV

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
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
    )

    committers = []
    if response.ok:
        repo_items = json.loads(response.text or response.content)
        for item in repo_items:
            committers.append(item["login"])

    return committers


def get_country_from_location(location_string):
    """Return country (Hungary, United States, etc) from user location text

    Args:
        location_string: a text containing a city and/or state and/or country

    Return:
        str: a country from the list of full country names from the package
             country_list, or "NONE" if it wasn't a valid location or None was
             provided
    """
    # TODO: do case agnostic check
    # TODO: do we want to have this static list of all cities mapped to countries from
    # https://gist.github.com/fiorix/4592774 or https://datahub.io/core/world-cities ?
    # TODO: Kinga, do you have an intuition about the pro's and con's of having multiple
    # return statements in one function? My spidey sense says to avoid this, but I
    # am open to your more informed judgement and knowledge of software engineering
    # research and practice.

    if location_string == None:
        return "NONE"

    pieces = location_string.split(",")
    end_token = pieces[-1].strip()

    if "Georgia" == end_token:
        if len(pieces) > 1:
            return "United States"
        else:
            return "Georgia"

    if end_token in ALL_COUNTRIES:
        return end_token
    if end_token in STATE_NAMES:
        return "United States"
    if end_token in STATE_ABBREV:
        return "United States"

    return "NONE"


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
        "https://api.github.com/users/" + user,
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
    )

    user_location = ""
    if response.ok:
        user_info = json.loads(response.text or response.content)
        user_location = user_info["location"]

    return user_location
