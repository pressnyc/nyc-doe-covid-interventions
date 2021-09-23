#!/usr/bin/python3

# Import required libraries
import sqlite3
import pandas as pd
import sys

table_name = 'activeInterventions' 
csv_path = '../csv/activeinterventioncases.csv'
sqlite_path = 'datasette-dbs/doe-covid-data.db'

# Connect to SQLite database
conn = sqlite3.connect(sqlite_path)
  
# Load CSV data into Pandas DataFrame
data = pd.read_csv(csv_path)
# Write the data to a sqlite table
data.to_sql('temp_table', conn, if_exists='replace', index=True)

# Rename fields for easier comprehension.
mapper = {
        "nycsr_admininterventiontype@OData.Community.Display.V1.FormattedValue": "typeValue",
        "nycsr_interventionenddate@OData.Community.Display.V1.FormattedValue": "interventionDateFormatted",
        "nycsr_interventionstartdate@OData.Community.Display.V1.FormattedValue": "startDateFormatted",
        "nycsr_building.nycsr_address": "buildingAddress",
        "nycsr_building.nycsr_borough@OData.Community.Display.V1.FormattedValue": "boroughFormatted",
        "nycsr_building.nycsr_geographicaldistrictcode": "districtCode",
        "nycsr_building.nycsr_buildingname": "buildingName",
        "nycsr_locationsite.nycsr_sitename": "siteName"
}

cur = conn.cursor()
for original_column in mapper:
    new_column = mapper[original_column]
    sql = 'ALTER TABLE temp_table RENAME COLUMN `{0}` TO `{1}`'.format(original_column, new_column)
    cur.execute(sql)

# Rebuild the table with only the columns we want.
columns = list(mapper.values())
sql = "DROP TABLE IF EXISTS {0}".format(table_name)
cur.execute(sql)
sql = "CREATE TABLE {0} AS SELECT {1} FROM temp_table".format(table_name, ','.join(columns))
cur.execute(sql)
cur.execute("DROP TABLE temp_table")

conn.commit()
conn.close()

