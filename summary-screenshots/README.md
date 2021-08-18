# NYC DOE COVID Summary screen shots

This script is designed to be run on a daily schedule. It takes a dated
snapshot of the [NYC DOE COVID Summary
page](https://www.schools.nyc.gov/school-year/school-year-2020-21/return-to-school-2020/health-and-safety/daily-covid-case-map). 

It depends on the [screenshotlayer](https://screenshotlayer.com) API service,
which provides a free API key that can take up to 100 screen shots per month.

It is currently running and producing snapshot images via Jamie's May First
account with images available via: https://pressnyc.workingdirectory.net/img.

## Setup

It can be setup anywhere via a cron job or timer, provided you have obtained an
API key from [screenshotlayer](https://screenshotlayer.com).

```
/path/to/take-doe-covid-summary-screenshot $api_key $img_page
```

For example:

```
/path/to/take-doe-covid-summary-screenshot xyz123 /var/www/foo/img 
```

Each screen shot will be automatically named after the date it was taken (e.g.
`2021-08-23.png`).
