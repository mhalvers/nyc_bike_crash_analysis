#!/usr/bin/env python3
def retrieve_nyc_crashes_soda(token=None, query=None, output_file=None):

    """Retrieve NYC motor vehicle crash data from NYC Open Data using the
    sodapy, the python client for the Socrata Open Data API.  Returns
    data in a pandas dataframe.

    The default SoSQL query (https://dev.socrata.com/docs/queries/)
    is:

    select *
    where
    VEHICLE_TYPE_CODE1 = 'Bike' OR VEHICLE_TYPE_CODE1 = 'BICYCLE'
    OR
    VEHICLE_TYPE_CODE2 = 'Bike' OR VEHICLE_TYPE_CODE2 = 'BICYCLE'
    OR
    VEHICLE_TYPE_CODE_3 = 'Bike' OR VEHICLE_TYPE_CODE_3 = 'BICYCLE'
    OR
    VEHICLE_TYPE_CODE_4 = 'Bike' OR VEHICLE_TYPE_CODE_4 = 'BICYCLE'
    OR
    VEHICLE_TYPE_CODE_5 = 'Bike' OR VEHICLE_TYPE_CODE_5 = 'BICYCLE'
    OR
    NUMBER_OF_CYCLIST_INJURED > 0 OR NUMBER_OF_CYCLIST_KILLED > 0
    limit 1000000

    Note we have to specify a very high limit because the query
    defaults to 1000 records.

    """

    import os
    import pandas as pd
    from sodapy import Socrata


    # set up the Socrata client
    # use custom token to remove throttling):
    client = Socrata("data.cityofnewyork.us", token)


    # If a custom SoSQL query is not specified, set one up to retrieve
    # records containing bike crashes.  Note we have to specify a very
    # high limit because the query defaults to 1000 records

    if query is None:
        print("Using default query bicycle crash parameters")
        query = """
                select *
                where
                VEHICLE_TYPE_CODE1 = 'Bike' OR VEHICLE_TYPE_CODE1 = 'BICYCLE'
                OR
                VEHICLE_TYPE_CODE2 = 'Bike' OR VEHICLE_TYPE_CODE2 = 'BICYCLE'
                OR
                VEHICLE_TYPE_CODE_3 = 'Bike' OR VEHICLE_TYPE_CODE_3 = 'BICYCLE'
                OR
                VEHICLE_TYPE_CODE_4 = 'Bike' OR VEHICLE_TYPE_CODE_4 = 'BICYCLE'
                OR
                VEHICLE_TYPE_CODE_5 = 'Bike' OR VEHICLE_TYPE_CODE_5 = 'BICYCLE'
                OR
                NUMBER_OF_CYCLIST_INJURED > 0 OR NUMBER_OF_CYCLIST_KILLED > 0
                limit 1000000
                """


    # results returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("h9gi-nx95", query=query)


    # results is a list of dictionaries.  each dictionary is a crash
    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)

    print(f"Retrieved {df.shape[0]} crashes involving bicycles")


    # sodapy goofs up a few column names
    df.rename(columns={"vehicle_type_code1": "vehicle_type_code_1",
                       "vehicle_type_code2": "vehicle_type_code_2"},inplace=True)


    # remove underscores from column names
    df.columns = df.columns.str.replace('_', ' ')


    if output_file is not None:
        df.to_csv(path_or_buf = output_file, index=False)
        print(f"Wrote file: {os.getcwd()}/{output_file}")


    return df



if __name__ == "__main__":

    import argparse

    my_parser = argparse.ArgumentParser(description="Download NPYD motor vehicle crash data")

    my_parser.add_argument("--token", type=str, help="User's token")
    my_parser.add_argument("output", type=str, help="Data output file name")
    my_parser.add_argument("--query", type=str, help="SoSQL query string")

    args = my_parser.parse_args()

    my_token = args.token
    my_query = args.query
    outfile = args.output

    retrieve_nyc_crashes_soda(token=my_token, query=my_query, output_file=outfile)
