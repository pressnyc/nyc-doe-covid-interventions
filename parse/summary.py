#/usr/bin/python3

import json
import datetime
import csv
from git import Repo

import pandas as pd

repo = Repo('.')


path = "summary.json"



revlist = []
years = []

for commit in list(repo.iter_commits('main', paths=path)):
  dt = datetime.datetime.fromtimestamp(commit.committed_date)
  years.append(dt.year)
  revlist.append( (commit.tree / path).data_stream.read() )


confirmed = []
cumulative = []
actions = []

for filecontents in revlist:
  j = json.loads(filecontents)
  confirmed.append(j[0])
  cumulative.append(j[1])
  actions.append(j[2])




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
make_csv(confirmed, 'csv/confirmed-cases-daily.csv')




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


