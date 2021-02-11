"""Identify committer geographies associated with python package."""

import argparse

from github import get_contributors
from mapping import make_map
from multi_repo_scan import scan_multiple_repos
from printers import print_by_country, print_by_contributor
from pypi import get_pypi_data, extract_github_owner_and_repo


def parse_arguments():  # pragma: no cover
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", help="Specify Python (PyPI) package.")
    parser.add_argument("--repo", help="Specify GitHub repo.")
    parser.add_argument(
        "--multirepo",
        dest="multirepo",
        action="store_true",
        help="Scan multiple repos from input file.",
    )
    parser.add_argument(
        "--summary",
        dest="summary",
        action="store_true",  # when summary is not called, default is false
        help="Display results by country.",
    )
    parser.add_argument(
        "--output_csv",
        dest="output_csv",
        action="store_true",  # when summary is not called, default is false
        help="Output results in csv.",
    )
    parser.add_argument(
        "--map",
        dest="map",
        action="store_true",  # when summary is not called, default is false
        help="Display country by country results in map.",
    )
    return parser.parse_args()


def scan_single_package(pkg, summary):
    """Print location results for single package.

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
        print_by_contributor(pkg, contributors, pypi_data=pypi_data)


def scan_single_repo(repo, summary, output_csv):
    """Print location results for single GitHub repository.

    Printing can either be by contributor or by country.
    Output can optionally be stored as a csv.

    Args:
        repo - URL of repo
        summary - whether to print results by country, i.e. summary.
        output_csv - whether to store output in csv (default: false)

    Returns:
        null
    """
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string)
    print("-----------------")
    print("GITHUB REPO: {}".format(repo_ending_string))
    print("-----------------")

    if summary:
        print_by_country(contributors)
    else:
        print_by_contributor(repo_ending_string, contributors, output_csv)


if __name__ == "__main__":  # pragma: no cover

    args = parse_arguments()

    if args.package:
        scan_single_package(args.package, args.summary)
    elif args.repo:
        if args.map:
            make_map(args.repo)
        else:
            scan_single_repo(args.repo, args.summary, args.output_csv)
    elif args.multirepo:
        scan_multiple_repos()
