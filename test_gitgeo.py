"""Unit tests and integration tests for git-geo"""

import pytest

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

        # TODO: add tests for repos that don't have github link in normal section
        # but are in package description. Need to add this functioality first.
        # Could be a good hands-dirty task for Kinga
