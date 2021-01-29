"""Identify committer geographies associated with python package"""

import argparse
from collections import Counter

# uncomment these imports when building top package scan functionality
# from custom_csv import create_csv, add_committer_to_csv
from github import get_contributors, get_contributor_location, get_country_from_location
from pypi import (
    get_pypi_data,
    extract_github_owner_and_repo,
)  # , get_top_python_packages


def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--package", help="Specify Python (PyPI) package.")
    parser.add_argument("--repo", help="Specify GitHub repo.")
    parser.add_argument(
        "--summary",
        dest="summary",
        action="store_true",  # when summary is not called, default is false
        help="Display results by country.",
    )

    return parser.parse_args()


def scan_single_package(pkg, summary):
    """Print location results for single package

    Args:
        pkg - name of python package on PyPI

    Returns:
        null
    """
    pypi_data = get_pypi_data(pkg)
    contributors = get_contributors(pypi_data["github_owner_and_repo"])
    print("-----------------")
    print("PACKAGE: {}".format(pkg))
    print("GITHUB REPO: {}".format(pypi_data["github_owner_and_repo"]))
    print("-----------------")

    # print results by country
    if summary:
        print("COUNTRY | # OF CONTRIBUTORS")
        print("---------------------------")
        # todo: place this functionality in separate module
        # todo: bug -- Why are there two different unique none values? Huh
        country_list = []
        for contributor in contributors:
            location = get_contributor_location(contributor)
            country = get_country_from_location(location)
            country_list.append(country)

        country_counter = Counter(country_list)
        for country, count in country_counter.most_common():
            print(country, count)

    # print results contributor by contributor
    else:
        # todo: place this functionality in separate module
        print("CONTRIBUTOR, LOCATION")
        print("* indicates PyPI maintainer")
        print("---------------------")
        for contributor in contributors:
            location = get_contributor_location(contributor)
            country = get_country_from_location(location)
            try:
                if contributor in pypi_data["pypi_maintainers"]:
                    print(contributor, "*", "|", location, "|", country)
                else:
                    print(contributor, "|", location, "|", country)
            except UnicodeEncodeError:
                print(contributor, "| error")


def scan_single_repo(repo):
    """Print location results for single GitHub repository

    Args:
        repo - URL of repo on GitHub

    Returns:
        null
    """
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string)
    print("-----------------")
    print("PACKAGE: {}".format(repo_ending_string))
    print("-----------------")
    print("CONTRIBUTOR, LOCATION")
    print("---------------------")
    # todo: add summary logic
    for contributor in contributors:
        # todo: use functionality that is place in separate module
        location = get_contributor_location(contributor)
        country = get_country_from_location(location)
        try:
            print(contributor, "|", location, "|", country)
        except UnicodeEncodeError:
            print(contributor, "| error")


# def scan_top_package(top_n=100):
#    """Stub for scanning most downloaded python packages"""
#    pass


# def scan_dependencies(filename):
#    """Stub for scanning a requirements.txt or similar dependencies file"""
#     pass


if __name__ == "__main__":

    args = parse_arguments()

    if args.package:
        scan_single_package(args.package, args.summary)

    if args.repo:
        scan_single_repo(args.repo)

    # if args.top_packages:
    # 	create_csv()
    # 	# Create list of packages
    # 	for pkg in TEST_PKG:
    # 		github_repo = get_github_repo(pkg)
    # 		contributors = get_contributors(github_repo)
    # 		for contributor in contributors:
    # 			location = get_contributor_location(contributor)
    # 			add_committer_to_csv(pkg, contributor, location)
    # 			print(pkg, contributor, location)
