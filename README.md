# NYC bike crash analysis

## Description

This repo contains python notebooks and code to analyze NYPD records of bike crashes.  The goals was to do some basic EDA to develop an understanding of when/why/where crashes occur, and then to build a predictive model for bike crashes.  

# Analysis report

A brief report summarizing the findings of the analysis can be found in markdown format [here](https://github.com/mhalvers/nyc_bike_crash_analysis/tree/main/report).

# Instructions for use

1. Clone the repo: `git clone https://github.com/mhalvers/nyc_bike_crash_analysis.git`
2. Run `make` to download the most recent crash data.  Here is what `make` will do:
   1. Run `retrieve_nyc_crashes_soda.py` to download all available data into a csv file using [sodaypy](https://github.com/xmunoz/sodapy), a python client for the [Socrata Open Data API](https://dev.socrata.com/).
   2. (Optional) Downloading works best when the data request is made with a user-specific token (strict throttling is removed).  A token can be obtained by registering here with Socrata: https://data.cityofnewyork.us/signup.  
   3. (Optional) Store the token in an environment variable called `SODAPY_APPTOKEN` with the following command: `export SODAPY_APPTOKEN=<token>`.  Better yet, place this into your `.bash_profile` or `.bashrc`.
3. Or, simply run `retrieve_nyc_crashes_soda.py`.  Command line options are required, type `./retrieve_nyc_crashes_soda.py --help` for help.
4. Open `NYC_bike_crash_summary_stats.ipynb` to read the data from the csv output and explore.

## Data

The data were obtained from the NYC OpenData service.  The primary data set analyzed here was filtered from the [Motor Vehicle Collisions - Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data) page.  I filtered the data with the condition that "bike" or "bicycle" must appear somewhere in each row.

Each row contains a crash event.  The NYPD must file a police report if there is a death, injury, or significant property damage (>$1000).  The rows are described in [this spreadsheet](https://data.cityofnewyork.us/api/views/h9gi-nx95/files/bd7ab0b2-d48c-48c4-a0a5-590d31a3e120?download=true&filename=MVCollisionsDataDictionary_20190813_ERD.xlsx).

<img src="https://markhalverson.weebly.com/uploads/4/2/1/8/42181011/outcome-map_orig.png" alt="Crash outcome map" style="zoom:50%;" />

