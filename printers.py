"""Functions for printing contributor location results"""

from collections import Counter

from github import get_contributor_location, get_country_from_location


def print_by_country(contributors):
    """Print contributors aggregated by country

    Args:
        contributors: a list of contributors

    Returns:
    null
    """
    print("COUNTRY | # OF CONTRIBUTORS")
    print("---------------------------")
    country_list = []
    for contributor in contributors:
        location = get_contributor_location(contributor)
        country = get_country_from_location(location)
        country_list.append(country)

    country_counter = Counter(country_list)
    for country, count in country_counter.most_common():
        print(country, count)


def print_by_contributor(contributors, pypi_data=None):
    """Print location results by contributor

    Args:
        contributors - a list of contributors

    Returns:
        null
    """
    print("CONTRIBUTOR, LOCATION")
    if pypi_data is not None:
        print("* indicates PyPI maintainer")
    print("---------------------")
    for contributor in contributors:
        location = get_contributor_location(contributor)
        country = get_country_from_location(location)
        try:
            # Check if pypi_data is not None, indicating a PyPI package scan
            if pypi_data is not None and contributor in pypi_data["pypi_maintainers"]:
                print(contributor, "*", "|", location, "|", country)
            else:
                print(contributor, "|", location, "|", country)
        except UnicodeEncodeError:
            print(contributor, "| error")
