import pandas as pd
import datetime
from os.path import join
import numpy as np
import misc.constants as cs
import misc.datasets


def load_t1dms(dataset, subject, day_len):
    """
    Load a T1DMS file into a dataframe
    :param dataset: name of dataset
    :param subject: name of subject
    :param day_len: length of day scaled to sampling frequency
    :return: dataframe
    """
    # df = pd.read_csv(join(cs.path, "data", dataset, subject + ".csv"), header=None, dtype=np.float64)
    dt = pd.read_csv(join("diabetes_data", "train_301e2b3f992a2ee94fcbd13a207de095e06a99c680f707f2d84a8d60f328c998" + ".csv"), usecols=["cDateTime"])
    df = pd.read_csv(join("diabetes_data", "train_301e2b3f992a2ee94fcbd13a207de095e06a99c680f707f2d84a8d60f328c998" + ".csv"), dtype=np.float64, usecols=["mg_dL", "grams", "bolusInsulinAmount"])

    dt = pd.DataFrame(dt.apply(lambda x: datetime.datetime.timestamp(datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S")), axis=1), columns=["datetime"])
    
    df = pd.concat([dt, df], axis=1)

    df = df.rename(columns={"mg_dL": "glucose", "grams": "CHO", "bolusInsulinAmount": "insulin"}) 


    df.datetime = (df.datetime % day_len).astype("float64")
    # start_day = datetime.datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    start_day = datetime.datetime.strptime("2018-05-09 17:02:00", "%Y-%m-%d %H:%M:%S")
    day_len_ds = day_len * cs.freq / misc.datasets.datasets[dataset]["glucose_freq"]
    end_day = start_day + datetime.timedelta(days=np.float64(len(df) // day_len_ds)) - datetime.timedelta(minutes=1)
    
    print("\n\n\n\n\n", start_day, day_len_ds, end_day)

    df.datetime = pd.period_range(start_day, end_day, freq='1min').to_timestamp()
    return df


def _T1DMS_scaling(data):
    # scale insulin from pmol to unit
    data.loc[:, "insulin"] = data.loc[:, "insulin"] / 6000.0

    # accumulate the CHO intakes
    CHO_indexes = data[np.invert(data.loc[:, "CHO"] == 0.0)].index
    meals, meal, start_idx, past_idx = [], data.loc[CHO_indexes[0], "CHO"], CHO_indexes[0], CHO_indexes[0]
    for idx in CHO_indexes[1:]:
        if idx == past_idx + 1:
            meal = meal + data.loc[idx, "CHO"]
        else:
            meals.append([start_idx, meal])
            meal = data.loc[idx, "CHO"]
            start_idx = idx
        past_idx = idx
    meals.append([start_idx, meal])
    meals = np.array(meals)

    data.loc[:, "CHO"] = 0.0
    data.loc[meals[:, 0], "CHO"] = meals[:, 1]
