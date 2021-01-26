"""GitHub API-related functionality"""

# TODO: consider functionality that maps the free text of location
# to one country. Consider using geopy. Or geograpy.

import json
import os

import requests
from country_list import countries_for_language
import urllib.parse
import re

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
        user: a text containing a city and/or state and/or country

    Return:
        str: a country from the list of full country names from the package country_list, or "NONE" 
        if it wasn't a valid location or None was provided
    """
    # TODO: do case agnostic check

    if location_string == None:
        return "NONE"

    all_countries = dict(countries_for_language('en')).values()
    query = ""
    pieces = location_string.split(" ")

    # because the city/state could also be a country, and a country is also listed, try matching from right-to-left 
    pieces.reverse() 

    for p in pieces: 
        p = p.strip()
        if p in all_countries:
            return p
        query = urllib.parse.quote(p) + "+" + query # order matters for google search apparently

    # use regex to mine the results of a google query for the country
    regex_html = "(<span><h3 class.+><div class=.+>)([A-Za-z ]+)(</div></h3></span><span><div class=.+>Country in.+</div></span>)"
    url = "https://www.google.com/search?q=what+%22country%22+is+" + query + "+in"
    google_search = str(requests.get(url, allow_redirects=True).content)
    country_search = re.search(regex_html, google_search)
    if country_search == None:
        return "NONE"
    return country_search.group(2)


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

    return get_country_from_location(user_location)
