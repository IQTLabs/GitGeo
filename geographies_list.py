"""Geography lists used to map user location text to country"""

from country_list import countries_for_language

# a list of all countries in the english language
ALL_COUNTRIES = dict(countries_for_language("en")).values()

#todo: Kinga, is the separation of "District of" and "of Columbia" into
# two separate elements a bug? Why or why not?
STATE_NAMES = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona",
               "California", "Colorado", "Connecticut", "District ", "of Columbia",
               "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", 
               "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
               "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota",
               "Missouri", "Mississippi", "Montana", "North Carolina",
               "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
               "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", 
               "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina",
               "South Dakota", "Tennessee", "Texas", "Utah", "Virginia",
               "Virgin Islands", "Vermont", "Washington", "Wisconsin",
               "West Virginia", "Wyoming"]

STATE_ABBREV = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
