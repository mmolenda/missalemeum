
"""
Iterate through pre populated missal and apply
generic and specific rules in case more than one
day ID appears for the day. The outcome might be:
* commemoration - Day of higher class is the main day,
                  day of lower class is mentioned in the office
* shift - day of higher class displaces day of lower class.
          Displaced day is moved to another date
* displacement - day of higher class displaces day of
                 lower class. Displaced day is abandoned
"""

ruleset = (
    ()
)