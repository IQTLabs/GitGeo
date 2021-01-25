"""Unit tests and integration tests for git-geo"""

import os

import pytest

from custom_csv import create_csv, add_committer_to_csv
from github import get_contributors, get_contributor_location
from pypi import get_top_python_packages, get_pypi_data, extract_github_owner_and_repo


class TestPypiFunctionality:
    """Unit tests related to PyPI functionality"""

    def test_get_top_python_packages(self):
        """Unit test for get_top_python_packages()"""
        top_python_packages = get_top_python_packages(top_n=5)
        assert top_python_packages == [
            "urllib3",
            "six",
            "botocore",
            "requests",
            "python-dateutil",
        ]

    def test_get_pypi_data(self):
        """Unit test for get_pypi_data()"""
        requests_pypi_data = get_pypi_data("requests")

    def test_get_github_url_owner_and_repo(self):
        """Unit tests for get_github_URL_owner_and_repo()"""
        # tests for packages with standard location of GitHub link on PyPI page
        requests_pypi_data = get_pypi_data("requests")
        assert requests_pypi_data["github_owner_and_repo"] == "psf/requests"
        networkml_pypi_data = get_pypi_data("networkml")
        assert networkml_pypi_data["github_owner_and_repo"] == "IQTLabs/NetworkML"

        # tests for packages with no GitHub link on PyPI page
        reportlab_pypi_data = get_pypi_data("reportlab")
        assert reportlab_pypi_data["github_owner_and_repo"] == ""
        bfengine_pypi_data = get_pypi_data("bfengine")
        assert bfengine_pypi_data["github_owner_and_repo"] == ""

        # test for package names that are not on PyPI
        with pytest.raises(Exception):
            get_pypi_data("googlemooglegoogle")
        with pytest.raises(Exception):
            get_pypi_data("thispackageismalware")

    @pytest.mark.xfail  # test should fail, until functionality implemented
    def test_get_github_url_owner_and_repo_with_link_in_description(self):
        """Unit test for get_github_URL_owner_and_repo functionality that is not yet implemented"""
        # Could be a good hands-dirty task for Kinga
        pythondateutil_pypi_data = get_pypi_data("python-dateutil")
        assert pythondateutil_pypi_data["github_owner_and_repo"] == "dateutil/dateutil"

    def test_get_pypi_maintainers(self):
        """Unit test for get_pypi_maintainers()"""
        requests_pypi_data = get_pypi_data("pcap2map")
        assert requests_pypi_data["pypi_maintainers"] == ["jspeed-meyers"]


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

    def test_extract_github_owner_and_repo(self):
        """Unit test for extract_github_owner_and_repo()"""
        owner_and_repo = extract_github_owner_and_repo("www.github.com/psf/requests")
        assert owner_and_repo == "psf/requests"


class TestCsvFunctionality:
    """Unit tests related to CSV functionality"""

    def test_create_csv(self):
        """Unit test for create_csv()"""
        create_csv()
        assert os.path.exists("git-geo-results.csv")

    def test_add_committer_to_csv(self):
        """Unit test fpr add_committer_to_csv"""
        add_committer_to_csv("googlemoogle", "eschmidt", "innovation-island")
        os.remove("git-geo-results.csv")  # remove file
