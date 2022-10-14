#/usr/bin/python3

import json
import datetime
import csv
from git import Repo
import re
import pandas as pd

# The title field include a string like "September 23, 2021". That's the
# creaky way we figure out the date. Here's the regexp to match the
# date.
dateMatcher = re.compile('^([A-Za-z]+ [0-9]+, 202[1-9])')

repo = Repo('.')


path = "summary.json"



revlist = []
years = []

# Only record one set of data per calendar day by tracking the
# days we've seen already.
seen = []

for commit in list(repo.iter_commits('main', paths=path)):
  data = (commit.tree / path).data_stream.read()
  j = json.loads(data)
  title = j[0]['title']
  title_parts = title.split(':')
  date_part = title_parts[1].strip()
  dateMatch = dateMatcher.match(date_part)
  if dateMatch:
    date_string = dateMatch.group(1)
  else:
      print("Failed to parse time from {0}".format(title))
      continue
  dt = datetime.datetime.strptime(date_string, "%B %d, %Y")
  # We are iterating in reverse chronological order, so we should
  # get the most recent date first. All following dates should be
  # ignore becaues they are less up-to-date.
  if date_string in seen:
      print("Continuing on {0}".format(dt))
      continue

  revlist.append(j)
  years.append(dt.year)
  seen.append(date_string)

confirmed = []
cumulative = []
actions = []
charter = []

for j in revlist:
  confirmed.append(j[0]) # first child
  cumulative.append(j[1]) # second child
  try:
    actions.append(j[2]) # third child
  except:
    pass
  try:
    charter.append(j[3])
  except:
    pass



def make_csv(data, output_filename):

    output_array = []

    for c in data:
      output = {
        'Title': c['title'],
        c['header'][0]: c['rows'][0][0],
        c['header'][1]: c['rows'][0][1],
        c['header'][2]: c['rows'][0][2],
      }
      output_array.append(output)

    data_file = open(output_filename, 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for o in output_array:
        if count == 0: 
            header = o.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(o.values()) 
    data_file.close()

make_csv(cumulative, 'csv/confirmed-cases-cumulative.csv')



def make_daily_from_cumulative(data, output_filename):

    output_array = []
    
    previous_title = None;

    previous_total = 0;
    previous_students = 0;
    previous_staff = 0;
    current_total = 0;
    current_students = 0;
    current_staff = 0;

    for c in data:
        
      c['title'] = c['title'].replace('Confirmed Cumulative Positive COVID Cases: September 13, 2021 - ','Confirmed Positive COVID Cases, ')
      c['title'] = c['title'].replace('Confirmed Cumulative Positive COVID Cases: September 14, 2020 - ','Confirmed Positive COVID Cases, ')
      c['title'] = c['title'].replace('Cumulative Reported Cases: September 13, 2021 - ','Confirmed Positive COVID Cases, ')
      c['title'] = c['title'].replace('Cumulative Reported Cases: September 08, 2022 - ','Confirmed Positive COVID Cases, ')

      current_total = previous_total - int(c['rows'][0][0].replace(',', ''))
      current_students = previous_students - int(c['rows'][0][1].replace(',', ''))
      current_staff = previous_staff - int(c['rows'][0][2].replace(',', ''))
    
      if current_total == 0 and current_students == 0 and current_staff == 0: continue
    
      if current_total < 0:
         current_total = previous_total
         current_students = previous_students
         current_staff = previous_staff
    
      if previous_title:
          output = {
            'Title': previous_title,
            'Cumulative ' + c['header'][0]: previous_total,
            'Cumulative ' + c['header'][1]: previous_students,
            'Cumulative ' + c['header'][2]: previous_staff,
            c['header'][0]: current_total,
            c['header'][1]: current_students,
            c['header'][2]: current_staff,
          }
          output_array.append(output)

      previous_title =  c['title']
      previous_total = int(c['rows'][0][0].replace(',', ''))
      previous_students = int(c['rows'][0][1].replace(',', ''))
      previous_staff = int(c['rows'][0][2].replace(',', ''))
      
    # end for
    
    data_file = open(output_filename, 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for o in output_array:
        if count == 0: 
            header = o.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(o.values()) 
    data_file.close()

make_daily_from_cumulative(cumulative, 'csv/confirmed-cases-daily.csv')




def make_actions_csv(data, output_filename):

    output_array = []

    for c in data:
      output = {}

      for row in c['rows']:
        for i in range(len(row)):
        
          date = c['header'][1].replace('<br/>',' ').replace(' as of 6 PM','')
          date = date + '/' + str( years[data.index(c)] )

          if i == 0:          
            output['Date'] = date
          elif i == 1:          
            output[ row[0] ] = row[i] 
          else:
            header = c['header'][i].replace('<br/>',' ')
            header = header.replace('(since 9/14)','(since 9/14/2020)')
            header = header.replace('(since 9/13)','(since 9/13/2021)')
            output[ row[0] + ', ' + header ] = row[i] 
            
      output_array.append(output)

    df = pd.DataFrame(output_array)
    df.to_csv(output_filename, index = None, encoding='utf-8')

make_actions_csv(actions, 'csv/actions.csv')
make_actions_csv(charter, 'csv/actions-charter.csv')


