# Created by Erin Watson
# April 14, 2024
# As a part of the effort to get Tidepool data through the GLYFE metric

import pandas as pd
import datetime
from os.path import join
import numpy as np
import misc.constants as cs
import misc.datasets

def load_tidepool(dataset, subject):
    """
    Load a Tidepool file into a dataframe
    :param dataset: name of dataset
    :param subject: name of subject
    :param day_len: length of day scaled to sampling frequency
    :return: dataframe
    """
    df = pd.read_csv(join(cs.path, "data", dataset, subject + ".csv"), low_memory=False)
    # pull in just the data needed to run the GLYFE metric (no extras!)
    df_glucose_carb_bolus = df[["cDateTime", "mg_dL", "grams", "normal", "extendedAmount"]].copy()
    # aggregate bolus data and rename columns
    df_glucose_carb_bolus["insulin"] = df_glucose_carb_bolus["normal"] + df_glucose_carb_bolus["extendedAmount"]
    df_glucose_carb_bolus = df_glucose_carb_bolus.drop(columns=["normal", "extendedAmount"])
    df_glucose_carb_bolus.rename(columns={"cDateTime": "datetime", "mg_dL": "glucose", "grams": "CHO"}, inplace=True)
    # convert datetime to a datetime object
    df_glucose_carb_bolus["datetime"] = pd.to_datetime(df_glucose_carb_bolus["datetime"])

    print(df_glucose_carb_bolus.head())
    return df_glucose_carb_bolus
  

    # df.datetime = (df.datetime % day_len).astype("float64")
    # start_day = datetime.datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    # day_len_ds = day_len * cs.freq / misc.datasets.datasets[dataset]["glucose_freq"]
    # end_day = start_day + datetime.timedelta(days=np.float64(len(df) // day_len_ds)) - datetime.timedelta(minutes=1)
    # df.datetime = pd.period_range(start_day, end_day, freq='5min').to_timestamp()
    # return df