"""Unit tests and integration tests for git-geo"""

import os

import pytest

from custom_csv import create_csv, add_committer_to_csv
from github import get_contributors, get_contributor_location
from pypi import get_top_python_packages, get_github_repo


class TestPypiFunctionality:
    """Unit tests related to PyPI functionality"""

    def test_get_top_python_packages(self):
        """Unit test for get_top_python_packages()"""
        top_python_packages = get_top_python_packages(top_N=5)
        assert top_python_packages == [
            "urllib3",
            "six",
            "botocore",
            "requests",
            "python-dateutil",
        ]

    def test_get_github_repo(self):
        """Unit test for get_github_repo()"""
        # tests for packages with standard location of GitHub link on PyPI page
        github_repo_requests = get_github_repo("requests")
        assert github_repo_requests == "psf/requests"
        github_repo_networkml = get_github_repo("networkml")
        assert github_repo_networkml == "IQTLabs/NetworkML"

        # tests for packages with no GitHub link on PyPI page
        github_repo_reportlab = get_github_repo("reportlab")
        assert github_repo_reportlab == ""
        github_repo_bfengine = get_github_repo("bfengine")
        assert github_repo_bfengine == ""

        # test for package names that are not on PyPI
        with pytest.raises(Exception):
            get_github_repo("googlemooglegoogle")
        with pytest.raises(Exception):
            get_github_repo("thispackageismalware")

    @pytest.mark.xfail  # test should fail, until functionality implemented
    def test_get_github_repo_with_link_in_description(self):
        """Unit test for get_github_repo functionality that is not yet implemented"""
        # Could be a good hands-dirty task for Kinga
        github_repo = get_github_repo("python-dateutil")
        assert github_repo == "dateutil/dateutil"


class TestGitHubFunctionality:
    """Unit tests related to GitHub functionality"""

    def test_get_contributors(self):
        """Unit test for get_contributors()"""
        contributors = get_contributors("jspeed-meyers/pcap2map")
        assert contributors == ["jspeed-meyers"]

    def test_get_contributor_location(self):
        """Unit test for get_contributor_location()"""
        location = get_contributor_location("anarkiwi")
        assert location == "Wellington, New Zealand"

class TestCsvFunctionality:
    def test_create_csv(self):
        """Unit test for create_csv()"""
        create_csv()
        assert os.path.exists("git-geo-results.csv") == True

    def test_add_committer_to_csv(self):
        add_committer_to_csv("googlemoogle", "eschmidt", "innovation-island")
        os.remove("git-geo-results.csv") # remove file
