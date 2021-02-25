"""geolocation functionality."""

from geographies_list import (
    ALL_COUNTRIES,
    CITY_COUNTRY_DICT,
    CODE_COUNTRY_DICT,
    STATE_ABBREV,
    STATE_NAMES,
    CITY_COUNTRY_STRINGS,
    METRO_AREA_COUNTRY_DICT,
    SPECIAL_CITIES,
)


def levenshteinDistance(s1, s2):
    """Calculate Levenstein edit distance between two arbitary strings.

    from https://stackoverflow.com/questions/2460177/edit-distance-in-python

    Args:
        s1: an arbitrary string
        s2: a second arbitrary string

    Return:
        str: an integer value of how distant the two strings are
    """
    # pylint: disable=invalid-name

    # special cities and countries
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                )
        distances = distances_
    return distances[-1]


def edit_distance_to_world(location):
    """Use Levenstein distance to approximate match to city+country strings.

    Args:
        location_string: a text containing user-supplied location

    Return:
        str: a country
    """
    # pylint: disable=invalid-name

    # special cities and countries
    special_locations_domestic = [
        "US",
        "USA",
        "U.S.A",
        "U.S.",
        "San Francisco",
        "NYC",
        "Bay Area",
        "New York",
        "SF",
    ]
    if location in special_locations_domestic:
        return "United States"
    for locale in special_locations_domestic:
        if locale in location:
            return "United States"

    special_locations_international = ["EU", "Europe", "Earth"]
    if location in special_locations_international:
        return "None"

    all_countries = set(CITY_COUNTRY_STRINGS.values())
    MIN_DIST = 1000
    min_country = None
    for country in all_countries:
        dist = levenshteinDistance(location, country)
        if dist < MIN_DIST:
            MIN_DIST = dist
            min_country = country
    return min_country


def get_country_from_location(location_string):
    """Return country (Hungary, United States, etc) from user location text.

    This function implements an admittedly imprecise text matching method.

    Args:
        location_string: a text containing user-supplied location

    Return:
        str: a country
    """
    # pylint: disable=too-many-return-statements,no-else-return,bad-continuation
    # pylint: disable=consider-iterating-dictionary,too-many-branches

    # TODO: make all checks lowercase
    if location_string is None:
        return "None"

    # sometimes they give an international state or metro area
    if location_string in METRO_AREA_COUNTRY_DICT.keys():
        return METRO_AREA_COUNTRY_DICT[location_string]
    for metro in METRO_AREA_COUNTRY_DICT.keys():
        if location_string in metro:
            return METRO_AREA_COUNTRY_DICT[metro]

    # check if city,country is recognized (global and USA) as major city
    stripped_location = location_string.replace(",", "").replace(
        " ", ""
    )  # remove both commas and spaces
    if stripped_location in CITY_COUNTRY_STRINGS.keys():
        return CITY_COUNTRY_STRINGS[stripped_location]

    # one of the weird cities that has larger North American populatoin than global population
    if location_string in SPECIAL_CITIES.keys():
        return SPECIAL_CITIES[location_string]

    # if not international, likely to be USA: check if ends in a state
    for state in STATE_NAMES:
        if location_string.endswith(state):
            return "United States"
    for state in STATE_ABBREV:
        if location_string.endswith(state):
            return "United States"

    # Loop through different typical separators of city, country, etc.
    for separator in [",", " "]:
        # Check different positions of the token
        for position in [-1, 0]:
            pieces = location_string.split(separator)
            token = pieces[position].strip()

            # Use returns as a way of exiting double loop
            # Mali has a city named San, which messes this up
            if token in CITY_COUNTRY_DICT.keys() and token != "San":
                return CITY_COUNTRY_DICT[token]
            elif token in ALL_COUNTRIES:  # pylint: disable=no-else-return
                return token
            elif token in CODE_COUNTRY_DICT.keys():
                return CODE_COUNTRY_DICT[token]

    return edit_distance_to_world(location_string)
