"""Identify committer geographies associated with python package"""

import argparse

from github import get_contributors
from printers import print_by_country, print_by_contributor
from pypi import get_pypi_data, get_top_python_packages, get_github_url


def parse_arguments():  # pragma: no cover
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

    Printing can either be by contributor or by country

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

    if summary:
        print_by_country(contributors)
    else:
        print_by_contributor(contributors, pypi_data)


def scan_single_repo(repo, summary):
    """Print location results for single GitHub repository

    Printing can either be by contributor or by country

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

    if summary:
        print_by_country(contributors)
    else:
        print_by_contributor(contributors)

    # def scan_top_packages(top_n=100):
    """Stub for scanning most downloaded python packages"""
    # create_csv()
    # Create list of packages
    # for pkg in get_top_python_packages():
    #     pypi_data = get_pypi_data(pkg)
    #     print("-----------------")
    #     print("{} :{}".format(pkg, pypi_data["github_owner_and_repo"]))
    #     contributors = get_contributors(github_repo)
    #   for contributor in contributors:
    #       location = get_contributor_location(contributor)
    #       add_committer_to_csv(pkg, contributor, location)
    #       print(pkg, contributor, location)


# def scan_dependencies(filename):
#    """Stub for scanning a requirements.txt or similar dependencies file"""
#     pass


if __name__ == "__main__":  # pragma: no cover

    args = parse_arguments()

    # scan_top_packages()

    if args.package:
        scan_single_package(args.package, args.summary)

    if args.repo:
        scan_single_repo(args.repo, args.summary)
