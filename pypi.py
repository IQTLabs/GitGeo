"""PyPI and python package-related functions"""

import json
import sys
import urllib

from bs4 import BeautifulSoup
import requests


def get_top_python_packages(top_N=100):
    """Generate list of most downloaded python packages

    Args:
    TOP_N: the number of most downloaded packages to return

    Returns:
        (list) Names of most downloaded packages
    """
    # JSON file containing top 4000 packages
    # found here: https://hugovk.github.io/top-pypi-packages/
    top_python_pkgs = "top_python_pkg_downloads.json"
    with open(top_python_pkgs, "r") as j:
        contents = json.loads(j.read())

        # store names of top packges
        top_pkgs = []
        cnt = 0
        for pkg in contents["rows"]:
            # only append TOP_N number of packages
            if cnt == top_N:
                break
            top_pkgs.append(pkg["project"])
            cnt += 1

        return top_pkgs


def get_pypi_data(pkg):
    """Return data associated with a python package

    Args:
        pkg: the name of a python package found on PyPI

    Returns:
        dict: data related to a PyPI package
    """
    # Retrieve PyPI package JSON data
    try:
        pkg_url = "https://pypi.org/pypi/" + pkg + "/json"
        response = requests.get(pkg_url)
        pypi_pkg_json = response.json()
    except urllib.error.HTTPError:
        print("ERROR: No such package on PyPI")
        sys.exit(1)  # 1 indicates error

    pypi_data = {}

    pypi_data["github_owner_and_repo"] = get_github_URL_owner_and_repo(pypi_pkg_json)
    pypi_data["pypi_maintainers"] = get_pypi_maintainers(pkg)

    return pypi_data


def get_github_URL_owner_and_repo(pypi_pkg_json):
    """Retrieve owner and repo associated with GitHub URL

    e.g. psf/requests, NOT https://www.github.com/psf/requests

    Args:
        pypi_pkg_json: a json blob of pypi package data

    Returns:

        str: owner and repo name associated with GitHub URL
    """
    github_page = ""
    # Check potential fields for a github link
    potential_github_fields = [pypi_pkg_json["info"]["home_page"]]
    # Add project url fields if url fields present
    if pypi_pkg_json["info"]["project_urls"]:
        for _, url in pypi_pkg_json["info"]["project_urls"].items():
            potential_github_fields.append(url)
    # TODO: Add a search of the text in PyPI for any GitHub mentions

    for field in potential_github_fields:
        # Any field with github in it must be github link
        if "github" in field:
            github_page = field
            break

    # Extract repo owner and repo name only
    github_page_elements = github_page.split("/")[-2:]
    github_owner_and_repo = ("/").join(github_page_elements)

    return github_owner_and_repo


def get_pypi_maintainers(pkg):
    """Extract list of PyPI maintainers, i.e. those with publish rights

    PyPI JSON endpoint does not contain the maintainers' data found in the
    PyPI UI. IMO, this is an oversight. To retrieve PyPI maintainers date,
    use web scraping. There will be a speed penalty, but this feature was
    given a strong priority.

    Args:
        pkg: package name

    Returns:
        list: one or more maintainer PyPI usernames
    """
    # Scrape regular PyPI package site
    url = "https://pypi.org/project/" + pkg
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    elements = soup.findAll("span", {"class": "sidebar-section__user-gravatar-text"})
    # Strip white space from all elements
    maintainers_full_list = [elem.string.strip() for elem in elements]
    # Remove duplicates via set, then sort a list of maintainers
    maintainers_list = sorted(list(set(maintainers_full_list)))

    return maintainers_list
