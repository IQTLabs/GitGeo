"""Geography lists used to map user location text to country."""

import csv
from pathlib import Path

# static list of all cities mapped to countries
# from https://datahub.io/core/world-cities\
# ignore errors because of many unicode errors.
with open(Path(__file__).with_name("world_cities.csv"), errors="ignore", newline="") as file:
    reader = csv.reader(file)
    city_country_list = list(reader)
    city_country_dict = {}
    metro_area_country_dict = {}
    # TODO: If a city is in the list twice, the country should be ambiguous.
    for row in city_country_list:
        # key is city (row[0]), value is country (row[1])
        city_country_dict[row[0]] = row[1]
        # key is metro location (row[2]), value is country (row[1])
        metro_area_country_dict[row[2]] = row[1]

city_country_dict['British Columbia'] = 'Canada'
city_country_dict['Ontario'] = 'Canada'
city_country_dict['Quebec'] = 'Canada'
city_country_dict['Manitoba'] = 'Canada'
city_country_dict['Alberta'] = 'Canada'
city_country_dict['New Brunswick'] = 'Canada'
city_country_dict['Nova Scotia'] = 'Canada'
city_country_dict['Nsw'] = 'Australia'
city_country_dict['Qld'] = 'Australia'
city_country_dict['New South Wales'] = 'Australia'
city_country_dict['Queensland'] = 'Australia'
city_country_dict['South Australia'] = 'Australia'
city_country_dict['Tasmania'] = 'Australia'
city_country_dict['Victoria'] = 'Australia'
city_country_dict['Western Australia'] = 'Australia'

CITY_COUNTRY_DICT = city_country_dict
METRO_AREA_COUNTRY_DICT = metro_area_country_dict

# list of country codes
with open(Path(__file__).with_name("country_codes.csv"), errors="ignore", newline="") as file:
    reader = csv.reader(file)
    code_country_list = list(reader)
    code_country_dict = {}
    country_code_dict = {}
    for row in code_country_list:
        # key is country code (row[1]), value is country (row[0])
        code_country_dict[row[1]] = row[0]
        # key is country (row[0]), value is country code (row[1])
        country_code_dict[row[0]] = row[1]


CODE_COUNTRY_DICT = code_country_dict
# we create the "inverse" of the other dict to use below to create pre-processed potentials mashups
# of city,country and city,country_code to make matching stronger against user inputs
COUNTRY_CODE_DICT = country_code_dict

# a list of all countries in the english language
ALL_COUNTRIES = [
    "Afghanistan",
    "Åland Islands",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua & Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia",
    "Bosnia & Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory",
    "British Virgin Islands",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Caribbean Netherlands",
    "Cayman Islands",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands",
    "Colombia",
    "Comoros",
    "Congo - Brazzaville",
    "Congo - Kinshasa",
    "Cook Islands",
    "Costa Rica",
    "Côte d’Ivoire",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Falkland Islands",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories",
    "Gabon",
    "Gambia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard & McDonald Islands",
    "Honduras",
    "Hong Kong SAR China",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao SAR China",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar (Burma)",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "North Korea",
    "North Macedonia",
    "Northern Mariana Islands",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestinian Territories",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Pitcairn Islands",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Réunion",
    "Romania",
    "Russia",
    "Rwanda",
    "Samoa",
    "San Marino",
    "São Tomé & Príncipe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia & South Sandwich Islands",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "St. Barthélemy",
    "St. Helena",
    "St. Kitts & Nevis",
    "St. Lucia",
    "St. Martin",
    "St. Pierre & Miquelon",
    "St. Vincent & Grenadines",
    "Sudan",
    "Suriname",
    "Svalbard & Jan Mayen",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad & Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks & Caicos Islands",
    "Tuvalu",
    "U.S. Outlying Islands",
    "U.S. Virgin Islands",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Wallis & Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

STATE_NAMES = [
    "Alaska",
    "Alabama",
    "Arkansas",
    "American Samoa",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "District of Columbia",
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
    "Washington, DC",
    "Washington, D.C.",
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

# some major cities have smaller populations than North American cities, but I suspect the people that
# live in the latter know not to use their city name. See Sydney in Nova Scotia vs Syndey Austratial

SPECIAL_CITIES = {
    'Sydney':'Australia',
    'Amsterdam':'Netherlands',
    'Barcelona':'Spain',
    'Hyderabad':'India',
    'Vancouver':'Canada',
    'Saint Petersburg':'Russia',
    'England':'United Kingdom',
    'Athens':'Greece',
    'Lima':'Peru',
    'Scotland':'United Kingdom',
    'Rome':'Italy',
    'Dublin':'Ireland',
    'Edinburgh':'United Kingdom',
    'Bangalore':'India',
    'Geneva':'Switzerland',
    'Melbourne':'Australia',
    'Bruges':'Belgium',
    'PRC':'China',
    'York':'United Kingdom',
    'Valenica':'Spain',
    'Republic of Korea':'South Korea',
    'Waterloo':'United Kingdom',
    'M√ºnchen':'Germany',
    'Montreal, CA':'Canada',
    'Florian√≥polis':'Brazil',
    'Perth':'Australia',
    'Oxford':'United Kingdom',
    'Milan':'Italy',
    'Russian Federation':'Russia'
}

# mashes together the common cities and countries/codes in a stable format,
# so it's easier for us to try this match first
CITY_COUNTRY_STRINGS = {}
# Add ignore errors to deal with strange characters on windows machine
with open(Path(__file__).with_name("world_cities.csv"), errors="ignore") as file:
    # pylint: disable=bad-continuation
    data = file.readlines()
    for line in csv.reader(
        data, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
    ):
        city = line[0]
        country = line[1]
        location = (city + country).replace(",", "").replace(" ", "")
        CITY_COUNTRY_STRINGS[location] = country

        # in addition to generating city,country->country entries above, let's also generate
        # city,country_code->country entries in another dict below
        if country in COUNTRY_CODE_DICT.keys():
            CITY_COUNTRY_STRINGS[
                (city + COUNTRY_CODE_DICT[country]).replace(",", "").replace(" ", "")
            ] = country
