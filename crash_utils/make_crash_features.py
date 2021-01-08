def make_crash_features(df, drop_featured_columns = True):
    """
    Feature Engineering

    [x] is_intersection (when ON STREET NAME and CROSS STREET NAME are non-null)
    [ ] is_day, is_dusk, is_dawn, is_night (use hour)
    [x] hour, month, day of week
    [ ] is_summer, is_winter (use month) or maybe do this by season
    [ ] weather
    [x] number of vehicles in accident
    [x] number of factors in accident

    Also concatenates the CONTRIBUTING FACTOR and VEHICLE TYPE columns
    so that the count vectorizer can easily digest them.

    """

    # the usual
    import pandas as pd
    import numpy as np


    # Let's try and set up an is_intersetion by looking at existence of
    # "ON STREET NAME" and "CROSS STREET NAME"

    is_intersection = df["on street name"].notna() & \
                      df["cross street name"].notna()
    df.insert(4,"is_intersection",is_intersection)


    # drop cross street
    if drop_featured_columns:
        df.drop(columns="cross street name",inplace=True)


    # replace missing "ON STREET NAME" with "MISSING"
    df["on street name"].fillna("MISSING", inplace = True)


    # trim the street name strings and upper
    df["on street name"] = df["on street name"].str.strip()
    df["on street name"] = df["on street name"].str.upper()


    # let's replace all street names with very few incidents with "other"
    mask = df["on street name"].value_counts().values < 10
    strs_to_other = df["on street name"].value_counts().index[mask]

    mask = df["on street name"].isin(strs_to_other)
    df.loc[mask,"on street name"] = "OTHER"


    # now work on time/date: get month, day of week, and hour of the
    # day

    df["month"] = pd["datetime"].dt.month
    df["DAY_OF_WEEK"] = pd["datetime"].dayofweek
    df["HOUR"] = pd["datetime"].hour


    # now drop the datetime
    if drop_featured_columns:
        df.drop(columns = "datetime",inplace = True)


    # compute number of vehicles by couning non-nulls in vehicle type
    col_ind = df.columns.str.match("vehicle type")
    cols = df.columns[col_ind].tolist()

    df["n_vehicle"] = df.loc[:,cols].notnull().sum(axis=1)


    # vehicle type will not be everything but bikes.  in other words,
    # we only want the other vehicle (if any) that was involved in the
    # crash.

    # there are some cases when there are only 1 vehicle.

    # n1bikemask = (df["n_vehicle"] == 1) & (df["VEHICLE TYPE CODE 1"] == "bike")
    # df.loc[n1bikemask,"VEHICLE TYPE CODE 1"] = "none"

    # n1bikemask = (df["n_vehicle"] == 1) & (df["VEHICLE TYPE CODE 2"] == "bike")
    # df.loc[n1bikemask,"VEHICLE TYPE CODE 2"] = "none"

    #sum(n1bikemask)
    #df["VEHICLE TYPE CODE 1"][df["n_vehicle"]==1].head(50)


    # concatenate the vehicle types into a single column

    # concatenate the columns
    new_str = df["vehicle type code 1"]
    for col in cols[1:]:
        new_str = new_str.str.cat(df[col], sep = ",", na_rep = "")


    # add result as new column.
    df["vehicles"] = new_str


    # first, put a dash in the spaces to keep things like "passenger
    # vehicle" together
    df["vehicles"] = df["vehicles"].str.replace(" ","-")


    # replace the commas with a white space for the count vectorizer
    df["vehicles"] = df["vehicles"].str.replace(","," ")

    # drop the individual columns
    if drop_featured_columns:
        df.drop(columns = cols, inplace = True)


    # there are several cases when VEHICLES contains the same two
    # vehicles, but they are ordered differently.  for example, “taxi
    # bike” and “bike taxi”. fix by alphabetizing
    df["vehicles"] = df["vehicles"].str.split().apply(sorted,reverse=True).str.join(sep=" ")


    # now concatenate the contributing factors

    # build list of columns on which to operate
    col_ind = df.columns.str.match("contributing")
    cols = df.columns[col_ind].tolist()

    # number of factors (1 for each vehicle for the most part)

    df["n_factor"] = df.loc[:,cols].notnull().sum(axis=1)


    # concatenate all CONTRIBUTING FACTORS text into a single column
    new_str = df["contributing factor vehicle 1"]
    for col in cols[1:]:
        new_str = new_str.str.cat(df[col], sep = ",", na_rep = "")


    # now drop the individual columns
    df["factors"] = new_str


    # put a dash in the spaces to keep things like "passenger vehicle" together
    df["factors"] = df["factors"].str.replace(" ","-")


    # replace "Driver-Inattention/Distraction" with "Driver-Inattention"
    df["factors"] = df["factors"].str.replace("Driver-Inattention/Distraction","Driver-Inattention")

    # replace the commas with a white space for the count vectorizer
    df["factors"] = df["factors"].str.replace(","," ")

    # something about the string types is causing the sklearn
    # CountVectorizer to choke.  solution is to change to unicode:
    # https://stackoverflow.com/questions/39303912/tfidfvectorizer-in-scikit-learn-valueerror-np-nan-is-an-invalid-document
    df["factors"] = df["factors"].values.astype('U')


    if drop_featured_columns:
        df.drop(columns = cols, inplace = True)


    return df
