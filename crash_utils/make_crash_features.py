def make_crash_features(df):
    """
    Feature Engineering

    [x] is_intersection (when ON STREET NAME and CROSS STREET NAME are non-null)
    [ ] is_day, is_dusk, is_dawn, is_night (use hour)
    [x] hour and month
    [ ] is_summer, is_winter (use month) or maybe do this by season
    [ ] get precip/weather
    [x] number of vehicles in accident


    Note: Might want to note that it will be difficult to predict how many
    vehicles (or what type of vehicle) will be involved in an accident, so
    regressing on it might not be helpful because N_vehicles cannot be
    predicted?
    """

    # the usual
    import pandas as pd
    import numpy as np


    # Let's try and set up an is_intersetion by looking at existence of
    # "ON STREET NAME" and "CROSS STREET NAME"

    is_intersection = df["ON STREET NAME"].notna() & \
                      df["CROSS STREET NAME"].notna()
    df.insert(4,"is_intersection",is_intersection)

    # drop cross street
    df.drop(columns="CROSS STREET NAME",inplace=True)


    # trim the street name strings and upper
    df["ON STREET NAME"] = df["ON STREET NAME"].str.strip()
    df["ON STREET NAME"] = df["ON STREET NAME"].str.upper()


    # let's replace all street names with very few incidents with "other"
    mask = df["ON STREET NAME"].value_counts().values < 10
    strs_to_other = df["ON STREET NAME"].value_counts().index[mask]

    mask = df["ON STREET NAME"].isin(strs_to_other)
    df.loc[mask,"ON STREET NAME"] = "OTHER"


    # now work on time/date
    # let's get month, day of week, and hour of the day

    df["MONTH"] = pd.DatetimeIndex(df["DATETIME"]).month
    df["DAY_OF_WEEK"] = pd.DatetimeIndex(df["DATETIME"]).dayofweek
    df["HOUR"] = pd.DatetimeIndex(df["DATETIME"]).hour

    # now drop the datetime
    df.drop(columns = "DATETIME",inplace = True)


    # compute number of vehicles by couning non-nulls in vehicle type

    df["n_vehicle"] = df.loc[:,"VEHICLE TYPE CODE 1":"VEHICLE TYPE CODE 5"].notnull().sum(axis=1)


    # vehicle type will not be everything but bikes.  in other words,
    # we only want the other vehicle (if any)
    # that was involved in the crash.

    # there are some cases when there are only 1 vehicle. 

    #df.columns[-5:]

    # n1bikemask = (df["n_vehicle"] == 1) & (df["VEHICLE TYPE CODE 1"] == "bike")
    # df.loc[n1bikemask,"VEHICLE TYPE CODE 1"] = "none"

    # n1bikemask = (df["n_vehicle"] == 1) & (df["VEHICLE TYPE CODE 2"] == "bike")
    # df.loc[n1bikemask,"VEHICLE TYPE CODE 2"] = "none"

    #sum(n1bikemask)
    #df["VEHICLE TYPE CODE 1"][df["n_vehicle"]==1].head(50)



    # concatenate the vehicle types, separate by comma

    # first replace NaNs with empty strings
    col_ind = df.columns.str.match("VEHICLE")
    cols = df.columns[col_ind]

    for col in cols:
        df.loc[df[col].isna(),col]= ""

    # concatenate the columns    
    new_str = df["VEHICLE TYPE CODE 1"]
    for col in cols[1:]:
        new_str = new_str.str.cat(df[col], sep = ",")

    # add result as new column.  drop the individual columns    
    df["VEHICLES"] = new_str
    df.drop(columns = cols, inplace = True)


    #_now repeat for contributing factors

    # number of factors (1 for each vehicle for the most part)
    df["n_factor"] = df.loc[:,"CONTRIBUTING FACTOR VEHICLE 1":"CONTRIBUTING FACTOR VEHICLE 5"].notnull().sum(axis=1)


    # first replace NaNs with empty strings
    col_ind = df.columns.str.match("CONTRIBUTING")
    cols = df.columns[col_ind]

    for col in cols:
        df.loc[df[col].isna(),col]= ""


    new_str = df["CONTRIBUTING FACTOR VEHICLE 1"]
    for col in cols[1:]:
        new_str = new_str.str.cat(df[col], sep = ",")    


    df["factors"] = new_str
    df.drop(columns = cols, inplace = True)


    return df
