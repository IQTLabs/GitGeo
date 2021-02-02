"""Unit tests and integration tests for GitGeo."""

# pylint: disable=no-self-use, too-many-locals

import os
import textwrap

import pytest

from custom_csv import create_csv, add_committer_to_csv
from github import get_contributors, get_contributor_location
from geolocation import get_country_from_location
from main import scan_single_package, scan_single_repo
from printers import print_by_contributor, print_by_country
from pypi import get_top_python_packages, get_pypi_data, extract_github_owner_and_repo


class TestPypiFunctionality:
    """Unit tests related to PyPI functionality."""

    def test_get_top_python_packages(self):
        """Unit test for get_top_python_packages()."""
        top_python_packages = get_top_python_packages(top_n=5)
        assert top_python_packages == [
            "urllib3",
            "six",
            "botocore",
            "requests",
            "python-dateutil",
        ]

    def test_get_github_url_owner_and_repo(self):
        """Unit tests for get_github_URL_owner_and_repo()."""
        # tests for packages with standard location of GitHub link on PyPI page
        requests_pypi_data = get_pypi_data("requests")
        assert requests_pypi_data["github_owner_and_repo"] == "psf/requests"
        networkml_pypi_data = get_pypi_data("networkml")
        assert networkml_pypi_data["github_owner_and_repo"] == "IQTLabs/NetworkML"
        pandas_pypi_data = get_pypi_data("pandas")
        assert pandas_pypi_data["github_owner_and_repo"] == "pandas-dev/pandas"
        awscli_pypi_data = get_pypi_data("awscli")
        assert awscli_pypi_data["github_owner_and_repo"] == "aws/aws-cli"
        protobuf_pypi_data = get_pypi_data("protobuf")
        assert protobuf_pypi_data["github_owner_and_repo"] == "protocolbuffers/protobuf"
        pillow_pypi_data = get_pypi_data("pillow")
        assert pillow_pypi_data["github_owner_and_repo"] == "python-pillow/Pillow"
        tornado_pypi_data = get_pypi_data("tornado")
        assert tornado_pypi_data["github_owner_and_repo"] == "tornadoweb/tornado"
        typingextensions_pypi_data = get_pypi_data("typing-extensions")
        assert typingextensions_pypi_data["github_owner_and_repo"] == "python/typing"
        tensorflow_pypi_data = get_pypi_data("tensorflow")
        assert tensorflow_pypi_data["github_owner_and_repo"] == "tensorflow/tensorflow"

        # tests for packages with no GitHub link on PyPI page
        reportlab_pypi_data = get_pypi_data("reportlab")
        assert reportlab_pypi_data["github_owner_and_repo"] == ""
        bfengine_pypi_data = get_pypi_data("bfengine")
        assert bfengine_pypi_data["github_owner_and_repo"] == ""
        docutils_pypi_data = get_pypi_data("docutils")
        assert docutils_pypi_data["github_owner_and_repo"] == ""

        # test for package names that are not on PyPI
        with pytest.raises(Exception):
            get_pypi_data("googlemooglegoogle")

    def test_get_github_url_owner_and_repo_with_link_in_description(self):
        """Unit test for get_github_URL_owner_and_repo functionality."""
        pythondateutil_pypi_data = get_pypi_data("python-dateutil")
        assert pythondateutil_pypi_data["github_owner_and_repo"] == "dateutil/dateutil"
        rsa_pypi_data = get_pypi_data("rsa")
        assert rsa_pypi_data["github_owner_and_repo"] == "sybrenstuvel/python-rsa"
        py_pypi_data = get_pypi_data("py")
        assert py_pypi_data["github_owner_and_repo"] == "pytest-dev/py"

    @pytest.mark.xfail  # known bug, don't know how to fix without breaking other code
    def test_get_github_url_owner_and_repo_with_link_in_description_hyperlinked(self):
        """
        Unit test for get_github_URL_owner_and_repo functionality where URL is
        embedded in hypertext
        """
        uritemplate_pypi_data = get_pypi_data("uritemplate")
        assert (
            uritemplate_pypi_data["github_owner_and_repo"] == "python-hyper/uritemplate"
        )

    def test_get_pypi_maintainers(self):
        """Unit test for get_pypi_maintainers()."""
        requests_pypi_data = get_pypi_data("pcap2map")
        assert requests_pypi_data["pypi_maintainers"] == ["jspeed-meyers"]


class TestGitHubFunctionality:
    """Unit tests related to GitHub functionality"""

    def test_get_contributors(self):
        """Unit test for get_contributors()."""
        assert get_contributors("jspeed-meyers/pcap2map") == ["jspeed-meyers"]

    def test_get_contributor_location(self):
        """Unit test for get_contributor_location()."""
        assert get_contributor_location("anarkiwi") == "Wellington, New Zealand"

    def test_get_country_from_location_standard_order_with_comma(self):
        """test get_country_from_location on standard order pairs with comma."""
        assert get_country_from_location("Wellington, New Zealand") == "New Zealand"
        assert get_country_from_location("Jordan, Minnesota") == "United States"
        assert get_country_from_location("Jordan, MN") == "United States"
        assert get_country_from_location("Atlanta, Georgia") == "United States"
        assert get_country_from_location("Atlanta, Ga") == "United States"
        assert get_country_from_location("London, England") == "United Kingdom"
        assert get_country_from_location("Prague, Czech Republic") == "Czech Republic"
        assert get_country_from_location("Virginia, USA") == "United States"
        assert get_country_from_location("Naperville, IL") == "United States"
        assert get_country_from_location("Toronto, Ontario, Canada") == "Canada"
        assert get_country_from_location("Berlin, DE") == "Germany"
        assert get_country_from_location("CSU Sacramento") == "United States"

    def test_get_country_from_location_nonstandard_order(self):
        """test get_country_from_location on non-standard order pairs."""
        assert get_country_from_location("Russia, Moscow") == "Russia"
        assert get_country_from_location("Russia, Nizhny Novgorod") == "Russia"

    def test_get_country_from_location_standard_order_no_comma(self):
        """test get_country_from_location on standard order pairs without comma."""
        assert get_country_from_location("Menlo Park CA") == "United States"

    def test_get_country_from_location_world_cities(self):
        """test get_country_from_location on world city names."""
        assert get_country_from_location("Tokyo") == "Japan"
        assert get_country_from_location("London") == "United Kingdom"
        assert get_country_from_location("Jakarta") == "Indonesia"
        assert get_country_from_location("Beijing") == "China"
        assert get_country_from_location("Washington D.C.") == "United States"
        assert get_country_from_location("Toronto, ON") == "Canada"

    def test_get_country_from_location_country_abbreviations(self):
        """test get_country_from_location on country abbreviations."""
        assert get_country_from_location("USA") == "United States"
        assert get_country_from_location("Cambridge, UK") == "United Kingdom"
        assert get_country_from_location("UK") == "United Kingdom"

    def test_get_country_from_location_corner_case_geographies(self):
        """test get_country_from_location on unusual geographies."""
        assert get_country_from_location("Palestine") == "Palestine"
        assert get_country_from_location("San Francisco Bay Area") == "United States"

    def test_extract_github_owner_and_repo(self):
        """Unit test for extract_github_owner_and_repo()."""
        owner_and_repo = extract_github_owner_and_repo("www.github.com/psf/requests")
        assert owner_and_repo == "psf/requests"


class TestCsvFunctionality:
    """Unit tests related to CSV functionality"""

    def test_create_csv(self):
        """Unit test for create_csv()."""
        create_csv()
        assert os.path.exists("git-geo-results.csv")

    def test_add_committer_to_csv(self):
        """Unit test fpr add_committer_to_csv."""
        add_committer_to_csv("googlemoogle", "eschmidt", "innovation-island")
        os.remove("git-geo-results.csv")  # remove file


def test_print_by_contributor_repo(capsys):
    """Unit test for print by contributors for GitHub repo."""
    repo = "jspeed-meyers/pcap2map"
    contributors = get_contributors(repo)
    print_by_contributor(contributors)
    captured = capsys.readouterr()  # capture output printed
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        CONTRIBUTOR, LOCATION
        ---------------------
        jspeed-meyers | None | None\n"""
    )
    assert captured.out == output_text


def test_print_by_contributor_package(capsys):
    """Unit test for print_by_contributor() for networml python package."""
    pkg = "networkml"
    pypi_data = get_pypi_data(pkg)
    contributors = get_contributors(pypi_data["github_owner_and_repo"])
    print_by_contributor(contributors, pypi_data)
    captured = capsys.readouterr()  # capture output
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        CONTRIBUTOR, LOCATION
        * indicates PyPI maintainer
        ---------------------
        cglewis * | USA | United States
        anarkiwi | Wellington, New Zealand | New Zealand
        CStephenson970 | None | None
        renovate-bot | None | None
        lilchurro | None | None
        jspeed-meyers * | None | None
        pyup-bot | None | None
        rashley-iqt | None | None
        alshaboti | Wellington, New Zealand | New Zealand
        jseparovic | Mountain View, CA | United States
        squeeve | None | None
        gregs5 | Washington DC | United States
        krb1997 | None | None
        toddstavish | None | None
        sneakyoctopus12 | None | None
        Hax7 | Palestine | None
        paulgowdy | Menlo Park CA | United States\n"""
    )
    assert captured.out == output_text


def test_print_by_country(capsys):
    """Unit test for print_by_country() for networml python package."""
    repo = "https://www.github.com/iqtlabs/networkml"
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string)
    print_by_country(contributors)
    captured = capsys.readouterr()  # capture outpt printed to date
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        COUNTRY | # OF CONTRIBUTORS
        ---------------------------
        None 11
        United States 4
        New Zealand 2\n"""
    )
    assert captured.out == output_text


def test_scan_single_package_no_summary(capsys):
    """Integration test for scan_single_package with no summary."""
    pkg = "pcap2map"
    scan_single_package(pkg, False)  # False indicates no summary
    captured = capsys.readouterr()  # capture output printed
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        -----------------
        PACKAGE: pcap2map
        GITHUB REPO: jspeed-meyers/pcap2map
        -----------------
        CONTRIBUTOR, LOCATION
        * indicates PyPI maintainer
        ---------------------
        jspeed-meyers * | None | None\n"""
    )
    assert captured.out == output_text


def test_scan_single_package_with_summary(capsys):
    """Integration test for scan_single_package with summary."""
    pkg = "networkml"
    scan_single_package(pkg, True)  # True indicates do summary
    captured = capsys.readouterr()  # capture output printed
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        -----------------
        PACKAGE: networkml
        GITHUB REPO: IQTLabs/NetworkML
        -----------------
        COUNTRY | # OF CONTRIBUTORS
        ---------------------------
        None 11
        United States 4
        New Zealand 2\n"""
    )
    assert captured.out == output_text


@pytest.mark.xfail  # known bug, likely with capsys and pytest, test fails in actions
def test_scan_single_repo_no_summary(capsys):
    """Integration test for scan_single_repo with no summary."""
    repo = "https://www.github.com/jspeed-meyers/pcap2map"
    scan_single_repo(repo, False)  # False indicates no summary
    captured = capsys.readouterr()  # capture output printed
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        -----------------
        GITHUB REPO: jspeed-meyers/pcap2map
        -----------------
        CONTRIBUTOR, LOCATION
        ---------------------
        jspeed-meyers | None | None\n"""
    )
    assert captured.out == output_text


@pytest.mark.xfail  # known bug, likely with capsys and pytest, test fails in actions
def test_scan_single_repo_with_summary(capsys):
    """Integration test for scan_single_repo with summary."""
    repo = "https://www.github.com/IQTLabs/NetworkML"
    scan_single_repo(repo, True)  # True indicates summary
    captured = capsys.readouterr()  # capture output printed
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        -----------------
        GITHUB REPO: IQTLabs/NetworkML
        -----------------
        COUNTRY | # OF CONTRIBUTORS
        ---------------------------
        None 11
        United States 4
        New Zealand 2\n"""
    )
    assert captured.out == output_text
