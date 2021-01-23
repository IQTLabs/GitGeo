"""PyPI and python package-related functions"""

import json
import sys

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


def get_github_repo(pkg):
    """Return GitHub repo associated with a python package

    NOTE: Only the repo owner and and repo name are returned.
    Not the whole URL. e.g. psf/requrests.

    Args:
        pkg: the name of a python package found on PyPI

    Returns:
        str: the owner and name of a github URL
    """
    # Retrieve PyPI package JSON data
    try:
        pkg_url = "https://pypi.org/pypi/" + pkg + "/json"
        response = requests.get(pkg_url)
        pypi_pkg = response.json()
    # TODO: Fix bare except with non-simplejson JSON error type
    except:
        print("Exception: ", e)
        print("ERROR: No such package on PyPI")
        sys.exit(1)  # 1 indicates error

    github_page = ""
    # Check potential fields for a github link
    potential_github_fields = [pypi_pkg["info"]["home_page"]]
    # Add project url fields if url fields present
    if pypi_pkg["info"]["project_urls"]:
        for _, url in pypi_pkg["info"]["project_urls"].items():
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
