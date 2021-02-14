"""Unit tests and integration tests for GitGeo."""

# pylint: disable=no-self-use, too-many-locals

import csv
import glob
import os
import textwrap

import pandas as pd
import pytest

from custom_csv import create_csv, add_committer_to_csv
from geolocation import get_country_from_location
from github import get_contributors, get_contributor_location
from main import scan_single_package, scan_single_repo
from mapping import get_dataframe_from_repo, add_contributor_count_to_json, make_map
from multi_repo_scan import scan_multiple_repos
from printers import print_by_contributor, print_by_country
from pypi import get_pypi_data, extract_github_owner_and_repo


class TestPypiFunctionality:  # pragma: no cover
    """Unit tests related to PyPI functionality."""

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


class TestGitHubFunctionality:  # pragma: no cover
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
        assert get_country_from_location("Philadelphia, PA") == "United States"

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

    @pytest.mark.xfail  # known bug, unknown origin
    def test_get_country_from_location_dataset_pull_geographies(self):
        assert get_country_from_location("EU") == "Europe"
        assert get_country_from_location("Canary Islands") == "Canary Islands"
        assert get_country_from_location("waterloo") == "United Kingdom"
        assert get_country_from_location("Earth") == "None"
        assert get_country_from_location("Australia, Victoria") == "Australia"
        assert get_country_from_location("Europe/Berlin") == "Germany"
        assert get_country_from_location("York") == "United Kingdom"
        assert get_country_from_location("M√ºnchen") == "Germany"
        assert get_country_from_location("Amsterdam") == "Netherlands"
        assert get_country_from_location("Sydney") == "Australia"
        assert get_country_from_location("Saclay") == "France"
        assert get_country_from_location("Montreal, CA") == "Canada"
        assert get_country_from_location("NYC") == "United States"
        assert get_country_from_location("Florian√≥polis") == "Brazil"
        assert get_country_from_location("Bay Area") == "United States"
        assert get_country_from_location("Montr√©al") == "Canada"
        assert get_country_from_location("Warszawa") == "Poland"
        assert get_country_from_location("Bangalore") == "India"
        assert get_country_from_location("Amsterdam, The Netherlands") == "Netherlands"
        assert get_country_from_location("Perth, Western Australia") == "Australia"
        assert get_country_from_location("Oxford") == "United Kingdom"
        assert get_country_from_location("Barcelona") == "Spain"
        assert get_country_from_location("Kerala") == "India"
        assert get_country_from_location("S√£o Paulo") == "Brazil"
        assert get_country_from_location("Jiangxi") == "China"
        assert get_country_from_location("Kyiv") == "Ukraine"
        assert get_country_from_location("N.H.") == "United States"
        assert get_country_from_location("Vancouver, BC") == "Canada"
        assert get_country_from_location("Hyderabad") == "India"
        assert get_country_from_location("Sri-City, Andhra Pradesh") == "India"
        assert (
            get_country_from_location("roudnice nad labem, czech republic")
            == "Czech Republic"
        )
        assert get_country_from_location("Scotland") == "United Kingdom"
        assert get_country_from_location("New York") == "United States"
        assert get_country_from_location("Geneva") == "Switzerland"
        assert get_country_from_location("Vancouver") == "Canada"
        assert get_country_from_location("Berlin/Florence") == "Germany"
        assert get_country_from_location("Rotterdam, the Netherlands") == "Netherlands"
        assert get_country_from_location("Milan") == "Italy"
        assert get_country_from_location("Republic of Korea") == "South Korea"
        assert get_country_from_location("Bras√≠lia, Brazil.") == "Brazil"
        assert get_country_from_location("beijing") == "China"
        assert get_country_from_location("Greater Seattle Area") == "United States"
        assert get_country_from_location("Barcelona") == "Spain"
        assert get_country_from_location("Z√ºrich") == "Switzerland"
        assert get_country_from_location("Flanders, Europe, Earth") == "Belgium"
        assert get_country_from_location("Kitchener, Ontario") == "Canada"
        assert get_country_from_location("Athens") == "Greece"
        assert get_country_from_location("Saint Petersburg") == "Russia"
        assert get_country_from_location("England") == "United Kingdom"
        assert get_country_from_location("Montr√©al, QC") == "Canada"
        assert get_country_from_location("Europe") == "None"
        assert get_country_from_location("Lima") == "Peru"
        assert get_country_from_location("Glasgow, Scotland") == "United Kingdom"
        assert (
            get_country_from_location("28 rue du Dr Roux 75015 Paris, FRANCE")
            == "France"
        )
        assert get_country_from_location("Bay Area") == "United States"
        assert get_country_from_location("Krak√≥w") == "Poland"
        assert get_country_from_location("ƒ∞stanbul") == "Turkey"
        assert get_country_from_location("San Francisco") == "United States"
        assert get_country_from_location("Russian Federation") == "Russia"
        assert get_country_from_location("Newcastle, NSW") == "Australia"
        assert get_country_from_location("Wroc≈Çaw") == "Poland"
        assert get_country_from_location("Gda≈Ñsk") == "Poland"
        assert get_country_from_location("SF") == "United States"

    def test_extract_github_owner_and_repo(self):
        """Unit test for extract_github_owner_and_repo()."""
        owner_and_repo = extract_github_owner_and_repo("www.github.com/psf/requests")
        assert owner_and_repo == "psf/requests"


class TestCsvFunctionality:  # pragma: no cover
    """Unit tests related to CSV functionality"""

    def test_create_csv(self):
        """Unit test for create_csv()."""
        create_csv("contributors", "1")
        assert os.path.exists(os.path.join("results", "contributors_1.csv"))

    def test_add_committer_to_csv(self):
        """Unit test fpr add_co0mmitter_to_csv."""
        add_committer_to_csv(
            "contributors", "test", "1", "googlemoogle", "eschmidt", "innovation-island"
        )
        os.remove(os.path.join("results", "contributors_1.csv"))  # remove file


class TestMultiRepoScan:  # pragma: no cover
    """Tests related to multi-repo scanning capability."""

    # pylint: disable=too-few-public-methods

    def test_multi_repo_scan(self):
        """Unit test for scan_multiple_repos()."""
        scan_multiple_repos("test_repos.txt")
        # identify file created for test
        files = glob.glob("results/*.csv")
        test_file = max(files, key=os.path.getctime)
        # check that csv rows are as expected
        with open(test_file, newline="") as test_output:
            for index, row in enumerate(csv.reader(test_output)):
                if index == 0:
                    assert row == ["software_name", "username", "location", "country"]
                elif index == 1:
                    assert row == [
                        "jspeed-meyers_pcap2map",
                        "jspeed-meyers",
                        "",
                        "None",
                    ]
                elif index == 4:
                    assert row == [
                        "iqtlabs_portunus",
                        "anarkiwi",
                        "Wellington, New Zealand",
                        "New Zealand",
                    ]
        os.remove(test_file)


class TestMapping:
    """Tests related to mapping capability."""

    # pylint: disable=invalid-name

    def test_get_dataframe_from_repo(self):
        """Unit test for get_dataframe_from_repo()."""
        output = get_dataframe_from_repo("www.github.com/iqtlabs/gitgeo")
        expected_ouput = pd.DataFrame(
            {"country": ["None", "Portugal"], "contributor_count": [3, 1]}
        )
        assert output.equals(expected_ouput)

    def test_add_contributor_count_to_json(self):
        """Unit test for add_contributor_count_to_json()."""
        df = pd.DataFrame(
            {"country": ["None", "Portugal"], "contributor_count": [3, 1]}
        )
        output = add_contributor_count_to_json(df)
        assert isinstance(output, str)

    def test_make_map(self):
        """Unit test for make_map() with a number greater than 100 of contributors."""
        make_map("www.github.com/iqtlabs/gitgeo", 200)
        # identify and delete map file created for test
        files = glob.glob("results/*.html")
        test_file = max(files, key=os.path.getctime)
        os.remove(test_file)


def test_print_by_contributor_repo(capsys):
    """Unit test for print by contributors for GitHub repo."""
    repo = "jspeed-meyers/pcap2map"
    contributors = get_contributors(repo)
    print_by_contributor(repo, contributors)
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
    print_by_contributor(pkg, contributors, pypi_data=pypi_data)
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
        Hax7 | Palestine | Palestine
        paulgowdy | Menlo Park CA | United States\n"""
    )
    assert captured.out == output_text


def test_print_by_country(capsys):
    """Unit test for print_by_country() for networml python package."""
    repo = "https://www.github.com/iqtlabs/networkml"
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string)
    print_by_country(contributors)
    captured = capsys.readouterr()  # capture output printed to date
    # dedent removes spacing, using the spacing width from the first line
    output_text = textwrap.dedent(
        """        COUNTRY | # OF CONTRIBUTORS
        ---------------------------
        None 10
        United States 4
        New Zealand 2
        Palestine 1\n"""
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


@pytest.mark.xfail  # known bug, unknown origin
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
        None 10
        United States 4
        New Zealand 2
        Palestine 1\n"""
    )
    assert captured.out == output_text


@pytest.mark.xfail  # known bug, likely with capsys and pytest, test fails in actions
def test_scan_single_repo_no_summary(capsys):
    """Integration test for scan_single_repo with no summary."""
    repo = "https://www.github.com/jspeed-meyers/pcap2map"
    scan_single_repo(repo, summary=False, output_csv=False)
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
    scan_single_repo(repo, summary=True, output_csv=False)
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
