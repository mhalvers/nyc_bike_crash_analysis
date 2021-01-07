def retrieve_nyc_crashes_soda(my_token = None, limit = None):

    """Retrieve NYC motor vehicle crash data from NYC Open Data using the
    sodapy, the python client for the Socrata Open Data API

    Returns data in a pandas dataframe

    """
  
    import pandas as pd
    from sodapy import Socrata


    # set up the Socrata client
    # use custom token to remove throttling):
    client = Socrata("data.cityofnewyork.us", my_token)


    # results returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("h9gi-nx95", limit=limit)


    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)


    return df
