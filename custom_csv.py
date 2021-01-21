"""Custom CSV-related functionality"""

import csv
import os

def create_csv():
	"""Create new csv to store git-geo result

	Delete any existing csv and the create new csv.
	"""
	# delete csv if it already exists
	FILENAME = "git-geo-results.csv"
	try:
		os.remove(FILENAME)
	except OSError:
		print("ERROR: File import error")
		sys.exit(1)		

	# Create new csv file with column names
	with open(FILENAME, "w") as file:
		fieldnames = ['pkg', 'username', 'location']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()


def add_committer_to_csv(pkg, username, location):
	"""Write committer info to existing csv file

	Args:
		pkg - package name
		username - GitHub username
		location - Geographic info from GitHub profile

	Returns:
		null
	"""
	with open("git-geo-results.csv", 'a') as file:
		fieldnames = ['pkg', 'username', 'location']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writerow({'pkg': pkg,
    					 'username': username,
					 	 'location': location})
