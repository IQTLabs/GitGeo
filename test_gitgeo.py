"""Unit tests and integration tests for git-geo"""

from pypi import get_top_python_packages, get_github_repo


class TestPypiFunctionality:
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
        github_repo_requests = get_github_repo("requests")
        assert github_repo_requests == "psf/requests"
        github_repo_networkml = get_github_repo("networkml")
        assert github_repo_networkml == "IQTLabs/NetworkML"
        #TODO: add tests for repos that don't have any github link (annoyingly!)
        #TODO: add tests for repos that don't have github link in normal section but are in package descriptiono