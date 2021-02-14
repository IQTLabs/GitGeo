"""GitHub API-related functionality."""

import json
import os

import requests

# access secret token for GitHub API to increase rate limit
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_contributors(repo, max_num_contributors=100):
    """Generate list of up to top 500 contributors for a repo.

    Create list of contributors for a repo. The GitHub API will return up
    to the top 500 contributors for a repo. The list will be organized by
    the contributors with the most commits in descending order.

    Args:
        repo: a GitHub repo url
        max_num_contributors: the maximum number of contributors to return
                              if available

    Return:
        list: committer handles
    """
    committers = []
    max_num_pages = int(max_num_contributors / 100)

    # the loop handles pagination associated with the GitHub API
    for page in range(1, max_num_pages + 1):
        response = requests.get(
            "https://api.github.com/repos/"
            + repo
            + "/contributors?page="
            + str(page)
            + "&per_page=100",
            # convert username and token to strings per requests's specifications
            auth=(str(GITHUB_USERNAME), str(GITHUB_TOKEN)),
        )

        if response.ok:
            repo_items = json.loads(response.text or response.content)
            for item in repo_items:
                committers.append(item["login"])

        # determine if pagination has ended or not. If there are more pages
        # to return, the API JSON will include a 'next' field
        if "next" not in response.links:
            break

    return committers


def get_contributor_location(user):
    """Return geographic location, if present on github page, of user.

    Args:
        user: the GitHub user name

    Return:
        str: a geographic location
    """
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
