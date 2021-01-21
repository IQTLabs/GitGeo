"""Identify committer geographies associated with python package"""

# todo: add github API token capability to increate allowable
# rate of GitHub API usage

import argparse
import csv
import os

from custom_csv import (
	create_csv,
	add_committer_to_csv
	)
from github import (
	get_contributors,
	get_contributor_location
	)
from pypi import (
	get_top_python_packages,
	get_github_repo
	)

def parse_arguments():
	"""Parse command line arguments"""

	parser = argparse.ArgumentParser()
	parser.add_argument("--package",
						help="Specify Python (PyPI) package.")
	
	return parser.parse_args()

def scan_single_package(pkg):
	"""Print location results for single package

	Args:
		pkg - name of python package on PyPI

	Returns:
		null
	"""
	github_repo = get_github_repo(pkg)
	contributors = get_contributors(github_repo)
	print("-----------------")
	print("PACKAGE: {}".format(pkg))
	print("-----------------")
	print("CONTRIBUTOR, LOCATION")
	print("---------------------")
	for contributor in contributors:
		location = get_contributor_location(contributor)
		print(contributor, "|", location)


if __name__ == "__main__":

	args = parse_arguments()

	if args.package:
		scan_single_package(args.package)

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
