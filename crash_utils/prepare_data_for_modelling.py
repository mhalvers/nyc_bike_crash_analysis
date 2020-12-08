def prepare_data_for_modelling(df, include_fatalities = False, encode_streets = False):

    '''Prepare the collision data for modelling:

    1. Removes latitude, longitude, and collision_id
    2. Encode the crash outcome
    3. Runs crash_utils/make_crash_features.py
    4. One-hot-encodes borough, zip-code, and on-street name
    5. Generates document-term matrix for vehicles and collision factors

    '''

    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.feature_extraction.text import CountVectorizer
    from crash_utils.make_crash_features import make_crash_features


    # trim more columns that aren't useful for modelling
    df.drop(columns=["LATITUDE","LONGITUDE","COLLISION_ID"],inplace = True)

    # now encode the outcome: 0 = no injury, 1 = injury, 2 = fatality
    # (if include_fatalities = True)

    # initiate column
    df["outcome"] = np.nan

    # no injuries
    mask = df["NUMBER OF CYCLIST INJURED"] == 0
    df.loc[mask,"outcome"] = 0

    # injuries only
    mask = df["NUMBER OF CYCLIST INJURED"] > 0
    df.loc[mask,"outcome"] = 1

    # fatalities
    mask = df["NUMBER OF CYCLIST KILLED"] > 0

    if include_fatalities:
        df.loc[mask,"outcome"] = 2
    else:
        df = df.loc[~mask]


    df.drop(columns = ["NUMBER OF CYCLIST INJURED","NUMBER OF CYCLIST KILLED"],
            inplace = True)


    # make another data frame, but now with features (can be easier for some analyses)
    df = make_crash_features(df)


    # lowercase the column names
    df.columns= df.columns.str.lower()


    # now one-hot encode some data

    cols_to_encode = ["borough","zip code"]

    if encode_streets:
        cols_to_encode.append("on street name")
    
    ohe = OneHotEncoder(drop = "first")
    ohe.fit(df[cols_to_encode])
    ohe_matrix = ohe.transform(df[cols_to_encode])
    ohe_df = pd.DataFrame.sparse.from_spmatrix(data = ohe_matrix,
                                               columns = ohe.get_feature_names())


    # generate a document-term matrix for the vehicles and contributing factors

    # vehicles
    # 1. Instantiate
    bagofwords = CountVectorizer(token_pattern=r"(?u)\S\S+")

    # 2. Fit
    bagofwords.fit(df["vehicles"])

    # 3. Transform
    veh_transformed = bagofwords.transform(df["vehicles"])

    veh_df = pd.DataFrame.sparse.from_spmatrix(data = veh_transformed,
                                               columns = bagofwords.get_feature_names())


    # crash factors

    # 1. Instantiate
    bagofwords = CountVectorizer(token_pattern=r"(?u)\S\S+")

    # 2. Fit
    bagofwords.fit(df["factors"])

    # 3. Transform
    factors_transformed = bagofwords.transform(df["factors"])


    factors_df = pd.DataFrame.sparse.from_spmatrix(data = factors_transformed,
                                                   columns = bagofwords.get_feature_names())



    # concatenate the original df, the ohe df, and the two document term dfs

    # reset indices to ensure smooth concatenation
    df.reset_index(drop = True, inplace = True)
    ohe_df.reset_index(drop=True, inplace=True)
    veh_df.reset_index(drop = True, inplace=True)
    factors_df.reset_index(drop = True, inplace=True)


    df = pd.concat((df,ohe_df,veh_df, factors_df),axis=1)
    del ohe_df, veh_df, factors_df

    # drop all columns that we encoded or count-vectorized
    df.drop(columns = ["vehicles","factors","borough","zip code","on street name"],
            inplace = True)


    # move outcome to be the 1st column
    outcome = df["outcome"]
    df.drop(columns="outcome",inplace=True)
    df.insert(0,"outcome",outcome)


    return df
