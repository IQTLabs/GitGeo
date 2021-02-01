"""GitHub API-related functionality"""

import json
import os

import requests

from geographies_list import (
    ALL_COUNTRIES,
    CITY_COUNTRY_DICT,
    STATE_NAMES,
    STATE_ABBREV,
    CODE_COUNTRY_DICT,
)

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
        location_string: a text containing user-supplied location

    Return:
        str: a country
    """
    # TODO: do case agnostic check
    country = "None"
    if location_string is None:
        country = "None"
    else:
        # Loop through different typical separators of city, country, etc.
        for separator in [",", " "]:
            # Check different positions of the token
            for position in [-1, 0]:

                pieces = location_string.split(separator)
                token = pieces[position].strip()

                # todo: these break statements are probably not behaving like
                # jsm expects
                if token in ALL_COUNTRIES:
                    country = token
                    break
                elif token in CITY_COUNTRY_DICT.keys():
                    country = CITY_COUNTRY_DICT[token]
                    break
                elif token in CODE_COUNTRY_DICT.keys():
                    country = CODE_COUNTRY_DICT[token]
                    break
                elif token in STATE_NAMES or token in STATE_ABBREV:
                    country = "United States"

    return country


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
