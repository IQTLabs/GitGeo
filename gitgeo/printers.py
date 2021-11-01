"""Functions for printing contributor location results."""

from collections import Counter
import time

from gitgeo.custom_csv import create_csv, add_committer_to_csv
from gitgeo.github import get_contributor_location
from gitgeo.geolocation import get_country_from_location


def print_by_country(contributors):
    """Print contributors aggregated by country.

    Print contributor county by country to terminal window.

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


def print_by_contributor(software_name, contributors, output_csv=False, pypi_data=None):
    """Print location results by contributor.

    Print contributors and countries to terminal window. If output csv is set
    to true, then also output results to a csv file.

    Args:
        software_name - name of package or repo
        contributors - a list of contributors
        output_csv - whether to output a csv.
        pypi_data - a pypi data object.

    Returns:
        null
    """
    # create csv if output_csv specified
    if output_csv:
        # unique current time timestamp to create unique filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        create_csv("contributor", timestamp)

    print("CONTRIBUTOR, LOCATION")
    if pypi_data is not None:
        print("* indicates PyPI maintainer")
    print("---------------------")
    for contributor in contributors:
        location = get_contributor_location(contributor)
        country = get_country_from_location(location)
        if output_csv:
            add_committer_to_csv(
                "contributor", software_name, timestamp, contributor, location, country
            )
        try:
            # Check if pypi_data is not None, indicating a PyPI package scan
            if pypi_data is not None and contributor in pypi_data["pypi_maintainers"]:
                print(contributor, "*", "|", location, "|", country)
            else:
                print(contributor, "|", location, "|", country)
        except UnicodeEncodeError:
            print(contributor, "| error")
