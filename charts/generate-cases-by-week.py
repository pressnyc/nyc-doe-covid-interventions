import csv
from datetime import datetime, timedelta
import re
import sys
from matplotlib import pyplot as plt

# The data in the CSV file is unusable as is, so it has to be parsed. The raw
# data has one row per day, but sometimes more then one row per day (in which
# case we take the first row we find). We then create one data point per week
# with the sum of all the totals for that week.

# Create a dict indexed to the monday of the week that the date falls in. This
# is the data we are going to chart. The value is the total number of cases
# that week.
weeklyTotals = {}

# Keep a list of seen dates so we don't count the same date twice.
seenDates = []

# The title field include a string like "September 23, 2021". That's the
# creaky way we figure out the date. Here's the regexp to match the
# date.
dateMatcher = re.compile('^([A-Za-z]+ [0-9]+, 202[1-9])')
with open("./csv/confirmed-cases-daily.csv") as csvDataFile:
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
            weeklyTotals[weekStart]['total'] += int(row[1])
            weeklyTotals[weekStart]['students'] += int(row[2])
            weeklyTotals[weekStart]['staff'] += int(row[3])

# Get a sorted list of the weeks, so when plotting, we go from earliest to
# latest (the original data goes from latest to earliest).
dates = list(weeklyTotals.keys())
dates.sort()

# We are never sure if the last week is complete or not. So we
# always throw it out. It we only show a week the moment we have
# data for the following week.
dates.pop()

# Now we have a dictionary indexed to a weekly date object. Next we have to
# convert that into two lists. One is a list of weeks (identified by the date
# of the Monday starting the week) and the other is a list of total cases for
# that entire week.
week_starting = []
total = []
students = []
staff = []
for week_start_date in dates:
    # We have some data prior to school starting. We're going to throw
    # that out so we start on September 13th, the monday that school started.
    chart_start_date = datetime(2021, 9, 13)
    if week_start_date < chart_start_date:
        continue
    week_end = week_start_date + timedelta(days=6)
    week_starting.append("{0} to {1}".format(week_start_date.strftime('%b %d'), week_end.strftime("%b %d, %Y")))
    total.append(weeklyTotals[week_start_date]['total'])
    students.append(weeklyTotals[week_start_date]['students'])
    staff.append(weeklyTotals[week_start_date]['staff'])

plt.plot(week_starting, total, label="Total cases")
plt.plot(week_starting, students, label="Students")
plt.plot(week_starting, staff, label="Staff")
plt.title('Covid Cases per week')
plt.xlabel('Date')
plt.ylabel('Confirmed covid cases')
plt.legend()
#plt.show()
plt.savefig('./charts/output/cases-by-week.png')

plt.close()
plt.bar(week_starting, students, label="Students")
plt.bar(week_starting, staff, label="Staff")
plt.title('Covid Cases per week')
plt.xlabel('Date')
plt.ylabel('Confirmed covid cases')
plt.legend()
#plt.show()
plt.savefig('./charts/output/cases-by-week.bar.png')

plt.close()
plt.bar(week_starting, students, label="Students")
plt.title('Student covid cases per week')
plt.xlabel('Date')
plt.ylabel('Confirmed student covid cases')
#plt.show()
plt.savefig('./charts/output/cases-by-week.bar.student.png')

plt.close()
plt.bar(week_starting, staff, label="Staff")
plt.title('Staff covid cases per week')
plt.xlabel('Date')
plt.ylabel('Confirmed student covid cases')
#plt.show()
plt.savefig('./charts/output/cases-by-week.bar.staff.png')

