def basic_cleaning(df):

    """Performs some basic cleaning steps on the NYC crash data.
    1.  Removes "LOCATION" column (redundant)
    2.  Replaces zero'ed lat/lons with NaNs
    3.  Corrects a misspelling in the contributing factors.
    4.  Converts crash date and time to datetime64 ("DATETIME")
    5.  Drops "OFF STREET NAME" column
    6.  Fixes NaNs in "NUMBER OF PERSONS KILLED" and "NUMBER OF PERSONS INJURED"
    7.  Changes a few dtypes to integers.
    8.  Removes rows with no cyclist involvement.
    9.  Sorts rows by "DATETIME"
    10. Drops duplicate rows
    """

    # imports
    import pandas as pd
    import numpy as np


    # first, remove LOCATION.  it is redundant with LATITUDE and LONGITUDE
    df.drop(columns = "location", inplace = True)


    # there are some zeros in the positions
    mask = (df["latitude"] < 35) | (df["longitude"]>-65)
    df.loc[mask,"latitude"] = np.nan
    df.loc[mask,"longitude"] = np.nan


    # correct the mis-spelling of "illness"
    mask = df["contributing factor vehicle 1"].str.fullmatch("illnes", case=False)
    mask.fillna(False,inplace = True)
    df.loc[mask,"contributing factor vehicle 1"] = "Illness"


    # change date and time to datetime64
    crash_dt = df["crash date"] + " " + df["crash time"]
    crash_dt = pd.to_datetime(crash_dt)
    df.insert(0, "datetime", crash_dt)
    df.drop(columns = ["crash date", "crash time"], inplace = True)


    # off-street name
    # list( df["off street name"][~df["off street name"].isna()] )
    # basically a street address if there is one.  missing 90% of the values
    df.drop(columns="off street name", inplace = True)


    # captialize the street names
    df["on street name"] = df["on street name"].str.title()
    df["cross street name"] = df["cross street name"].str.title()


    # NUMBER OF PERSONS INJURED and NUMBER OF PERSONS KILLED have a few nans
    # fix them
    na_rows = df["number of persons injured"].isna()
    na_rows = df.loc[na_rows,:].index

    # the first one, 21634, has no injuries or deaths, but a bike was involved
    # assume then this was a property damage incident (no injury or death)
    df.loc[na_rows[0],"number of persons injured"] = 0
    df.loc[na_rows[0],"number of persons killed"] = 0


    # the second one, 26814, has a NUMER OF CYCLIST INJURED = 1, but nothing in the
    df.loc[na_rows[1],"number of persons injured"] = 1
    df.loc[na_rows[1],"number of persons killed"] = 0


    # convert the following columns to integer dtypes
    df["number of persons injured"] = df["number of persons injured"].astype("int")
    df["number of persons killed"] = df["number of persons killed"].astype("int")


    # remove instances when no bicyclist was involved.  here we state
    # that "bike" must be mentioned in the "VEHICLES" column, OR that
    # there must have been a cyclist injuries or fatality

    # easiest to search all columsn of VEHICLE TYPE by cat'ing them first
    col_ind = df.columns.str.match("vehicle_type")
    cols = df.columns[col_ind].tolist()

    new_str = df["vehicle type code 1"]
    for col in cols[1:]:
        new_str = new_str.str.cat(df[col], sep = ",", na_rep = "")


    # what rows contain "bike"?
    has_bike = new_str.str.contains("bike")


    # maybe "bike" was recorded in vehicle types.  also check if there
    # is a cyclist injury or death
    cyclist_mask = (df["number of cyclist injured"] > 0) | (df["number of cyclist killed"] > 0)

    # combine the masks
    the_mask = has_bike | cyclist_mask

    # keep only the desired rows
    df = df.loc[the_mask]


    # sort the collisions by timestamp
    df.sort_values(by = "datetime", inplace = True, ignore_index = True)


    # any duplicate rows?
    df.drop_duplicates(inplace = True, ignore_index = True)


    return df
