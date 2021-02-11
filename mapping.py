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

from pypi import extract_github_owner_and_repo
from geolocation import get_country_from_location
from github import get_contributors, get_contributor_location


def make_map(repo):
    """Create a world map of contributor locations.

    Create a chloropleth world map that displays the number of contributors
    per country.

    Args:
        repo - a full GitHub URL

    Returns:
        null
    """
    # generate pandas dataframe of countries and contributor count
    df = get_dataframe_from_repo(repo)

    # add countributor count to world.json
    world_json = add_contributor_count_to_json(df)

    m = folium.Map(location=[0, 0], zoom_start=1.5)

    # this is the heart of the folium chloropleth mapping functionality
    # todo: work on legend binning for easier reading, especially when one country
    # has many more contributors than the others (e.g. USA for psf/requests)
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
        attr="Mapping via Folium. Data from GitGeo.",
    ).add_to(m)

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


def get_dataframe_from_repo(repo):
    """Create pandas dataframe of contributors by country.

    Args:
        repo - a full GitHub URL

    Returns:
        df - a pandas dataframe of contributors by country
    """
    # get contributors
    repo_ending_string = extract_github_owner_and_repo(repo)
    contributors = get_contributors(repo_ending_string)

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

    return df
