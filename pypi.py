"""PyPI and python package-related functions"""

import json
import sys
import urllib

from bs4 import BeautifulSoup
import requests


def get_top_python_packages(top_n=100):
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
            if cnt == top_n:
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

    pypi_data["github_owner_and_repo"] = get_github_url_owner_and_repo(pypi_pkg_json)
    pypi_data["pypi_maintainers"] = get_pypi_maintainers(pkg)

    return pypi_data


def get_github_url_owner_and_repo(pypi_pkg_json):
    """Retrieve owner and repo associated with GitHub URL

    Search for potential GitHub URLS and then return
    in proper format. e.g. psf/requests,
    NOT https://www.github.com/psf/requests

    Args:
        pypi_pkg_json: a json blob of pypi package data

    Returns:

        str: owner and repo name associated with GitHub URL
    """
    github_page = ""
    potential_github_fields = []

    # check home page url
    if "github.com" in pypi_pkg_json["info"]["home_page"]:
        potential_github_fields.append(pypi_pkg_json["info"]["home_page"])

    # check project url fields if url fields present
    if pypi_pkg_json["info"]["project_urls"]:
        for _, url in pypi_pkg_json["info"]["project_urls"].items():
            if "github.com" in url:
                potential_github_fields.append(url)

    # check PyPI description text for any GitHub mentions, if url
    # fields not present
    description = pypi_pkg_json["info"]["description"]
    if potential_github_fields == [] and description:
        for token in description.split():
            if "github.com" in token:
                potential_github_fields.append(token)

    for field in potential_github_fields:
        # Any field with github in it must be github link
        if "github" in field:
            github_page = field
            break

    # Extract repo owner and repo name only
    github_owner_and_repo = extract_github_owner_and_repo(github_page)

    return github_owner_and_repo


def extract_github_owner_and_repo(github_page):
    """Extract only owner and repo name from GitHub page

    https://www.github.com/psf/requests -> psf/requests

    Args:
        github_page - a reference, e.g. a URL, to a GitHub repo

    Returns:
        str: owner and repo joined by a '/'
    """
    if github_page == "":
        return ""

    # remove slash if last character
    if github_page[-1] == "/":
        github_page = github_page[:-1]

    github_page_elements = github_page.split("/")

    # deal with "pandas"-type bug where url includes issues at the end
    # bug: https://github.com/pandas-dev/pandas/issues -> pandas/issues
    # correct: https://github.com/pandas-dev/pandas/issues -> pandas-dev/pandas
    if github_page_elements[-1] == "issues":
        github_page_elements.pop(-1)

    # join last two element with a slash
    github_owner_and_repo = ("/").join(github_page_elements[-2:])

    return github_owner_and_repo


def get_pypi_maintainers(pkg):
    """Extract list of PyPI maintainers, i.e. those with publish rights

    PyPI JSON endpoint does not contain the maintainers' data found in the
    PyPI UI. IMO, this is an oversight. To retrieve PyPI maintainers data,
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
    # Remove duplicates via set
    maintainers_list = list(set(maintainers_full_list))

    return maintainers_list
