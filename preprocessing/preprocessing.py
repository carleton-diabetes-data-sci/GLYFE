from exceptiongroup import catch
import pandas as pd
from .cleaning.unit_scaling import scaling_T1DMS
from misc import constants as cs
from preprocessing.cleaning.nans import remove_nans, fill_nans
from preprocessing.loading.loading_ohio import load_ohio
from preprocessing.loading.loading_t1dms import load_t1dms
from preprocessing.loading.loading_sap100 import load_sap100
import misc.datasets
from preprocessing.resampling import resample
from preprocessing.samples_creation import create_samples
from preprocessing.splitting import split
from preprocessing.standardization import standardize
from .cleaning.last_day_removal import remove_last_day
from .cleaning.anomalies_removal import remove_anomalies


def preprocessing_ohio(dataset, subject, ph, hist, day_len, n_days_test):
    """
    OhioT1DM dataset preprocessing pipeline:
    loading -> samples creation -> cleaning (1st) -> splitting -> cleaning (2nd) -> standardization

    First cleaning is done before splitting to speedup the preprocessing

    :param dataset: name of the dataset, e.g. "ohio"
    :param subject: id of the subject, e.g. "559"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 288 (1440/5)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """
    data = load_ohio(dataset, subject)
    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers


def preprocessing_t1dms(dataset, subject, ph, hist, day_len, n_days_test):
    """
    T1DMS dataset preprocessing pipeline (valid for adult, adolescents and children):
    loading -> samples creation -> splitting -> standardization

    :param dataset: name of the dataset, e.g. "t1dms"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """
    data = load_t1dms(dataset, subject, day_len)
    data = scaling_T1DMS(data)
    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers

def preprocessing_sap100(dataset, subject, ph, hist, day_len, n_days_test):
    """
    Tidepool SAP100 dataset preprocessing pipeline:
    ?

    :param dataset: name of the dataset, e.g. "sap100"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """
    data = load_sap100(dataset, subject)
    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    # print("Printing heads of split dataset")
    # print("Train")
    # print(train[0].iloc[100:110])
    # print("Valid")
    # print(valid[0].iloc[100:110])
    # print("Test")
    # print(test[0].iloc[100:110])
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)

    return train, valid, test, scalers

def preprocessing_sap100_1y(dataset, subject, ph, hist, day_len, n_days_test):
    """
    Tidepool SAP100 dataset preprocessing pipeline:
    Only take the last one year + 60 days of data (60 test days)
    
    Errors out if there is not enough data.

    :param dataset: name of the dataset, e.g. "sap100"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """

    data = load_sap100(dataset, subject)

    # Take the last 365+60 days of data
    data = data.iloc[-(365+60)*1440//cs.freq:]
    
    if data.shape[0] < (365+60)*1440//cs.freq:
        print("Tried to take the last 365+60 days of data, but there was not enough data for subject " + subject)
        raise ValueError("Not enough data for subject " + subject)

    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers

def preprocessing_sap100_4m(dataset, subject, ph, hist, day_len, n_days_test):
    """
    Tidepool SAP100 dataset preprocessing pipeline:
    Only take the last 4 months + 60 days of data (60 test days)
    
    Errors out if there is not enough data.

    :param dataset: name of the dataset, e.g. "sap100"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """

    data = load_sap100(dataset, subject)

    # Take the last 4 months+60 days of data
    data = data.iloc[-(122+60)*1440//cs.freq:]
    
    if data.shape[0] < (122+60)*1440//cs.freq:
        print("Tried to take the last 122+60 days of data, but there was not enough data for subject " + subject)
        raise ValueError("Not enough data for subject " + subject)

    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers

def preprocessing_sap100_6w(dataset, subject, ph, hist, day_len, n_days_test):
    """
    Tidepool SAP100 dataset preprocessing pipeline:
    Only take the last 6 weeks + 60 days of data (60 test days)
    
    Errors out if there is not enough data.

    :param dataset: name of the dataset, e.g. "sap100"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """

    data = load_sap100(dataset, subject)

    # Take the last 6 weeks+60 days of data
    data = data.iloc[-(42+60)*1440//cs.freq:]
    
    if data.shape[0] < (42+60)*1440//cs.freq:
        print("Tried to take the last 42+60 days of data, but there was not enough data for subject " + subject)
        raise ValueError("Not enough data for subject " + subject)

    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers

def preprocessing_sap100_6w_gap(dataset, subject, ph, hist, day_len, n_days_test):
    """
    Tidepool SAP100 dataset preprocessing pipeline:
    Modification of the 6w pipeline to mimic the idea that you train your model once,
    and then use it for a long period of time.
    Take the 6 weeks of data from the beginning of the timeframe covered in sap100_1y, 
    and the same 60 days of test data.
    
    Errors out if there is not enough data.

    :param dataset: name of the dataset, e.g. "sap100"
    :param subject: id of the subject, e.g. "1"
    :param ph: prediction horizon, e.g. 30
    :param hist: history length, e.g. 60
    :param day_len: length of a day normalized by sampling frequency, e.g. 1440 (1440/1)
    :return: training_old folds, validation folds, testing folds, list of scaler (one per fold)
    """

    data = load_sap100(dataset, subject)

    # Take correct data as described in doc string
    data = pd.concat([data.iloc[-(365+60)*1440//cs.freq : -(365+60-42)*1440//cs.freq], data.iloc[-60*1440//cs.freq :]])
    
    if data.shape[0] < (42+60)*1440//cs.freq:
        print("Tried to take data out of a 1 year + 60 day timeframe, but there was not enough data for subject " + subject)
        raise ValueError("Not enough data for subject " + subject)

    data = resample(data, cs.freq)
    data = create_samples(data, ph, hist, day_len)
    data = fill_nans(data, day_len, n_days_test)
    train, valid, test = split(data, day_len, n_days_test, cs.cv)
    [train, valid, test] = [remove_nans(set) for set in [train, valid, test]]
    train, valid, test, scalers = standardize(train, valid, test)
    return train, valid, test, scalers

# the sap100 preprocessing file might work for other tidepool datasets like PA50 and HCL150, I (Erin) don't know.
preprocessing_per_dataset = {
    "t1dms": preprocessing_t1dms,
    "t1dms_adult": preprocessing_t1dms,
    "t1dms_adolescent": preprocessing_t1dms,
    "t1dms_child": preprocessing_t1dms,
    "ohio": preprocessing_ohio,
    "sap100": preprocessing_sap100,
    "sap100_1y": preprocessing_sap100_1y,
    "sap100_4m": preprocessing_sap100_4m,
    "sap100_6w": preprocessing_sap100_6w,
    "sap100_6w_gap": preprocessing_sap100_6w_gap
}


def preprocessing(target_dataset, target_subject, ph, hist, day_len):
    """
    associate every dataset with a specific pipeline - which should be consistent with the others

    :param dataset: name of dataset (e.g., "ohio")
    :param subject: name of subject (e.g., "559")
    :param ph: prediction horizon in minutes (e.g., 5)
    :param hist: length of history in minutes (e.g., 60)
    :param day_len: typical length of a day in minutes standardized to the sampling frequency (e.g. 288 for 1440 min at freq=5 minutes)
    :return: train, valid, test folds
    """
    n_days_test = misc.datasets.datasets[target_dataset]["n_days_test"]
    return preprocessing_per_dataset[target_dataset](target_dataset, target_subject, ph, hist, day_len, n_days_test)

