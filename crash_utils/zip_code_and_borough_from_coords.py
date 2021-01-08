def zip_code_and_borough_from_coords(df):

    """A fairly large number of postal codes and boroughs are missing from the crash
    data.

    Notebook to develop a function that takes in lat/lon pair and
    returns a postal code and borough.

    Note: After filling in as many missing values as possible, this
    function removes any rows that still do not have a zip code and
    borough.  It is possible for such cases to occur when the crash is
    missing coordinates.

    """

    ## imports
    import pandas as pd
    import numpy as np

    data_path = "data/"


    # crash data for testing as script
    # read the crash data, but only the relevant columns
    #data_file_with_path = data_path + "Motor_Vehicle_Collisions_-_Crashes.csv"
    #df = pd.read_csv(data_file_with_path, usecols = [2, 3, 4, 5])

    # read in the zip code / lat-lon file
    ny = pd.read_csv(data_path + "NY-zip-code-latitude-and-longitude.csv",delimiter=";", usecols=[0, 1, 3, 4])


    # there are some zeros in the positions.  nan them
    mask = (df["latitude"] < 35) | (df["longitude"]>-65)
    df.loc[mask,"latitude"] = np.nan
    df.loc[mask,"longitude"] = np.nan


    # the NY state file contains zip codes for all of NY state.  subset to
    # the region we need:
    minlat, maxlat = np.min(df["latitude"]), np.max(df["latitude"])
    minlon, maxlon = np.min(df["longitude"]), np.max(df["longitude"])


    latlonmask = (ny["Longitude"] >= minlon) & (ny["Longitude"] <= maxlon)
    latlonmask = latlonmask &                 \
                 (ny["Latitude"] >= minlat) & \
                 (ny["Latitude"] <= maxlat)
    ny = ny[latlonmask]


    # get indices of crashes missing a zip code
    missing_mask = df["zip code"].isnull().to_numpy()
    missing_ind = np.nonzero(missing_mask)[0]


    # run through all of the instances of a missing zip code in crash data
    # frame find the distance between all of the NY zip code coordinates
    # and the crash coordinates find the nearest zip code to the crash
    # fill the missing zip code in the crash data frame with the nearest
    # zip code
    #
    # in every case but one, a crash with a missing zip code is also
    # missing a borough so use the "city" column of the NY zip code data
    # as the borough.

    borough_col = np.argwhere(df.columns == "borough")[0]
    zip_col = np.argwhere(df.columns == "zip code")[0]

    for k in missing_ind:

        dist = (df.iloc[k]["longitude"] - ny["Longitude"])**2 + \
               (df.iloc[k]["latitude"] - ny["Latitude"])**2
        dist = dist.to_numpy()

        nearest_ind = np.argmin(dist)
        nearest_zip = ny.iloc[nearest_ind]["Zip"]
        nearest_borough = ny.iloc[nearest_ind]["City"]

        dist = dist[nearest_ind]

        if np.isfinite(dist):
            df.iloc[k,zip_col] = nearest_zip
            df.iloc[k,borough_col] = nearest_borough

            #print(f"k = {k}, min. distance = {dist}, nearest index = {nearest_ind}, nearest zip = {nearest_zip}")




    # drop all rows where there isn't a borough (and also therefore a
    # zipcode)
    mask = df["borough"].isna()
    df = df[~mask]


    # make the zip code an integer
    df["zip code"] = df["zip code"].astype(str)


    ## now rename to fit in one of the five boroughs

    # "New York" in the zip code file is actually Manhattan
    df["borough"] = df["borough"].str.replace("New York","MANHATTAN")

    # the NY zip code "cities" were not all-caps
    df["borough"] = df["borough"].str.replace("Bronx","BRONX")
    df["borough"] = df["borough"].str.replace("Brooklyn","BROOKLYN")
    df["borough"] = df["borough"].str.replace("Staten Island","STATEN ISLAND")

    # all of the others appear to be in Queens
    #boroughs = ('STATEN ISLAND', 'BRONX', 'QUEENS', 'MANHATTAN','BROOKLYN')
    #mask = False * len(df)
    #for borough in boroughs:
    #    mask = mask | (df["borough"] == borough)
    #mask = ~mask

    # klugey, but find all the non-boroughs just by looking for
    # strings that are not all upper-case
    mask = df["borough"].str.isupper()
    mask = ~mask

    df.loc[mask,"borough"] = "QUEENS"

    return df
