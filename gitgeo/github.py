"""GitHub API-related functionality."""

import itertools
import json
import os

import requests

# GITHUB USERNAME AND TOKEN SECTION - See next ~50 lines.

# access secret token for GitHub API to increase rate limit
# see below for token-related functionality
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")


def get_github_tokens(token_file="tokens.txt"):  # nosec
    """Retrieve GitHub token or tokens.

    Either retrieve tokens from the tokens.txt file or retrieve the
    environmental variable. Then convert the results to a list that
    cycles to enable the GitHub API calls to easily cycle through
    tokens. The itertools.cycle data structure allows the use of
    next() to retrieve the next item in the list, including allowing the
    last list item to link to the first list item.

    Args:
        token_file - a txt document containing one token per line

    Returns:
        cycle_token_list - a list of tokens (>=1) to cycle through

    """
    token_list = read_in_github_token_list(token_file)
    if token_list:
        cycle_token_list = itertools.cycle(token_list)
    else:
        # place single environmental variable in list so that cycle
        # functionality will still work properly
        cycle_token_list = itertools.cycle([os.environ.get("GITHUB_TOKEN")])

    # return iterable token list.
    return cycle_token_list


def read_in_github_token_list(file="tokens.txt"):
    """If a tokens file exists, extract tokens line by line.

    This functionality enables reading in multiple GitHub personal
    access tokens so that a user can use the GitHub API more than
    if he or she had only one token.

    Args:
        file - a txt document containing one token per line

    Returns:
        tokens - a list of tokens
    """
    tokens = []
    try:
        with open(file, "r") as token_file:
            for token in token_file:
                # remove whitespace such as returns from token string
                tokens.append(token.strip())
    except FileNotFoundError:
        pass

    return tokens


# place GitHub token call here, in this admittedly awkward spot, so that
# token-related functions are available above
GITHUB_TOKENS = get_github_tokens()


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
        # cycle through GitHub tokens
        github_token = next(GITHUB_TOKENS)
        response = requests.get(
            "https://api.github.com/repos/"
            + repo
            + "/contributors?page="
            + str(page)
            + "&per_page=100",
            # convert username and token to strings per requests's specifications
            auth=(str(GITHUB_USERNAME), str(github_token)),
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
    # cycle through GitHub tokens
    github_token = next(GITHUB_TOKENS)
    response = requests.get(
        "https://api.github.com/users/" + user,
        # convert username and token to strings per requests's specifications
        auth=(str(GITHUB_USERNAME), str(github_token)),
    )

    user_location = ""
    if response.ok:
        user_info = json.loads(response.text or response.content)
        user_location = user_info["location"]

    return user_location
