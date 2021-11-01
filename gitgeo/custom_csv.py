"""Custom CSV-related functionality."""

# pylint: disable=too-many-arguments, bad-continuation

import csv
import os


def create_csv(results_type, timestamp):
    """Create new csv to store GitGeo results.

    Delete any existing csv and the create new csv.

    Args:
        results_type - a string indicating by contributor or by country
        timestamp - datetime to create unique file name
    Returns:
        None
    """
    filename = os.path.join("results", results_type + "_" + timestamp + ".csv")

    # Create new csv file with column names
    with open(filename, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["software_name", "username", "location", "country"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


def add_committer_to_csv(
    results_type, software_name, timestamp, username, location, country
):
    """Write committer info to existing csv file.

    Use to create dataset of location data for analysis.

    Args:
        results_type - a string indicating by contributor or by country
        software_name - package name or github name
        timestamp - datetime to append to unique existing file
        username - GitHub username
        location - Geographic info from GitHub profile
        country - country predicted by GitGeo

    Returns:
        null
    """
    # replace slashes to avoid incorrect creation of directories
    software_name = software_name.replace("/", "_")
    filename = os.path.join("results", results_type + "_" + timestamp + ".csv")
    # newline='' prevents spaces in between entries. Setting encoding to utf-8
    # ensures that most (all?) characters can be read. "a" is for append.
    with open(filename, "a", encoding="utf-8", newline="") as file:
        fieldnames = ["software_name", "username", "location", "country"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(
            {
                "software_name": software_name,
                "username": username,
                "location": location,
                "country": country,
            }
        )
