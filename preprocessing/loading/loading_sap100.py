# Created by Erin Watson
# April 14, 2024
# As a part of the effort to get Tidepool data through the GLYFE metric

import pandas as pd
import datetime
from os.path import join
import numpy as np
import misc.constants as cs
import misc.datasets

def load_sap100(dataset, subject):
    """
    Load a Tidepool SAP100 file into a dataframe
    This same function might apply to other Tidepool datasets like PA50 and HCL150, I don't know.
    :param dataset: name of dataset
    :param subject: name of subject
    :param day_len: length of day scaled to sampling frequency
    :return: dataframe
    """
    df = pd.read_csv(join(cs.path, "data", "sap100", "short-names", subject + ".csv"), low_memory=False)
    # pull in just the data needed to run the GLYFE metric (no extras!)
    df_glucose_carb_bolus = df[["cDateTime", "blood_glucose_level", "carbs", "normal", "extendedAmount"]].copy()
    # aggregate bolus data and rename columns
    df_glucose_carb_bolus["insulin"] = df_glucose_carb_bolus["normal"] + df_glucose_carb_bolus["extendedAmount"]
    df_glucose_carb_bolus = df_glucose_carb_bolus.drop(columns=["normal", "extendedAmount"])
    df_glucose_carb_bolus.rename(columns={"cDateTime": "datetime", "blood_glucose_level": "glucose", "carbs": "CHO"}, inplace=True)
    # convert datetime to a datetime object
    df_glucose_carb_bolus["datetime"] = pd.to_datetime(df_glucose_carb_bolus["datetime"])

    return df_glucose_carb_bolus
  