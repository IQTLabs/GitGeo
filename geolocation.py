"""geolocation functionality"""

from geographies_list import (
    ALL_COUNTRIES,
    CITY_COUNTRY_DICT,
    CODE_COUNTRY_DICT,
    STATE_ABBREV,
    STATE_NAMES,
)


def get_country_from_location(location_string):
    """Return country (Hungary, United States, etc) from user location text

    Args:
        location_string: a text containing user-supplied location

    Return:
        str: a country
    """
    country = "None"
    if location_string is None:
        country = "None"
    else:
        # Loop through different typical separators of city, country, etc.
        for separator in [",", " "]:
            # Check different positions of the token
            for position in [-1, 0]:

                pieces = location_string.split(separator)
                token = pieces[position].strip()

                # Use returns as a way of exiting double loop
                if token in ALL_COUNTRIES:  # pylint: disable=no-else-return
                    return token
                elif token in CITY_COUNTRY_DICT.keys():
                    return CITY_COUNTRY_DICT[token]
                elif token in CODE_COUNTRY_DICT.keys():
                    return CODE_COUNTRY_DICT[token]
                elif token in STATE_NAMES or token in STATE_ABBREV:
                    return "United States"

    # if no matches are found, will return "none"
    return country
