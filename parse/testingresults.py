import math
import requests
import pandas as pd

pageSize = 50

testing_data = []

sess = requests.Session()
data = {'sort':'','page':'1','pageSize':pageSize,'group':'','filter':'','SelectedLocation':'','SelectedBorough':''}
page_results = sess.post("https://testingresults.schools.nyc/surveytesting/get", data=data)
page_json = page_results.json()
testing_data = page_json['Data']

total = page_json['Total']

num_pages = int(math.ceil(total/pageSize)) + 1
    
for page in range(2, num_pages):
  data = {'sort':'','page':page,'pageSize':pageSize,'group':'','filter':'','SelectedLocation':'','SelectedBorough':''}
  page_results = sess.post("https://testingresults.schools.nyc/surveytesting/get", data=data)
  page_json = page_results.json()
  testing_data = testing_data + page_json['Data']
  

df = pd.DataFrame(testing_data)
df.to_csv('csv/testing-results-detail.csv', index = None, encoding='utf-8')

