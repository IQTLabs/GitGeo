"""GitHub API-related functionality"""

import json

import requests

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

	#todo: consider returning "NA" when no value available

	return user_location