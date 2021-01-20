"""Identify committer geographies associated with python package"""

import json

import requests
import simplejson

def get_top_python_packages(TOP_N=100):
	"""Generate list of most downloaded python packages

	Args:
		TOP_N: the number of most downloaded packages to return

	Returns:
		(list) Names of most downloaded packages
	"""
	# JSON file containing top 4000 packages
	# found here: https://hugovk.github.io/top-pypi-packages/
	top_python_pkgs = "top_python_pkg_downloads.json"

	with open(top_python_pkgs, 'r') as j:

	     contents = json.loads(j.read())

	     # store names of top packges
	     top_pkgs = []
	     cnt = 0
	     for pkg in contents['rows']:
	     	# only append TOP_N number of packages
	     	if cnt == TOP_N:
	     		break
	     	top_pkgs.append(pkg['project'])
	     	cnt += 1

	     return top_pkgs


def get_github_repo(pkg):
	"""Return GitHub repo associated with a python package

	Args:
		pkg: the name of a python package found on PyPI

	Returns:
		str: a github URL
	"""
	# Retrieve PyPI package JSON data
	try:
		pkg_url = "https://pypi.org/pypi/" + pkg + "/json"
		response = requests.get(pkg_url)
		pypi_pkg = response.json()
	except simplejson.errors.JSONDecodeError:
		print("ERROR: No such package on PyPI")
		sys.exit(1)

	github_page = ""
	# Check potential fields for a github link
	potential_github_fields = [pypi_pkg["info"]["home_page"]]
	# Add project url fields
	for _, url in pypi_pkg["info"]["project_urls"].items():
		potential_github_fields.append(url)
	# TODO: Add a search of the text in PyPI for any GitHub mentions
	# Only do this for second revision
	for field in potential_github_fields:
		# Any field with github in it must be github link
		if "github" in field:
			github_page = field
			break

	return github_page


# Identify up to top 100 committers associated with a Github repo
def get_contributors(repo):
	"""Generate list of up to top 100 contributors on package

	Args:
		repo: a github repo url 

	Return:
		list: committer handles
	"""
	# TODO: Consider looping thru pages 1-5. The github contributors API will return up
	# to 500 contributors
	# TODO: Enable using GitHub token (need to create one and then store in secret file)
	r = requests.get('https://api.github.com/repos/' + repo + '/contributors?page=1&per_page=100')
	
	committers = []
	if(r.ok):
		repoItems = json.loads(r.text or r.content)
		for item in repoItems:
			committers.append(item['login'])

	return committers
		

def get_contributor_location(user):
	"""Return geographic location, if present on github page, of user

	Args:
		user: the GitHub user name

	Return:
		str: a geographic location
	"""
	# TODO: What to do if location is not present? What to do
	# if location is not listed in profile?
	# https://stackoverflow.com/questions/26983017/detect-ip-address-of-github-commit
	# https://gist.github.com/paulmillr/2657075
	r = requests.get('https://api.github.com/users/' + user)
	
	user_location = ''
	if(r.ok):
		userInfo = json.loads(r.text or r.content)
		user_location = userInfo['location']

	return user_location


if __name__ == "__main__":
	#top_pkgs = get_top_python_packages()
	#print(top_pkgs)
	#for pkg in top_pkgs:
	# 	print(pkg, ": ", get_github_repo(pkg))
	print(get_contributors("psf/requests"))
	# print(get_contributor_location('anarkiwi'))


# For each committer, check if there is geographic location

# Output csv with project, committer, location fields