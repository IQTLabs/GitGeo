"""Identify committer geographies associated with python package."""

import argparse

from gitgeo.github import get_contributors
from gitgeo.mapping import make_map
from gitgeo.multi_repo_scan import scan_multiple_repos
from gitgeo.printers import print_by_country, print_by_contributor
from gitgeo.pypi import get_pypi_data, extract_github_owner_and_repo


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
        "--multirepo_map",
        dest="multirepo_map",
        action="store",
        type=str,
        help="Convert mutlirepo scan file into map.",
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
        action="store_true",  # when output_csv is not called, default is false
        help="Output results in csv.",
    )
    parser.add_argument(
        "--map",
        dest="map",
        action="store_true",  # when map is not called, default is false
        help="Display country by country results in map.",
    )
    parser.add_argument(
        "--num",
        choices=range(100, 501, 100),  # 501 so that upper limit is 500
        type=int,
        default=100,
        dest="num",
        help="Specify max number of contributors per repo.",
    )
    return parser.parse_args()


def scan_single_package(pkg, summary, num=100):
    """Print location results for single package.

    Printing can either be by contributor or by country.

    Args:
        pkg - name of python package on PyPI
        summary - whether to summarize answers by country or not
        num - max number of contributors to analyze

    Returns:
        null
    """
    pypi_data = get_pypi_data(pkg)
    contributors = get_contributors(pypi_data["github_owner_and_repo"], num)
    print("-----------------")
    print("PACKAGE: {}".format(pkg))
    print("GITHUB REPO: {}".format(pypi_data["github_owner_and_repo"]))
    print("-----------------")

    if summary:
        print_by_country(contributors)
    else:
        print_by_contributor(pkg, contributors, pypi_data=pypi_data)


def scan_single_repo(repo, summary, output_csv, num=100):
    """Print location results for single GitHub repository.

    Printing can either be by contributor or by country.
    Output can optionally be stored as a csv.

    Args:
        repo - URL of repo
        summary - whether to print results by country, i.e. summary.
        output_csv - whether to store output in csv (default: false)
        num - max number of contributors to analyze

    Returns:
        null
    """
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string, num)
    print("-----------------")
    print("GITHUB REPO: {}".format(repo_ending_string))
    print("-----------------")

    if summary:
        print_by_country(contributors)
    else:
        print_by_contributor(repo_ending_string, contributors, output_csv)


def main(): # pragma: no cover
    args = parse_arguments()

    if args.package:
        scan_single_package(args.package, args.summary, args.num)
    elif args.repo:
        if args.map:
            make_map(repo=args.repo, num=args.num)
        else:
            scan_single_repo(args.repo, args.summary, args.output_csv, args.num)
    elif args.multirepo:
        scan_multiple_repos(num=args.num)
    elif args.multirepo_map:
        make_map(csv=args.multirepo_map)
