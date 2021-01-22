"""Unit tests and integration tests for git-geo"""

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
        # test(s) for packages with no GitHub link on PyPI page
        github_repo_reportlab = get_github_repo("reportlab")
        assert github_repo_reportlab == ""
        # TODO: fix bug that results from incorrect assumption that all PyPI pages
        # have an info section for searching (JSM thinks this is the bug 1/22/21)
        # bug-inducing test start
        # github_repo_bfengine = get_github_repo("bfengine")
        # assert github_repo_bfengine == ''
        # bug-inducing test end
        # TODO: add tests for repos that don't have github link in normal section
        # but are in package description. Need to add this functioality first.
        # Could be a good hands-dirty task for Kinga
