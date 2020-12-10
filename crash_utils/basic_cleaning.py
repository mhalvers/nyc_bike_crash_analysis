def basic_cleaning(df):

    """Performs some basic cleaning steps on the NYC crash data.
    1. Removes "LOCATION" column (redundant)
    2. Replaces zero'ed lat/lons with NaNs
    3. Corrects a misspelling in the contributing factors.
    4. Converts crash date and time to datetime64 ("DATETIME")
    5. Drops "OFF STREET NAME" column
    6. Fixes NaNs in "NUMBER OF PERSONS KILLED" and "NUMBER OF PERSONS INJURED"
    7. Changes a few dtypes to integers.
    8. Sorts rows by "DATETIME"
    """

    # imports
    import pandas as pd
    import numpy as np


    # first, remove LOCATION.  it is redundant with LATITUDE and LONGITUDE
    df.drop(columns = "LOCATION", inplace = True)


    # there are some zeros in the positions
    mask = (df["LATITUDE"] < 35) | (df["LONGITUDE"]>-65)
    df.loc[mask,"LATITUDE"] = np.nan
    df.loc[mask,"LONGITUDE"] = np.nan


    # correct the mis-spelling of "illness"
    mask = df["CONTRIBUTING FACTOR VEHICLE 1"].str.fullmatch("illnes", case=False)
    mask.fillna(False,inplace = True)
    df.loc[mask,"CONTRIBUTING FACTOR VEHICLE 1"] = "Illness"
    
    
    # change date and time to datetime64
    crash_dt = df["CRASH DATE"] + " " + df["CRASH TIME"]
    crash_dt = pd.to_datetime(crash_dt)
    df.insert(0, "DATETIME", crash_dt)
    df.drop(columns = ["CRASH DATE", "CRASH TIME"], inplace = True)


    # OFF-STREET NAME
    # list( df["OFF STREET NAME"][~df["OFF STREET NAME"].isna()] )
    # basically a street address if there is one.  missing 90% of the values
    df.drop(columns="OFF STREET NAME", inplace = True)


    # NUMBER OF PERSONS INJURED and NUMBER OF PERSONS KILLED have a few nans
    # fix them
    na_rows = df["NUMBER OF PERSONS INJURED"].isna()
    na_rows = df.loc[na_rows,:].index

    # the first one, 21634, has no injuries or deaths, but a bike was involved
    # assume then this was a property damage incident (no injury or death)
    df.loc[na_rows[0],"NUMBER OF PERSONS INJURED"] = 0
    df.loc[na_rows[0],"NUMBER OF PERSONS KILLED"] = 0


    # the second one, 26814, has a NUMER OF CYCLIST INJURED = 1, but nothing in the 
    df.loc[na_rows[1],"NUMBER OF PERSONS INJURED"] = 1
    df.loc[na_rows[1],"NUMBER OF PERSONS KILLED"] = 0


    # convert the following columns to integer dtypes
    df["NUMBER OF PERSONS INJURED"] = df["NUMBER OF PERSONS INJURED"].astype("int")
    df["NUMBER OF PERSONS KILLED"] = df["NUMBER OF PERSONS KILLED"].astype("int")


    # sort the collisions by timestamp
    df.sort_values(by = "DATETIME", inplace = True, ignore_index = True)


    # any duplicate rows?
    df.drop_duplicates(inplace = True, ignore_index = True)


    return df
