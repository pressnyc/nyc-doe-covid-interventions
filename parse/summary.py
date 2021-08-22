#/usr/bin/python3

import json
import csv
from git import Repo

repo = Repo('.')


path = "summary.json"


revlist = (
  (commit, (commit.tree / path).data_stream.read())
  for commit in repo.iter_commits('main', paths=path)
)


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
      output = {
        'Date': c['header'][1].replace('<br/>',' '),
        'Classroom Closures, on Date': c['rows'][0][1],
        'Classroom Closures, Cumulative': c['rows'][0][2],
        'Classroom Closures, Currently in effect': c['rows'][0][3],
        'School Investigations, on Date': c['rows'][1][1],
        'School Investigations, Cumulative': c['rows'][1][2],
        'School Investigations, Currently in effect': c['rows'][1][3],
        'School Closures, on Date': c['rows'][2][1],
        'School Closures, Cumulative': c['rows'][2][3],
        'School Closures, Currently in effect': c['rows'][2][3],
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

make_actions_csv(actions, 'csv/actions.csv')


