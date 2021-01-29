"""Geography lists used to map user location text to country"""

import csv

from country_list import countries_for_language

# a list of all countries in the english language
ALL_COUNTRIES = dict(countries_for_language("en")).values()

# static list of all cities mapped to countries
# from https://datahub.io/core/world-cities\
# ignore errors because of many unicode errors.
with open("world_cities.csv", errors="ignore", newline="") as file:
    reader = csv.reader(file)
    city_country_list = list(reader)
    city_country_dict = {}
    # TODO: If a city is in the list twice, the country should be ambiguous.
    for row in city_country_list:
        # key is city (row[0]), value is country (row[1])
        city_country_dict[row[0]] = row[1]

CITY_COUNTRY_DICT = city_country_dict

# todo: Kinga, is the separation of "District of" and "of Columbia" into
# two separate elements a bug? Why or why not?
STATE_NAMES = [
    "Alaska",
    "Alabama",
    "Arkansas",
    "American Samoa",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "District ",  # Kinga?
    "of Columbia",  # Kinga?
    "Delaware",
    "Florida",
    "Georgia",
    "Guam",
    "Hawaii",
    "Iowa",
    "Idaho",
    "Illinois",
    "Indiana",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Massachusetts",
    "Maryland",
    "Maine",
    "Michigan",
    "Minnesota",
    "Missouri",
    "Mississippi",
    "Montana",
    "North Carolina",
    "North Dakota",
    "Nebraska",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "Nevada",
    "New York",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Puerto Rico",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Virgin Islands",
    "Vermont",
    "Washington",
    "Wisconsin",
    "West Virginia",
    "Wyoming",
]

STATE_ABBREV = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DC",
    "D.C.",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]
