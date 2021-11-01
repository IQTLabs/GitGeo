"""Create chloropleth map using count of contributors by country."""

# for helpful starter code, see:
# https://coderzcolumn.com/tutorials/data-science/interactive-maps-choropleth-scattermap-using-folium

# pylint: disable=invalid-name

from collections import Counter
import json
import os
import time

import folium
import pandas as pd

from gitgeo.geolocation import get_country_from_location
from gitgeo.github import get_contributors, get_contributor_location
from gitgeo.pypi import extract_github_owner_and_repo


def make_map(repo=None, csv=None, num=100):
    """Create a world map of contributor locations.

    Create a chloropleth world map that displays the number of contributors
    per country.

    Args:
        repo - a full GitHub URL
        csv - a filename of a csv in the results folder
        num - number of contributors to analyze per repo

    Returns:
        null
    """
    # pylint: disable=bad-continuation
    # generate pandas dataframe of countries and contributor count
    # if input is repo, create dataframe from repo from scatch
    if repo:
        df, total_num_of_contributors = get_dataframe_from_repo(repo, num)
        title = repo
    # if input is a csv, create dataframe from csv
    elif csv:
        df, total_num_of_contributors = get_dataframe_from_csv(csv)
        title = csv

    # add countributor count to world.json
    world_json = add_contributor_count_to_json(df)

    m = folium.Map(location=[0, 0], zoom_start=1.5)

    # calculate the highest number of contributors for a country and then
    # set the variable to be appropriate for the upper end of the map legend
    max_contributors = df.contributor_count.max()
    if max_contributors < 100:
        max_contributors = 100

    # this is the heart of the folium chloropleth mapping functionality
    chloropleth = folium.Choropleth(
        geo_data=world_json,
        name="choropleth",
        data=df,
        columns=["country", "contributor_count"],
        key_on="feature.properties.sovereignt",
        fill_color="BuGn",  # choose color schemes here: https://colorbrewer2.org
        fill_opacity=0.7,
        line_opacity=0.5,
        nan_fill_color="white",  # set countries with no data to white background
        legend_name="Contributor Count",
        highlight=True,  # highlight country borders on mouseover
        bins=[1, 5, 20, max_contributors + 1],  # legend bins
        attr="Mapping via Folium. Data from GitGeo.",
    ).add_to(m)

    # add title to map and also number of contributors with no location
    num_contributors_no_location = df[df.country == "None"].contributor_count.values[0]
    title_html = """
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             """.format(
        "Top {} Contributors to {}<br>Number of contributors with no location: {}".format(
            total_num_of_contributors, title, num_contributors_no_location
        )
    )
    m.get_root().html.add_child(folium.Element(title_html))

    # tooltip to display data country by country
    chloropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ["sovereignt", "contributor_count"], labels=False
        )
    )

    # add ability to turn layers on and off
    folium.LayerControl().add_to(m)

    # save with cross-platform, timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    map_filename = os.path.join("results", "map" + "_" + timestamp + ".html")
    m.save(map_filename)


def add_contributor_count_to_json(df):
    """Create world json with a contributor count field.

    To compensate for inability of folium chloropleth to access the dataframe
    fields, add contributor count from dataframe into the json file with
    geographic information. This way the tooltip feature can access the
    contributor count from the json, not the pandas dataframe.

    Args:
        df - a dataframe

    Returns:
        json_data - a json objecet containing a contributor_count field
    """
    with open("world.json") as original_json_file:
        # load json file into an object
        data = json.load(original_json_file)
        for obj in data["features"]:
            # check if country is in dataframe
            country = obj["properties"]["sovereignt"]
            is_country_in_dataframe = country in df["country"].unique()
            if is_country_in_dataframe:
                # extract number of contributors associated with particular country
                # extract value from series and convert to int
                contributor_count = int(
                    df[df.country == country].contributor_count.values[0]
                )
                obj["properties"]["contributor_count"] = contributor_count
            else:
                # if country not in contributors data frame, this means the
                # country had zero contributors
                obj["properties"]["contributor_count"] = 0

        # convert data to json object
        json_data = json.dumps(data)
        return json_data


def get_dataframe_from_repo(repo, num=100):
    """Create pandas dataframe of contributors by country.

    Args:
        repo - a full GitHub repo URL
        num - number of contributors to analyze per repo

    Returns:
        df - a pandas dataframe of contributors by country
        num_contributors - total number of contributors
    """
    # get contributors
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string, num)
    num_contributors = len(contributors)

    # get count of countries
    country_list = []
    for contributor in contributors:
        location = get_contributor_location(contributor)
        country = get_country_from_location(location)
        country_list.append(country)
    country_counter = Counter(country_list)

    # convert counter to pandas dataframe
    df = pd.DataFrame.from_records(
        country_counter.most_common(), columns=["country", "contributor_count"]
    )

    return df, num_contributors


def get_dataframe_from_csv(filename):
    """Create pandas dataframe of contributors by country.

    Read in a csv from the results folder and convert to a dataframe
    that tabluates developer count by country.

    Args:
        filename - filename to input

    Returns:
        aggregated_df - a pandas dataframe of contributors by country
        num_contributors - total number of contributors
    """
    # file must be in the results folder
    df = pd.read_csv(os.path.join("results", filename))
    num_contributors = len(df)

    # create by-country count dict and then convert to pandas dataframe
    country_dict = df["country"].value_counts().to_dict()
    aggregated_df = pd.DataFrame.from_dict(
        country_dict, orient="index", columns=["contributor_count"]
    )

    # to ensure compatiblity with the dataframe structure created by
    # get_dataframe_from_repo, do a few minor changes to dataframe
    aggregated_df["country"] = aggregated_df.index
    aggregated_df = aggregated_df.reset_index(drop=True)
    aggregated_df = aggregated_df[["country", "contributor_count"]]

    return aggregated_df, num_contributors
