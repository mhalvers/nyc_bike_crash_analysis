def basic_cleaning(df):

    """docstring

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
    #list( df["OFF STREET NAME"][~df["OFF STREET NAME"].isna()] )
    # basically a street address if there is one.  missing 90% of the values
    df.drop(columns="OFF STREET NAME", inplace = True)


    # NUMBER OF PERSONS INJURED and NUMBER OF PERSONS KILLED
    # almost everything is there.
    na_rows = df["NUMBER OF PERSONS INJURED"].isna()
    na_rows = df.loc[na_rows,:].index


    # the first one, 21634, has no injuries or deaths.  drop!
    df.drop(index=na_rows[0], inplace = True)


    # the second one, 26814, has a NUMER OF CYCLIST INJURED = 1, but nothing in the 
    df.loc[na_rows[1],"NUMBER OF PERSONS INJURED"] = 1
    df.loc[na_rows[1],"NUMBER OF PERSONS KILLED"] = 0


    # convert the following columns to integer dtypes
    df["NUMBER OF PERSONS INJURED"] = df["NUMBER OF PERSONS INJURED"].astype("int")
    df["NUMBER OF PERSONS KILLED"] = df["NUMBER OF PERSONS KILLED"].astype("int")


    ## sort the collisions by timestamp
    df.sort_values(by = "DATETIME", inplace = True, ignore_index = True)


    ## any duplicate rows?
    # df[df.duplicated(keep = False)]
    df.drop_duplicates(inplace = True, ignore_index = True)


    # there are cases when there are no cyclist fatalies or injuries,
    # but there is an injury or death.  in most cases these are
    # related to crashes involving e-bikes and motorbikes (these
    # vehicles made it through my search query on the NYCOpenData
    # server.
    cyclist_mask = (df["NUMBER OF CYCLIST INJURED"] == 0) & (df["NUMBER OF CYCLIST KILLED"] == 0)
    other_mask = (df["NUMBER OF MOTORIST INJURED"] > 0) | (df["NUMBER OF MOTORIST KILLED"] > 0)
    mask = cyclist_mask & other_mask
    df = df.loc[~mask,:]


    ## finally, let's trim down the data to focus on predicting the
    ## outcome of the cyclist
    drop_cols = ["NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED",
                 "NUMBER OF PEDESTRIANS INJURED", "NUMBER OF PEDESTRIANS KILLED",
                 "NUMBER OF MOTORIST INJURED", "NUMBER OF MOTORIST KILLED"]

    df.drop(columns=drop_cols, inplace=True)

    return df

