import csv
from datetime import datetime, timedelta
import re
import sys

# The data in the CSV file is unusable as is, so it has to be parsed. The raw
# data has one row per day, but sometimes more then one row per day (in which
# case we take the first row we find). We then create one data point per week
# with the sum of all the totals for that week.

# Create a dict indexed to the monday of the week that the date falls in. This
# is the data we are going to output. The value is the total number of cases
# that week.
weeklyTotals = {}

# Keep a list of seen dates so we don't count the same date twice.
seenDates = []

# The title field include a string like "September 23, 2021". That's the
# creaky way we figure out the date. Here's the regexp to match the
# date.
dateMatcher = re.compile('^([A-Za-z]+ [0-9]+, 202[1-9])')
dateMatcherRange = re.compile('^([A-Za-z]+ [0-9]+, 202[1-9]) - ([A-Za-z]+ [0-9]+, 202[1-9])')
with open("./csv/confirmed-cases-daily.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        # The date is part of the title and has to be parsed out.
        title = row[0]
        # Skip the header
        if title == "Title":
            continue

        date_string = ''
        if ' - ' in title:
          date_part = title.replace('Cumulative Reported Cases: September 08, 2022 - ','').replace(' at 6 PM','')
          dateMatch = dateMatcher.match(date_part)
          if dateMatch:
              date_string = dateMatch.group(1)
          else:
              sys.exit("Failed to parse date from range: {0}".format(date_part))
        else:
          # title format "Confirmed Positive COVID Cases, December 17, 2021 at 6 PM"
          date_part = title.replace('Confirmed Positive COVID Cases, ','').replace(' at 6 PM','')
          dateMatch = dateMatcher.match(date_part)
          if dateMatch:
              date_string = dateMatch.group(1)
          else:
              sys.exit("Failed to parse date: {0}".format(date_string))
        date_obj = datetime.strptime(date_string, "%B %d, %Y")
        # We may have the same date twice, in which case take the first one we encounter.
        # That should be the most recent one.
        if not date_obj in seenDates:
            seenDates.append(date_obj)

            # What's the date of the start of this week?
            weekStart = date_obj - timedelta(days=date_obj.weekday())
            if not weekStart in weeklyTotals:
                weeklyTotals[weekStart] = {
                    'total': 0,
                    'students': 0,
                    'staff': 0
                } 
            weeklyTotals[weekStart]['total'] += int(row[4])
            weeklyTotals[weekStart]['students'] += int(row[5])
            weeklyTotals[weekStart]['staff'] += int(row[6])

# Get a sorted list of the weeks, so when plotting, we go from earliest to
# latest (the original data goes from latest to earliest).
dates = list(weeklyTotals.keys())
dates.sort()

# We are never sure if the last week is complete or not. So we
# always throw it out. It we only show a week the moment we have
# data for the following week.
dates.pop()

# Now we have a dictionary indexed to a weekly date object. Next we have to
# write that out to a csv file.
output_filename = "csv/confirmed-cases-by-week.csv"
with open(output_filename, 'w') as f:
    w = csv.writer(f)
    w.writerow([
        'Week Start', 
        'Week End', 
        'Total', 
        'Students', 
        'Staff'
        ])

    for week_start_date in dates:
        # We have some data prior to school starting. We're going to throw
        # that out so we start on September 13th, the monday that school started.
        chart_start_date = datetime(2021, 9, 13)
        if week_start_date < chart_start_date:
            continue
        week_end_date = week_start_date + timedelta(days=6)
        week_start_pretty = week_start_date.strftime('%Y-%m-%d')
        week_end_pretty = week_end_date.strftime('%Y-%m-%d')
        w.writerow([
            week_start_pretty, 
            week_end_pretty,
            weeklyTotals[week_start_date]['total'],
            weeklyTotals[week_start_date]['students'],
            weeklyTotals[week_start_date]['staff']
        ])



