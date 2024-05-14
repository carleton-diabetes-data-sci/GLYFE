'''

Code by Lucie Wolf, Spring 2024


Structure of test file system: 
    experiments:
        experiment_1 is DEC_8_2023
        experiment_2 is all_sap100
    models:
        model_1 is from base
        model_2 is from poly
    phs:
        ph_n1 is ph_30
        ph_n2 is 60

Note that ohio_559.txt is inentionally excluded in experiment_1,model_2,ph_n1 to ensure that it works 
even with that missing point.

I gave them fake names to make sure that no matter what changes happen in the future, the function works
regardless of ph names, experiments, models, etc.

'''

import pytest
import pandas as pd
import numpy as np

from interpret_outputs import *

# >>> Fixtures >>> #






# >>> Tests >>> #

def test_loop_all_files():
    dicts = loop_all_files(False)

    assert len(dicts) == 15






'''
# FIXTURES FOR addTimeColumns


# Fixtures for 'time' column for addTimeColumns
@pytest.fixture
def list_time_general():
    return ['2017-03-14T17:38:42.000Z', '2017-03-14T17:43:42.000Z', '2017-03-14T17:48:42.000Z', '2017-03-14T17:49:37.000Z']

@pytest.fixture
def list_time_unsorted():
    return ['2017-03-14T17:43:42.000Z', '2017-03-14T17:49:37.000Z', '2017-03-14T17:48:42.000Z', '2017-03-14T17:38:42.000Z']

@pytest.fixture
def list_time_inconsistent_format():
    return ['2017-03-14T17:38:42.000Z', '2017-03-14T17:43:42Z', '2017-03-14T17:48:42Z', '2017-03-14T17:49:37.000Z']

@pytest.fixture
def list_time_all():
    return ['2017-03-14T17:43:42Z', '2017-03-14T17:49:37.000Z', '2017-03-14T17:48:42Z', '2017-03-14T17:38:42.000Z']


# Fixtures for 'localTime' column for addTimeColumns
@pytest.fixture
def list_localTime_general():
    return [pd.to_datetime('2017-03-14T17:38:42'), pd.to_datetime('2017-03-14T17:43:42'), pd.to_datetime('2017-03-14T17:48:42'), pd.to_datetime('2017-03-14T17:49:37')]

@pytest.fixture
def list_localTime_unsorted():
    return [pd.to_datetime('2017-03-14T17:43:42'), pd.to_datetime('2017-03-14T17:49:37'), pd.to_datetime('2017-03-14T17:48:42'), pd.to_datetime('2017-03-14T17:38:42')]

@pytest.fixture
def list_localTime_local_is_not_utc():
    return [pd.to_datetime('2017-03-14T13:38:42'), pd.to_datetime('2017-03-14T13:43:42'), pd.to_datetime('2017-03-14T13:48:42'), pd.to_datetime('2017-03-14T13:49:37')]

@pytest.fixture
def list_localTime_all():
    return [pd.to_datetime('2017-03-14T13:43:42'), pd.to_datetime('2017-03-14T13:49:37'), pd.to_datetime('2017-03-14T13:48:42'), pd.to_datetime('2017-03-14T13:38:42')]



# Fixtures for other columns for addTimeColumns
@pytest.fixture
def list_utcTimezoneAware():
    return [pd.to_datetime('2017-03-14 17:38:42+00:00'), pd.to_datetime('2017-03-14 17:43:42+00:00'), pd.to_datetime('2017-03-14 17:48:42+00:00'), pd.to_datetime('2017-03-14 17:49:37+00:00')]

@pytest.fixture
def list_utcTime():
    return [pd.to_datetime('2017-03-14 17:38:42'), pd.to_datetime('2017-03-14 17:43:42'), pd.to_datetime('2017-03-14 17:48:42'), pd.to_datetime('2017-03-14 17:49:37'), ]

@pytest.fixture
def list_roundedLocalTime_local_is_not_utc():
    return [pd.to_datetime('2017-03-14T13:40:00'), pd.to_datetime('2017-03-14T13:45:00'), pd.to_datetime('2017-03-14T13:50:00'), pd.to_datetime('2017-03-14T13:50:00')]

@pytest.fixture
def list_roundedLocalTime_local_is_utc():
    return [pd.to_datetime('2017-03-14T17:40:00'), pd.to_datetime('2017-03-14T17:45:00'), pd.to_datetime('2017-03-14T17:50:00'), pd.to_datetime('2017-03-14T17:50:00')]



# Input dataframes for addTimeColumns
@pytest.fixture
def df_before_addTimeColumns_general(list_time_general, list_localTime_general):
    df = pd.DataFrame({'time': list_time_general,
                       'est.localTime': list_localTime_general
                       })
    return df

@pytest.fixture
def df_before_addTimeColumns_unsorted(list_time_unsorted, list_localTime_unsorted):
    df = pd.DataFrame({'time': list_time_unsorted,
                       'est.localTime': list_localTime_unsorted
                       })
    return df

@pytest.fixture
def df_before_addTimeColumns_local_is_not_utc(list_time_general, list_localTime_local_is_not_utc):
    df = pd.DataFrame({'time': list_time_general,
                       'est.localTime': list_localTime_local_is_not_utc
                       })
    return df

@pytest.fixture
def df_before_addTimeColumns_inconsistent_format(list_time_inconsistent_format, list_localTime_general):
    df = pd.DataFrame({'time': list_time_inconsistent_format,
                       'est.localTime': list_localTime_general
                       })
    return df

@pytest.fixture
def df_before_addTimeColumns_all(list_time_all, list_localTime_all):
    df = pd.DataFrame({'time': list_time_all,
                       'est.localTime': list_localTime_all
                       })
    return df

# Output dataframes for addTimeColumns
@pytest.fixture
def df_after_addTimeColumns_general(list_time_general, list_localTime_general, list_utcTimezoneAware, list_utcTime, list_roundedLocalTime_local_is_utc):
    df = pd.DataFrame({'time': list_time_general,
                       'est.localTime': list_localTime_general,
                       'localTime': list_localTime_general,
                       'utcTimezoneAware': list_utcTimezoneAware,
                       'utcTime': list_utcTime,
                       'roundedLocalTime': list_roundedLocalTime_local_is_utc
                       })
    return df

@pytest.fixture
def df_after_addTimeColumns_local_is_not_utc(list_time_general, list_localTime_local_is_not_utc, list_utcTimezoneAware, list_utcTime, list_roundedLocalTime_local_is_not_utc):
    df = pd.DataFrame({'time': list_time_general,
                       'est.localTime': list_localTime_local_is_not_utc,
                       'localTime': list_localTime_local_is_not_utc,
                       'utcTimezoneAware': list_utcTimezoneAware,
                       'utcTime': list_utcTime,
                       'roundedLocalTime': list_roundedLocalTime_local_is_not_utc
                       })
    return df

@pytest.fixture
def df_after_addTimeColumns_inconsistent_format(list_time_inconsistent_format, list_localTime_general, list_utcTimezoneAware, list_utcTime, list_roundedLocalTime_local_is_utc):
    df = pd.DataFrame({'time': list_time_inconsistent_format,
                       'est.localTime': list_localTime_general,
                       'localTime': list_localTime_general,
                       'utcTimezoneAware': list_utcTimezoneAware,
                       'utcTime': list_utcTime,
                       'roundedLocalTime': list_roundedLocalTime_local_is_utc
                       })
    return df

@pytest.fixture
def df_after_addTimeColumns_all(list_time_inconsistent_format, list_localTime_local_is_not_utc, list_utcTimezoneAware, list_utcTime, list_roundedLocalTime_local_is_not_utc):
    df = pd.DataFrame({'time': list_time_inconsistent_format,
                       'est.localTime': list_localTime_local_is_not_utc,
                       'localTime': list_localTime_local_is_not_utc,
                       'utcTimezoneAware': list_utcTimezoneAware,
                       'utcTime': list_utcTime,
                       'roundedLocalTime': list_roundedLocalTime_local_is_not_utc
                       })
    return df


### FIXTURES FOR removeNegativeColumnValues

@pytest.fixture
def list_other_column():
    return 

@pytest.fixture
def df_with_pos_col_vals(list_other_column):
    df = pd.DataFrame({'test_column': [np.nan, 2, 3, 4],
                       'test_column_2': list_other_column})
    return df

@pytest.fixture
def df_with_single_neg_col_val(list_other_column):
    df = pd.DataFrame({'test_column': [np.nan, -2, 2, 3, 4],
                       'test_column_2': list_other_column})
    return df

@pytest.fixture
def df_with_multiple_neg_col_vals(list_other_column):
    df = pd.DataFrame({'test_column': [np.nan, -2, 2, -10, 3, 4],
                       'test_column_2': list_other_column})
    return df

@pytest.fixture
def df_with_zero_col_vals(list_other_column):
    df = pd.DataFrame({'test_column': [np.nan, 0, 2, 3, 4],
                       'test_column_2': list_other_column})
    return df

@pytest.fixture
def df_with_no_col():
    df = pd.DataFrame({'test_column_2': [7.38249, -5, np.nan, 5.10669, np.nan]})
    return df


### FIXTURES FOR removeInvalidCgmValues

@pytest.fixture
def df_cgm_good():
    df = pd.DataFrame({'type': ['cbg', 'testing', 'basal', 'cbg', 'bolus'],
                       'value': [7.38249, -5, np.nan, 5.10669, np.nan]})
    return df

@pytest.fixture
def df_cgm_low():
    low = 26 / utils.MGDL_PER_MMOLL
    df = pd.DataFrame({'type': ['cbg', 'cbg', 'testing', 'basal', 'cbg', 'bolus'],
                       'value': [7.38249, low, -5, np.nan, 5.10669, np.nan]})
    return df

@pytest.fixture
def df_cgm_high():
    high = 432 / utils.MGDL_PER_MMOLL
    df = pd.DataFrame({'type': ['cbg', 'cbg', 'testing', 'basal', 'cbg', 'bolus'],
                       'value': [7.38249, high, -5, np.nan, 5.10669, np.nan]})
    return df

@pytest.fixture
def df_cgm_nan():
    df = pd.DataFrame({'type': ['cbg', 'testing', 'basal', 'cbg', 'bolus'],
                       'value': [np.nan, -5, np.nan, 5.10669, np.nan]})
    return df

@pytest.fixture
def df_cgm_multiple():
    low1 = 26 / utils.MGDL_PER_MMOLL
    low2 = 14 / utils.MGDL_PER_MMOLL
    high = 432 / utils.MGDL_PER_MMOLL
    df = pd.DataFrame({'type': ['cbg', 'cbg', 'cbg', 'testing', 'cbg', 'basal', 'cbg', 'bolus'],
                       'value': [7.38249, high, low1, -5, low2, np.nan, 5.10669, np.nan]})
    return df


### FIXTURES FOR set_up_dataframe

@pytest.fixture
def df_before_set_up_dataframe():
    low = 26 / utils.MGDL_PER_MMOLL
    high = 432 / utils.MGDL_PER_MMOLL

    df = pd.DataFrame({'time' : [
        '2016-04-22T05:08:57.000Z', '2016-04-22T04:48:58Z', '2016-04-22T04:58:57.000Z', '2016-04-22T05:23:57.000Z', '2016-04-22T05:13:57Z', '2016-04-22T05:18:57Z', '2016-04-22T04:53:57Z', '2016-04-22T05:28:57.000Z', '2016-04-22T02:14:53.000Z'
                        ],
                       'est.localTime' : [
        '2016-04-22T01:08:57', '2016-04-22T00:48:58', '2016-04-22T00:58:57', '2016-04-22T01:23:57', '2016-04-22T01:13:57', '2016-04-22T01:18:57', '2016-04-22T00:53:57', '2016-04-22T01:28:57', '2016-04-22T02:14:53'
                        ],
                        'duration' : [-1,        2,      9000000000,0,         -6,     10,        3,          np.nan,  4],
                        'type' :     ['cbg',     'cbg',  'cbg',     'test',    'test', 'upload',  'cbg',      'cbg',  'too_high'],
                        'value' :    [7.38249,   high,   low,       np.nan,    -5,      4,        5.10669,    np.nan,  4],
                        'test_col' : ['a',       'b',    'c',       'd',       'e',     'f',      'g',        'h',     'i']
                       })

    return df

@pytest.fixture
def df_after_set_up_dataframe():
    df = pd.DataFrame({'time' : ['2016-04-22T04:53:57Z', '2016-04-22T05:23:57.000Z', '2016-04-22T05:28:57.000Z'],
                       'est.localTime' : ['2016-04-22T00:53:57', '2016-04-22T01:23:57', '2016-04-22T01:28:57'],
                       'localTime': ['2016-04-22T00:53:57', '2016-04-22T01:23:57', '2016-04-22T01:28:57'],
                       'roundedLocalTime': [pd.to_datetime('2016-04-22T00:55:00'), pd.to_datetime('2016-04-22T01:25:00'), pd.to_datetime('2016-04-22T01:30')],
                       'utcTimezoneAware': [pd.to_datetime('2016-04-22T04:53:57+00:00'), pd.to_datetime('2016-04-22T05:23:57+00:00'), pd.to_datetime('2016-04-22T05:28:57+00:00')],
                       'utcTime': [pd.to_datetime('2016-04-22T04:53:57'), pd.to_datetime('2016-04-22T05:23:57'), pd.to_datetime('2016-04-22T05:28:57')],
                       'duration' : [3,    0,      np.nan],
                       'type' :     ['cbg',    'test', 'cbg'],
                       'value' :    [5.10669,    np.nan, np.nan,],
                       'test_col' : ['g',       'd',    'h']
                      })
    return df


# >>> Tests >>> #

# Tests for addTimeColumns

def test_addTimeColumns_format(df_before_addTimeColumns_general, df_after_addTimeColumns_general):
    """Test that the function has the correct number of columns and rows"""
    df = utils.addTimeColumns(df_before_addTimeColumns_general)

    assert len(df.columns) == 6
    assert len(df) == len(df_after_addTimeColumns_general)


def test_addTimeColumns_general(df_before_addTimeColumns_general, df_after_addTimeColumns_general):
    """Test that the function outputs the correct thing when the utc is the same timezone as the local timezone, the times are initially sorted, and the format is consistent"""
    df = utils.addTimeColumns(df_before_addTimeColumns_general)

    assert df['time'].equals(df_after_addTimeColumns_general['time'])
    assert df['est.localTime'].equals(df_after_addTimeColumns_general['est.localTime'])
    assert df['localTime'].equals(df_after_addTimeColumns_general['localTime'])
    assert df['utcTimezoneAware'].equals(df_after_addTimeColumns_general['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_addTimeColumns_general['utcTime'])
    assert df['roundedLocalTime'].equals(df_after_addTimeColumns_general['roundedLocalTime'])

def test_addTimeColumns_unsorted(df_before_addTimeColumns_unsorted, df_after_addTimeColumns_general):
    """Test that the function outputs the correct thing when the times are initially unsorted"""
    df = utils.addTimeColumns(df_before_addTimeColumns_unsorted)
    df = df.reset_index(drop=True)

    assert df['time'].equals(df_after_addTimeColumns_general['time'])
    assert df['est.localTime'].equals(df_after_addTimeColumns_general['est.localTime'])
    assert df['localTime'].equals(df_after_addTimeColumns_general['localTime'])
    assert df['utcTimezoneAware'].equals(df_after_addTimeColumns_general['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_addTimeColumns_general['utcTime'])
    assert df['roundedLocalTime'].equals(df_after_addTimeColumns_general['roundedLocalTime'])

def test_addTimeColumns_local_is_not_utc(df_before_addTimeColumns_local_is_not_utc, df_after_addTimeColumns_local_is_not_utc):
    """Test that the function outputs the correct thing when the local timezone is not the utc timezone"""
    df = utils.addTimeColumns(df_before_addTimeColumns_local_is_not_utc)
    df = df.reset_index(drop=True)

    assert df['time'].equals(df_after_addTimeColumns_local_is_not_utc['time'])
    assert df['est.localTime'].equals(df_after_addTimeColumns_local_is_not_utc['est.localTime'])
    assert df['localTime'].equals(df_after_addTimeColumns_local_is_not_utc['localTime'])
    assert df['utcTimezoneAware'].equals(df_after_addTimeColumns_local_is_not_utc['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_addTimeColumns_local_is_not_utc['utcTime'])
    assert df['roundedLocalTime'].equals(df_after_addTimeColumns_local_is_not_utc['roundedLocalTime'])

def test_addTimeColumns_inconsistent_format(df_before_addTimeColumns_inconsistent_format, df_after_addTimeColumns_inconsistent_format):
    """Test that the function outputs the correct thing when the format of the time sometimes contains nanoseconds but not always"""
    df = utils.addTimeColumns(df_before_addTimeColumns_inconsistent_format)

    print(df_before_addTimeColumns_inconsistent_format)
    print(df)
    print(df_after_addTimeColumns_inconsistent_format)

    assert df['time'].equals(df_after_addTimeColumns_inconsistent_format['time'])
    assert df['est.localTime'].equals(df_after_addTimeColumns_inconsistent_format['est.localTime'])
    assert df['localTime'].equals(df_after_addTimeColumns_inconsistent_format['localTime'])
    assert df['utcTimezoneAware'].equals(df_after_addTimeColumns_inconsistent_format['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_addTimeColumns_inconsistent_format['utcTime'])
    assert df['roundedLocalTime'].equals(df_after_addTimeColumns_inconsistent_format['roundedLocalTime'])

def test_addTimeColumns_all(df_before_addTimeColumns_all, df_after_addTimeColumns_all):
    """Test that the function outputs the correct thing when the local timezone is not the utc timezone, the times are initially unsorted, and the format of the time sometimes contains nanoseconds but not always"""
    df = utils.addTimeColumns(df_before_addTimeColumns_all)

    assert df['time'].equals(df_after_addTimeColumns_all['time'])
    assert df['est.localTime'].equals(df_after_addTimeColumns_all['est.localTime'])
    assert df['localTime'].equals(df_after_addTimeColumns_all['localTime'])
    assert df['utcTimezoneAware'].equals(df_after_addTimeColumns_all['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_addTimeColumns_all['utcTime'])
    assert df['roundedLocalTime'].equals(df_after_addTimeColumns_all['roundedLocalTime'])


# Tests for removeNegativeColumnValues

def test_removeNegativeColumnValues_no_neg(df_with_pos_col_vals):
    """Test that the function returns does nothing if all the column values are positive"""
    df, num_neg = utils.removeNegativeColumnValues(df_with_pos_col_vals, "test_column")
    assert df.equals(df_with_pos_col_vals)
    assert num_neg == 0

def test_removeNegativeColumnValues_one_neg(df_with_single_neg_col_val, df_with_pos_col_vals):
    """Test that a single negative column value is removed when there is only one, and only negative durations are removed"""
    df, num_neg = utils.removeNegativeColumnValues(df_with_single_neg_col_val, "test_column")
    df = df.reset_index(drop=True)
    assert df.equals(df_with_pos_col_vals)
    assert num_neg == 1

def test_removeNegativeColumnValues_multiple_neg(df_with_multiple_neg_col_vals, df_with_pos_col_vals):
    """Test that when multiple negative column values are present, all of them are removed, and only they are removed"""
    df, num_neg = utils.removeNegativeColumnValues(df_with_multiple_neg_col_vals, "test_column")
    df = df.reset_index(drop=True)
    assert df.equals(df_with_pos_col_vals)
    assert num_neg == 2

def test_removeNegativeColumnValues_zero_duration(df_with_zero_col_vals):
    """Test that nothing happens if there are column values of zero"""
    df, num_neg = utils.removeNegativeColumnValues(df_with_zero_col_vals, "test_column")
    assert df.equals(df_with_zero_col_vals)
    assert num_neg == 0

def test_removeNegativeColumnValues_no_duration(df_with_no_col):
    """Test that nothing happens if there is no column with the specified name"""
    df, num_neg = utils.removeNegativeColumnValues(df_with_no_col, "test_column")
    df = df.reset_index(drop=True)
    assert df.equals(df_with_no_col)


# Tests for removeInvalidCgmValues
    
def test_removeInvalidCgmValues_cgm_good(df_cgm_good):
    """Test that nothing happens if the cgm values are all valid"""
    df, num_removed = utils.removeInvalidCgmValues(df_cgm_good)
    assert df.equals(df_cgm_good)
    assert num_removed == 0

def test_removeInvalidCgmValues_cgm_low(df_cgm_low, df_cgm_good):
    """Test that the row is removed if the cgm values are low"""
    df, num_removed = utils.removeInvalidCgmValues(df_cgm_low)
    df = df.reset_index(drop=True)
    assert df.equals(df_cgm_good)
    assert num_removed == 1

def test_removeInvalidCgmValues_cgm_high(df_cgm_high, df_cgm_good):
    """Test that the row is removed if the cgm values are high"""
    df, num_removed = utils.removeInvalidCgmValues(df_cgm_high)
    df = df.reset_index(drop=True)
    assert df.equals(df_cgm_good)
    assert num_removed == 1

def test_removeInvalidCgmValues_cgm_multiple(df_cgm_multiple, df_cgm_good):
    """Test that multiple rows are removed if there are multiple bad cgm values"""
    df, num_removed = utils.removeInvalidCgmValues(df_cgm_multiple)
    df = df.reset_index(drop=True)
    assert df.equals(df_cgm_good)
    assert num_removed == 3

def test_removeInvalidCgmValues_cgm_nan(df_cgm_nan):
    """Test that nothing happens if a cgm value is nan"""
    df, num_removed = utils.removeInvalidCgmValues(df_cgm_nan)
    assert df.equals(df_cgm_nan)
    assert num_removed == 0


# Tests for set_up_dataframe

def test_set_up_dataframe_format(df_before_set_up_dataframe, df_after_set_up_dataframe):
    """Test that the function has the correct number of columns and rows"""
    df = set_up_dataframe(df_before_set_up_dataframe)

    assert len(df.columns) == len(df_after_set_up_dataframe.columns) # Same number of columns
    assert len(df) == len(df_after_set_up_dataframe) # Same number of rows


def test_set_up_dataframe_all(df_before_set_up_dataframe, df_after_set_up_dataframe):
    """Test that the function does everything it is meant to do with no conflicts between functions"""
    df = set_up_dataframe(df_before_set_up_dataframe)

    assert df['time'].equals(df_after_set_up_dataframe['time'])
    assert df['est.localTime'].equals(df_after_set_up_dataframe['est.localTime'])
    assert df['localTime'].equals(df_after_set_up_dataframe['localTime'])
    assert df['roundedLocalTime'].equals(df_after_set_up_dataframe['roundedLocalTime'])
    assert df['utcTimezoneAware'].equals(df_after_set_up_dataframe['utcTimezoneAware'])
    assert df['utcTime'].equals(df_after_set_up_dataframe['utcTime'])
    assert df['duration'].equals(df_after_set_up_dataframe['duration'])
    assert df['type'].equals(df_after_set_up_dataframe['type'])
    assert df['value'].equals(df_after_set_up_dataframe['value'])
    assert df['test_col'].equals(df_after_set_up_dataframe['test_col'])
'''