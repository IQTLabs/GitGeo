"""GitHub API-related functionality"""

import json
import os
import re
import urllib.parse

from country_list import countries_for_language
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


def get_country_from_location(location_string):
    """Return country (Hungary; United States, etc) from a text containing a city and/or state and/or country.
    Args:
        location_string: a text containing a city and/or state and/or country

    Return:
        str: a country from the list of full country names from the package country_list, or "NONE"
        if it wasn't a valid location or None was provided
    """
    # TODO: do case agnostic check
    # TODO: do we want to have this static list of all cities mapped to countries from 
    # https://gist.github.com/fiorix/4592774 or https://datahub.io/core/world-cities ?

    if location_string == None:
        return "NONE"

    all_countries = dict(countries_for_language("en")).values()
    state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", 
        "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", 
        "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", 
        "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", 
        "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", 
        "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", 
        "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

    state_abbrev = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


    query = ""
    pieces = location_string.split(",")

    if "Georgia" == pieces[-1].strip():
        if len(pieces) > 1:
            return "United States"
        else:
            return "Georgia"

    if pieces[-1].strip() in all_countries:
        return pieces[-1].strip()
    if pieces[-1].strip() in state_names:
        return "United States"
    if pieces[-1].strip() in state_abbrev:
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
        "https://api.github.com/users/" + user, auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )

    user_location = ""
    if response.ok:
        user_info = json.loads(response.text or response.content)
        user_location = user_info["location"]

    return user_location
