"""GitHub API-related functionality"""

import json
import os

import requests

from geographies_list import ALL_COUNTRIES, CITY_COUNTRY_DICT, STATE_NAMES, STATE_ABBREV

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
    # TODO: Kinga, do you have an intuition about the pro's and con's of having multiple
    # return statements in one function? My spidey sense says to avoid this, but I
    # am open to your more informed judgement and knowledge of software engineering
    # research and practice.

    if location_string is None:
        return "None"

    # Loop through different typical separators of city, country, etc.
    for separator in [",", " "]:
        # Check different positions of the token
        for position in [-1, 0]:

            pieces = location_string.split(separator)
            token = pieces[position].strip()

            if token == "Georgia":
                if len(pieces) > 1:
                    return "United States"
                return "Georgia"

            if token in ALL_COUNTRIES:
                return token
            if token in CITY_COUNTRY_DICT.keys():
                return CITY_COUNTRY_DICT[token]
            if token in STATE_NAMES:
                return "United States"
            if token in STATE_ABBREV:
                return "United States"

    # If no match is found, also return None as string
    return "None"


def get_contributor_location(user):
    """Return geographic location, if present on github page, of user

    Args:
        user: the GitHub user name

    Return:
        str: a geographic location
    """
    # TODO: What to do if location is not listed in profile? Kinga has
    # some predictive analytics ideas.
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
