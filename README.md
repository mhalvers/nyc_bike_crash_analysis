# NYC bike crash analysis

## Description

This repo contains python notebooks and code to analyze NYPD records of bike crashes.  The goal is to build a predictive model for bike crashes.  In doing so, we will discover the circumstances under which crashes occur, and even what causes their severity.

## Data

The data were obtained from the NYC OpenData service.  The primary data set analyzed here was filtered from the [Motor Vehicle Collisions - Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data) page.  I filtered the data with the condition that "bike" or "bicycle" must appear somewhere in each row.

Each row contains a crash event.  The NYPD must file a police report if there is a death, injury, or significant property damage (>$1000).  The rows are described in [this spreadsheet](https://data.cityofnewyork.us/api/views/h9gi-nx95/files/bd7ab0b2-d48c-48c4-a0a5-590d31a3e120?download=true&filename=MVCollisionsDataDictionary_20190813_ERD.xlsx).

## Summary

<img src="https://markhalverson.weebly.com/uploads/4/2/1/8/42181011/outcome-map_orig.png" alt="Crash outcome map" style="zoom:80%;" />