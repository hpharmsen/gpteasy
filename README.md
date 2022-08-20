# Justdays

Package to make working with days and ranges of days in Python super easy.

The package contains two classes: \
**Day** handles everything you want to do with days. \
**Period** handles a range of Day objects.

Current version: 1.5.4

## Installation
~~~~bash
python -m pip install justdays
~~~~

## Day class usage

### Initializing a Day
~~~~python
day = Day()  # No arguments, initalize with the current day
day = Day('2022-08-16')  # One argument, string in YYYY-MM-DD format
day = Day(2022, 32)  # Two arguments: year, week. Day with be the Monday of that week
day = Day(2022, 8, 16)  # Three arguments: year, month, day. 
day = Day(datetime(2022, 8, 16))  # Initialize with Python datetime object
day = Day(date(2022, 8, 16))  # Initialize with Python date object
~~~~

### Accessing Day fiels
~~~~python
d = day.d  # int
m = day.m  # int
y = day.y  # int
as_sting = day.str  # in YYYY-MM-DD format
~~~~

### Represenation
~~~~python
str(day) # Returns the day in YYYY-MM-DD format
day.as_datetime() # Returns the day as a Python datetime object
day.as_date() # Returns the day as a Python date object
day.strftime(format_string) # Returns the day as a string formatted according to the format string
day.as_unix_timestamp() # Returns the day as a unix timestamp (int)
~~~~

### Days further away or in the past
~~~~python
day.next()  # Next day
day.previous()  # Previous day
day.next_weekday()  # Next day that is on a weekday
day.plus_days(3)  # Add 3 days to the day
day.plus_days(-3)  # Subtract 3 days from the day
day.plus_weeks(1)  # Add 1 week to the day
day.plus_months(1)  # Add 1 month to the day
~~~~


### Comparing days
~~~~python
day1 = Day('2022-08-16')
day2 = Day('2022-08-20')
day2 > day1  # Returns True if day2 is after day1
day2 == day1  # Returns True if day2 is the same day as day1
days_difference = day2 - day 1  # Returns the difference in days between two days (4)
~~~~

### Miscellaneous
~~~~python
day.is_weekend()  # Returns True if the day is a weekend
day.is_weekday()  # Returns True if the day is a weekday
day.day_of_week()  # Returns the day of the week as an integer (0 = Monday, 6 = Sunday)
day.day_of_year()  # Returns the day of the year as an integer (1 = 1st of January, 365 = 31st of December in a non leap year)
day.fraction_of_the_year_past()  # Returns the fraction of the year that has passed (0.0 = 1st of January, 1.0 = 31st of December)
day.week_number()  # Returns the week number of the year (1 = first week of the year, 52 = last week of the year)
day.last_monday()  # Returns the last day that was a Monday or the day itself if it is a Monday
day.last_day_of_month()  # Returns the last day of the month of the day
~~~~


## Period class usage
Period is just a day range. Either fromday or untilday can be left to None

### Initializing a Period
~~~~python
period = Period(day1, day2)  # Period ranging from day1 (included) until day2 (not included)
period = Period(day1)  # One argument: fromday. Untilday is left open
period = Period('2022-08-16', '2022-08-20')  # Period can be initialized with strings in YYYY-MM-DD format
~~~~

### Accessing Period fields
~~~~python
fromday = period.fromday
untilday = period.untilday
length = len(period)
~~~~



### Iterating over a Period
~~~~python
for day in period:
    print(day)
~~~~

### Checking if a Day falls within a Period
~~~~python
if day in period:
    print('yes!')
~~~~
