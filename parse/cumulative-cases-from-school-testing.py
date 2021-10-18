#/usr/bin/python3

import re
import json
from bs4 import BeautifulSoup
import pandas as pd
from git import Repo



path = "testingresults-summary.html"

repo = Repo('.')



seenDates = []

output_array = []



for commit in list(repo.iter_commits('main', paths=path)):
  page_content = (commit.tree / path).data_stream.read()

  soup = BeautifulSoup(page_content, 'lxml')
  date_range = soup.find(id='ComulativeCityWide').find('li').text


  dateMatcher = re.compile('^Date Range: 9/13/2021 through (.*)')
  dateMatch = dateMatcher.match(date_range)
  if dateMatch:
      date_string = dateMatch.group(1)
  else:
      continue


  if not date_string in seenDates:
      seenDates.append(date_string)


      date_range = date_range.replace('Date Range: ','')
      
      div_content = str( soup.find(id='ComulativeCityWide').find('script') )

      matched = re.search('\{"Data":(\[(.*)\])', div_content )

      data = json.loads( matched[1] )

      output = {}
      output['Positive cases identified by school testing'] = date_range
      output.update( data[2] )
      del output['Citywide']

      output_array.append(output)


pd.DataFrame(output_array).to_csv('csv/cumulative-cases-from-school-testing.csv', index=False)
