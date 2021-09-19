#!/usr/bin/env python3

import csv
from datetime import datetime, timedelta
import re
import sys
from matplotlib import pyplot as plt

# The data in the CSV file is unusable as is, so it has to be parsed. The raw
# data has one row per day, but sometimes more then one row per day (in which
# case we take the first row we find). We then create one data point per week
# with the sum of all the totals for that week.

# First, create a dictionary indexed to the timestamp for each day with the
# value set to the total cases that day. This process also parses the
# date value from the Title field (which will hopefully stay constant).
massagedDailyData = {}

# The title field include a string like "September 23, 2021".
dateMatcher = re.compile('^([A-Za-z]+ [0-9]+, 202[1-9])')
with open("../csv/confirmed-cases-daily.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        # The date is part of the title and has to be parsed out.
        title = row[0]
        # Skip the header
        if title == "Title":
            continue
        title_parts = title.split(':')
        date_part = title_parts[1].strip()
        dateMatch = dateMatcher.match(date_part)
        if dateMatch:
            date_string = dateMatch.group(1)
        else:
            sys.exit("Failed to parse date: {0}".format(date_string))
        date_obj = datetime.strptime(date_string, "%B %d, %Y")
        ts = date_obj.timestamp()
        # We may have the same date twice, in which case take the first one we encounter.
        # That should be the most recent one.
        if not ts in massagedDailyData:
            massagedDailyData[ts] = int(row[1])

# Get a sorted list of the time stamps so, when plotting, we go from earliest
# to latest (the original data goes from latest to earliest).
timestamps = list(massagedDailyData.keys())
timestamps.sort()

# Now we have a dictionary indexed to a real time stamp. Next we have to
# convert that into two lists. One is a list of weeks (identified by the date
# of the Monday starting the week) and the other is a list of total cases for
# that entire week.
week_starting = []
totals = []
currentWeek = None
totalCasesThisWeek = 0
last_weekday = None
current_weekday = None
for ts in timestamps:
    # Convert the current timestamp to a real date object.
    date_obj = datetime.fromtimestamp(ts)

    # Reset the last_weekday variable so we can tell if we have flipped to a
    # new week.
    last_weekday = current_weekday

    # Calculate the current weekday - 0 is monday, 7 is sunday.
    current_weekday = date_obj.weekday()

    # We have to start somewhere. However, if the *beginning* of the data does
    # not fall on a monday, then we'll have a partial week and the total will be
    # artifically low. So, we are going to throw out any initial data that happens
    # before the first monday that data is collected.
    if currentWeek is None:
        if current_weekday != 0:
            # We are at the beginning of the data and it's not a monday. We will throw
            # out this data so we don't start with a partial week.
            continue
        else:
            # This is finally our first monday. Let's begin.
            currentWeek = date_obj
            last_weekday = 0

    # Here check to see if we have flipped from one week to the next week.
    if last_weekday > current_weekday:
        # We have cycled through a week and need to set the data for the
        # previous week and reset our counters.
        week_starting.append(currentWeek.strftime('%Y-%m-%d'))
        totals.append(totalCasesThisWeek)

        totalCasesThisWeek = 0
        currentWeek = date_obj

    totalCasesThisWeek += massagedDailyData[ts]

#print(week_starting)
#print(totals)

plt.plot(week_starting, totals)
plt.title('Total Covid Cases per week')
plt.xlabel('Total for Week Starting on this date')
plt.ylabel('Total confirmed covid cases')
#plt.show()
plt.savefig('output/cases-by-week.png')
