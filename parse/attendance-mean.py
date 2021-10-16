#/usr/bin/python3

import datetime
import io   
import csv
from git import Repo
import re
import pandas as pd


repo = Repo('.')

path = "csv/daily-attendance.csv"

output_filename = "csv/daily-attendance-mean.csv"

output = {}

for commit in list(repo.iter_commits('main', paths=path)):
  data = (commit.tree / path).data_stream.read().decode('ascii')
  df = pd.read_csv(io.StringIO(data))
  
  date_string = df['ATTD DATE'][0]
  df = df.apply(pd.to_numeric, errors='coerce')
  mean_attendance = df['%ATTD'].mean()

  if date_string in output:
    if output[date_string] < mean_attendance:
        output[date_string] = mean_attendance
  else:
    output[date_string] = mean_attendance


with open(output_filename, 'w') as f:
    w = csv.writer(f)
    w.writerow(['Date', 'Attendance'])

    output_list = []
    for c in output:
      output_list.append([ c, output[c] ])
    
    w.writerows(output_list)
