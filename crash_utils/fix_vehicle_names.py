def fix_vehicle_names(df):

    # the usual
    import pandas as pd
    import numpy as np

    ## for testing
    data_path = "/Users/Mark/brainstation/capstone/nyc_bike_crash_analysis/data/"
    data_file_with_path = data_path + "Motor_Vehicle_Collisions_-_Crashes.csv"
    df = pd.read_csv(data_file_with_path)


    # first lower-case and trim trailing and leading white space everything
    for col in df.columns[-5:]
        df[col] = df[col].str.lower()
        df[col] = df[col].str.strip()

    def vehicle_name_map():
        vehicle_map = {
            "bicycle":"bike",

            "sedan":"passenger vehicle",
            "station wagon/sport utility vehicle":"passenger vehicle",
            "sport utility / station wagon":"passenger vehicle",
            "4 dr sedan":"passenger vehicle",
            "2 dr sedan":"passenger vehicle",
            "convertible":"passenger vehicle",

            "truck":"pick-up truck",
            "pick up tr":"pick-up truck",

            "livery vehicle":"limousine",
            "limo":"limousine",
            "limou":"limousine",

            "posta":"mail truck",
            "usps":"mail truck",
            "usps mail":"mail truck",

            "ambu":"ambulance",
            "ambul":"ambulance",

            "garbage tr":"garbage truck",
            "garbage or refuse":"garbage truck",
            "sanit":"garbage truck",

            "cement tru":"cement truck",
            "concrete mixer":"cement truck",

            "dump":"dump truck",

            "fire":"fire truck",
            "fdny":"fire truck",
            "firet":"fire truck",
            "fire engin":"fire truck",

            "small com veh(4 tires)":"small com veh",
            "ford sprin":"small com veh",
            "sprin":"small com veh",
            "refrigerated van":"small com veh",
            "deliv":"small com veh",

            "large com veh(6 or more tires)":"large com veh",
            "box t":"large com veh",
            "box truck":"large com veh",
            "tow truck / wrecker":"large com veh",
            "chassis cab":"large com veh",
            "beverage truck":"large com veh",
            "flat bed":"large com veh",
            "comme":"large com veh",
            "pallet":"large com veh",
            "armored truck":"large com veh",

            "tanker":"tractor truck",
            "tractor truck gasoline":"tractor truck",
            "tractor truck diesel":"tractor truck",

            "schoo":"school bus",
            "mta b":"bus",
            "postal bus":"bus",

            "dirt bike":"motorcycle",
            "dirtbike":"motorcycle",

            "moped scoo":"moped",
            "moped elec":"moped",

            "e-bik":"e-bike",
            "e bike":"e-bike",
            "ebike":"e-bike",
            "scoot":"scooter",
            "e sco":"e-scooter",
            "e-sco":"e-scooter",
            "unkno":"unknown"
        }
        return vehicle_map


    # do the actual mapping
    for old, new in vehicle_map.items():
        df["VEHICLE TYPE CODE 1"] = df["VEHICLE TYPE CODE 1"].replace(old,new, regex = False)
        df["VEHICLE TYPE CODE 2"] = df["VEHICLE TYPE CODE 2"].replace(old,new, regex = False)
        df["VEHICLE TYPE CODE 3"] = df["VEHICLE TYPE CODE 3"].replace(old,new, regex = False)
        df["VEHICLE TYPE CODE 4"] = df["VEHICLE TYPE CODE 4"].replace(old,new, regex = False)
        df["VEHICLE TYPE CODE 5"] = df["VEHICLE TYPE CODE 5"].replace(old,new, regex = False)


    
    # now fill in everything with fewer than 5 incidents in Vehicle column 1
    # and everything with fewer than 3 incidents in Vehicle colkumn 2
    # with "other".
    strs_to_other_1 = df["VEHICLE TYPE CODE 1"].value_counts()
    strs_to_other_1 = strs_to_other_1[strs_to_other_1<5]

    strs_to_other_2 = df["VEHICLE TYPE CODE 2"].value_counts()
    strs_to_other_2 = strs_to_other_2[strs_to_other_2<3]

    strs_to_other = pd.concat([strs_to_other_1,strs_to_other_2]).index
    
    for cols in df.columns[-5:]:
        mask = df[cols].isin(strs_to_other)
        df.loc[mask,cols] = "other"


    return df
