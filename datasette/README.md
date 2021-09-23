# datasette for displaying CSV files

This directory contains scripts to help display some of the CSV files
using [datasette](https://datasette.io/).

datasette takes a sqlite database and provides a full-featured web
user interface for interacting with the data.

## Conversion

First, the CSV file has to be converted into a sqlite file.

The scripts for performing these conversions are in the converters directory.
These scripts also do some light massaging of the data - renaming long or
obtuse column names and dropping less useful ones.

## datasette

The `launch-datasette` command is a helper to launch the program.

## hosting

The datasette is currently hosted via:

https://pressnyc.workingdirectory.net/d/doe-covid-data/

## Updates

The data is kept up to date via a cron job that re-converts the latest data.

