'''
Code by Lucie Wolf, Spring 2024

This code tests for the functions in interpret_outputs.py.

The structure of test file system is meant to copy that of the "experiments" folder as of 5/19/2024.

File exceptions to note: 
- ohio_559.txt is inentionally excluded from DEC_8_2023,poly,ph_30 to ensure that it works 
  even with that missing point
- There is a "plots" folder in all_sap100, which should be ignored by the code. It has a plot
  and some RMSEs in it, but they all should be ignored
- sap100_0a1f3.txt in all_sap100,base,ph_60 contains no dictionary, simulating did not run 
  successfully or some other error

Functions without tests:
- No tests for getDictsFromStr because it is so implicit in processSingleFile
- No tests for getCharInds because it is so straightforward
'''

import pytest
import pandas as pd
import numpy as np

from interpret_outputs import *

NUM_METRICS = 31 # RMSE, MAPE, etc.
NUM_WORKING_FILES = 14 # 2^4=16, but one file is intentionally excluded and another is intentionally broken
WORKING_DIR = 'tests/series_creation/' # Directory where the test files are stored



# >>> Fixtures >>> #

@pytest.fixture
def sample_big_stats_dict():
    return {'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/mean' : 51.464559571687026,
            'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/std' : 1.1845270394300722,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/mean' : 35.211841589707234,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/std' : 0.5454520952270868,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' : 25.00442343701953,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/std' : 0.025546188842853097,
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/mean' : 31.995583232902874,
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/std' : 0.17899414344108275,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE/mean' : 31.995003953425652,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE/std' : 0.1789643924168278,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/mean' : 56.28985497890585,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/std' : 0.08401195701551065
            }


@pytest.fixture
def DEC_8_2023_dict():
    return {'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/mean' : 51.464559571687026,
            'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/std' : 1.1845270394300722,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/mean' : 35.211841589707234,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/std' : 0.5454520952270868,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' : 25.00442343701953,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/std' : 0.025546188842853097,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/mean' : 33.673937846707574,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/std' : 0.12846338940811253
            }

@pytest.fixture
def all_sap100_dict():
    return {'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/mean' : 31.995583232902874,
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/std' : 0.17899414344108275,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE/mean' : 31.995003953425652,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE/std' : 0.1789643924168278,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/mean' : 56.28985497890585,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/std' : 0.08401195701551065
            }

@pytest.fixture
def some_of_both_experiments_dict():
    return {'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' : 25.00442343701953,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/std' : 0.025546188842853097,
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/mean' : 31.995583232902874,
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE/std' : 0.17899414344108275,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/mean' : 56.28985497890585,
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE/std' : 0.08401195701551065
            }


@pytest.fixture
def contradictory_of_DEC_8_2023_dict():
    return {'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/mean' : 51.464559571687026,
            'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/std' : 1.1845270394300722,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/mean' : 35.211841589707234,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/std' : 100000.5454520952270868,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' : 25.00442343701953,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/std' : 0.025546188842853097,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/mean' : 33.673937846707574,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/std' : 0.12846338940811253
            }
            
@pytest.fixture
def floating_point_error_of_DEC_8_2023_dict():
    return {'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/mean' : 51.4645595717,
            'experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE/std' : 1.1845270394301,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/mean' : 35.211841589707,
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE/std' : 0.54545209522709,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' : 25.00442343701953,
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/std' : 0.025546188842853097,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/mean' : 33.673937846708,
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE/std' : 0.12846338940811253
            }

@pytest.fixture
def sample_index_tuples():
    return [('DEC_8_2023','poly',30,'ohio','563','RMSE','mean'),
            ('DEC_8_2023','poly',30,'ohio','563','RMSE','std'),
            ('DEC_8_2023','poly',60,'ohio','559','MAPE','mean'),
            ('DEC_8_2023','poly',60,'ohio','559','MAPE','std'),
            ('DEC_8_2023','base',30,'ohio','559','RMSE','mean'),
            ('DEC_8_2023','base',30,'ohio','559','RMSE','std'),
            ('all_sap100','poly',30,'sap100','0ae3c','RMSE','mean'),
            ('all_sap100','poly',30,'sap100','0ae3c','RMSE','std'),
            ('all_sap100','poly',60,'sap100','0ae3c','RMSE','mean'),
            ('all_sap100','poly',60,'sap100','0ae3c','RMSE','std'),
            ('all_sap100','poly',60,'sap100','0a1f3','RMSE','mean'),
            ('all_sap100','poly',60,'sap100','0a1f3','RMSE','std')
            ]



# >>> Tests >>> #

def test_loopAllFiles():
    big_stats_dict = loopAllFiles(False, outer_dir=WORKING_DIR)

    assert len(big_stats_dict) == (NUM_METRICS * NUM_WORKING_FILES * 2)
    assert WORKING_DIR+'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean' in big_stats_dict.keys()
    assert big_stats_dict[WORKING_DIR+'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE/mean'] == 25.00442343701953


@pytest.mark.xfail
def test_processSingleFile_badDict():
    ''' Tests that an error is thrown when the txt file's dictionary is broken. '''
    processSingleFile(WORKING_DIR+'stats_files/bad_dict.txt')


@pytest.mark.xfail
def test_processSingleFile_didNotRun():
    ''' Tests that an error is thrown when the txt file does not contain a dictionary. '''
    processSingleFile(WORKING_DIR+'stats_files/did_not_run.txt')


def test_processSingleFile_successful():
    ''' Tests that a single file is successfully loaded when the file is successful. '''
    list_file_dicts = processSingleFile(WORKING_DIR+'stats_files/successful.txt')

    assert len(list_file_dicts) == 2
    assert len(list_file_dicts[0].keys()) == 31
    assert len(list_file_dicts[1].keys()) == 31
    assert list_file_dicts[0]['RMSE'] == 25.00442343701953


def test_getIndexTuples(sample_big_stats_dict, sample_index_tuples):
    ''' Tests that the index tuples are correctly extracted from the dictionary. '''
    output_index_tuples = getIndexTuples(sample_big_stats_dict)

    assert len(output_index_tuples) == 12
    assert len(output_index_tuples[0]) == 7

    for tuple in output_index_tuples:
        assert tuple in sample_index_tuples


def test_makeSeriesFromDict(sample_big_stats_dict, sample_index_tuples):
    ''' Tests that series made from the dictionary has matching values. '''
    output_s = makeSeriesFromDict(sample_big_stats_dict)

    assert len(output_s) == 12
    for i in range(len(sample_big_stats_dict.keys())):
        real_val = sample_big_stats_dict[list(sample_big_stats_dict.keys())[i]]
        found_val = output_s[sample_index_tuples[i]]
        assert real_val == found_val


def test_loadSeries(sample_big_stats_dict):
    ''' Tests that the series loaded from a csv matches the original
    Note: relies on test_makeSeriesFromDict working. '''
    output_s = makeSeriesFromDict(sample_big_stats_dict)
    output_s.to_csv(WORKING_DIR+'/test_series.csv')

    loaded_s = loadSeries(WORKING_DIR+'/test_series.csv')
    os.remove(WORKING_DIR+'/test_series.csv')

    assert len(output_s) == len(loaded_s)

    for i in range(len(output_s)):
        assert (output_s.iloc[i] - loaded_s.iloc[i]) < 1e-10


def test_combineSeries_sameSeries(sample_big_stats_dict):
    ''' Tests that when the two series are identical, nothing is changed.
    Note: relies on test_makeSeriesFromDict working. '''
    s1 = makeSeriesFromDict(sample_big_stats_dict)
    s2 = makeSeriesFromDict(sample_big_stats_dict)

    s = combineSeries(s1, s2)

    assert len(s) == len(s1)
    for i in range(len(s1)):
        assert s.iloc[i] == s1.iloc[i]


def test_combineSeries_nonoverlappingSeries(DEC_8_2023_dict, all_sap100_dict):
    ''' Tests that when the two series have no overlap whatsoever (for example, contain none of the same experiments), they are combined correctly. 
    Note: relies on test_makeSeriesFromDict working. '''
    dec_s = makeSeriesFromDict(DEC_8_2023_dict)
    sap_s = makeSeriesFromDict(all_sap100_dict)
    s = combineSeries(dec_s, sap_s)

    assert len(s) == len(dec_s) + len(sap_s)
    for i in range(len(dec_s)):
        assert dec_s.iloc[i] in s.iloc
    for i in range(len(sap_s)):
        assert sap_s.iloc[i] in s.iloc


def test_combineSeries_overlappingSeries(DEC_8_2023_dict, some_of_both_experiments_dict):
    ''' Tests that when the two series have some non-contradictory overlap (for example, contain some the same experiments but with matching data), they are combined correctly. Note: relies on test_makeSeriesFromDict working. '''
    dec_s = makeSeriesFromDict(DEC_8_2023_dict)
    mix_s = makeSeriesFromDict(some_of_both_experiments_dict)
    s = combineSeries(dec_s, mix_s)

    assert len(s) < len(dec_s) + len(mix_s)
    for i in range(len(dec_s)):
        assert dec_s.iloc[i] in s.iloc
    for i in range(len(mix_s)):
        assert mix_s.iloc[i] in s.iloc


@pytest.mark.xfail
def test_combineSeries_contradictorySeries(DEC_8_2023_dict, contradictory_of_DEC_8_2023_dict):
    ''' Tests that when the two series have some contradictory overlap (for example, contain some the same experiments but with non-matching data), an error is thrown.
    Note: relies on test_makeSeriesFromDict working. '''
    dec_s = makeSeriesFromDict(DEC_8_2023_dict)
    bad_s = makeSeriesFromDict(contradictory_of_DEC_8_2023_dict)
    combineSeries(dec_s, bad_s)


def test_combineSeries_floatingPointErrorSeries(DEC_8_2023_dict, floating_point_error_of_DEC_8_2023_dict):
    ''' Tests that when the two series have some contradictory overlap (for example, contain some the same experiments but with non-matching data), an error is thrown.
    Note: relies on test_makeSeriesFromDict working. '''
    dec_s = makeSeriesFromDict(DEC_8_2023_dict)
    ok_s = makeSeriesFromDict(floating_point_error_of_DEC_8_2023_dict)
    combineSeries(dec_s, ok_s)