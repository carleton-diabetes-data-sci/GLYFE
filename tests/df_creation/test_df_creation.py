'''
Code by Lucie Wolf, Spring 2024

This code tests for the functions in interpret_outputs.py.

The structure of test file system is meant to copy that of the "experiments" folder as of Spring 2024.

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
WORKING_DIR = 'tests/df_creation/' # Directory where the test files are stored



# >>> Fixtures >>> #


# Main sample indices, means, and stds
@pytest.fixture
def sample_indices():
    return ['experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE',
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE',
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE'
            ]

@pytest.fixture
def sample_means():
    return [51.464559571687026,
            35.211841589707234,
            25.00442343701953,
            31.995583232902874,
            31.995003953425652,
            56.28985497890585
            ]

@pytest.fixture
def sample_stds():
    return [1.1845270394300722,
            0.5454520952270868,
            0.025546188842853097,
            0.17899414344108275,
            0.1789643924168278,
            0.08401195701551065
            ]


# Sample indices, means, and stds for only the DEC_8_2023 experiment
@pytest.fixture
def DEC_8_2023_indices():
    return ['experiments/DEC_8_2023/outputs/poly/ph_30/ohio_563.txt/RMSE',
            'experiments/DEC_8_2023/outputs/poly/ph_60/ohio_559.txt/MAPE',
            'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE',
            'experiments/DEC_8_2023/outputs/base/ph_60/ohio_563.txt/RMSE'
            ]

@pytest.fixture
def DEC_8_2023_means():
    return [51.464559571687026,
            35.211841589707234,
            25.00442343701953,
            33.673937846707574
            ]

@pytest.fixture
def DEC_8_2023_stds():
    return [1.1845270394300722,
            0.5454520952270868,
            0.025546188842853097,
            0.12846338940811253
            ]

# Sample indices, means, and stds for only the all_sap100 experiment
@pytest.fixture
def all_sap100_indices():
    return ['experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0ae3c.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE'
            ]

@pytest.fixture
def all_sap100_means():
    return [31.995583232902874,
            31.995003953425652,
            56.28985497890585,
            ]

@pytest.fixture
def all_sap100_stds():
    return [0.17899414344108275,
            0.1789643924168278,
            0.08401195701551065
            ]

# Sample indices, means, and stds for a subset of the data from both experiments
@pytest.fixture
def some_of_both_experiments_indices():
    return ['experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_30/sap100_0ae3c.txt/RMSE',
            'experiments/all_sap100/outputs/poly/ph_60/sap100_0a1f3.txt/RMSE'
            ]

@pytest.fixture
def some_of_both_experiments_means():
    return [25.00442343701953,
            31.995583232902874,
            56.28985497890585
            ]

@pytest.fixture
def some_of_both_experiments_stds():
    return [0.025546188842853097,
            0.17899414344108275,
            0.08401195701551065
            ]


# Sample indices, means, and stds for a subset of the data from DEC_8_2023, with some incorrect data

@pytest.fixture
def contradictory_of_DEC_8_2023_stds():
    return [1.1845270394300722,
            100000.5454520952270868,
            0.025546188842853097,
            0.12846338940811253
            ]


@pytest.fixture
def rounded_some_of_both_experiments_stds():
    return [0.0255461888429,
            0.1789941434411,
            0.0840119570155
            ]


@pytest.fixture
def sample_index_tuples():
    return [('DEC_8_2023','poly',30,'ohio','563','RMSE'),
            ('DEC_8_2023','poly',60,'ohio','559','MAPE'),
            ('DEC_8_2023','base',30,'ohio','559','RMSE'),
            ('all_sap100','poly',30,'sap100','0ae3c','RMSE'),
            ('all_sap100','poly',60,'sap100','0ae3c','RMSE'),
            ('all_sap100','poly',60,'sap100','0a1f3','RMSE')
            ]



# >>> Tests >>> #

def test_loopAllFiles():
    indices, means, stds = loopAllFiles(False, outer_dir=WORKING_DIR)
    sample_index = WORKING_DIR+'experiments/DEC_8_2023/outputs/base/ph_30/ohio_559.txt/RMSE'
    i = indices.index(sample_index)

    assert len(indices) == (NUM_METRICS * NUM_WORKING_FILES)
    assert abs(means[i] - 25.00442343701953) <= 1e-10
    assert abs(stds[i] - 0.025546188842853097) <= 1e-10


@pytest.mark.xfail
def test_processSingleFile_badDict():
    ''' Tests that an error is thrown when the txt file's dictionary is broken. '''
    processSingleFile(WORKING_DIR+'stats_files/bad_dict.txt')


@pytest.mark.xfail
def test_processSingleFile_didNotRun():
    ''' Tests that an error is thrown when the txt file does not contain a dictionary. '''
    processSingleFile(WORKING_DIR+'stats_files/did_not_run.txt')


def test_processSingleFile_successful():
    ''' Tests that a single file is successfully loaded when the file run was successful. '''
    list_file_dicts = processSingleFile(WORKING_DIR+'stats_files/successful.txt')

    assert len(list_file_dicts) == 2
    assert len(list_file_dicts[0].keys()) == 31
    assert len(list_file_dicts[1].keys()) == 31
    assert list_file_dicts[0]['RMSE'] == 25.00442343701953


def test_getIndexTuples(sample_indices, sample_index_tuples):
    ''' Tests that the index tuples are correctly extracted from the dictionary. '''
    output_index_tuples = getIndexTuples(sample_indices)

    assert len(output_index_tuples) == 6
    assert len(output_index_tuples[0]) == 6

    for tuple in output_index_tuples:
        assert tuple in sample_index_tuples


def test_makeDataframe(sample_index_tuples, sample_indices, sample_means, sample_stds):
    ''' Tests that dataframe made has the correct values. '''
    output_df = makeDataframe(sample_indices, sample_means, sample_stds)

    assert len(output_df) == 6
    for i in range(len(output_df)):
        real_mean = sample_means[i]
        found_mean = output_df['mean'][sample_index_tuples[i]]
        assert real_mean == found_mean

        real_std = sample_stds[i]
        found_std = output_df['std'][sample_index_tuples[i]]
        assert real_std == found_std
        


def test_loadDataframe(sample_indices, sample_means, sample_stds):
    ''' Tests that the dataframe loaded from a csv matches the original
    Note: relies on makeDataframe() working. '''
    output_df = makeDataframe(sample_indices, sample_means, sample_stds)
    output_df.to_csv(WORKING_DIR+'/test_dataframe.csv')

    loaded_df = loadDataframe(WORKING_DIR+'/test_dataframe.csv')
    os.remove(WORKING_DIR+'/test_dataframe.csv')

    assert len(output_df) == len(loaded_df)

    for i in range(len(output_df)):
        assert (output_df['mean'].iloc[i] - loaded_df['mean'].iloc[i]) < 1e-10
        assert (output_df['std'].iloc[i] - loaded_df['std'].iloc[i]) < 1e-10


def test_combineDataframes_sameDataframe(sample_indices, sample_means, sample_stds):
    ''' Tests that when the two dataframe are identical, nothing is changed.
    Note: relies on makeDataframe() working. '''
    df1 = makeDataframe(sample_indices, sample_means, sample_stds)
    df2 = makeDataframe(sample_indices, sample_means, sample_stds)
    df = combineDataframes(df1, df2)

    assert len(df) == len(df1)
    for i in range(len(df)):
        assert df['mean'].iloc[i] in df1['mean'].iloc
        assert df['std'].iloc[i] in df1['std'].iloc


def test_combineDataframes_nonoverlappingDataframes(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds, all_sap100_indices, all_sap100_means, all_sap100_stds):
    ''' Tests that when the two dataframes have no overlap whatsoever (for example, contain none of the same experiments), they are combined correctly. 
    Note: relies on makeDataframe() working. '''
    dec_df = makeDataframe(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds, )
    sap_df = makeDataframe(all_sap100_indices, all_sap100_means, all_sap100_stds, )
    df = combineDataframes(dec_df, sap_df)

    assert len(df) == len(dec_df) + len(sap_df)
    for i in range(len(dec_df)):
        assert dec_df['mean'].iloc[i] in df['mean'].iloc
        assert dec_df['std'].iloc[i] in df['std'].iloc
    for i in range(len(sap_df)):
        assert sap_df['mean'].iloc[i] in df['mean'].iloc
        assert sap_df['std'].iloc[i] in df['std'].iloc


def test_combineDataframes_overlappingDataframes(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds, some_of_both_experiments_indices, some_of_both_experiments_means, some_of_both_experiments_stds):
    ''' Tests that when the two dataframes have some non-contradictory overlap (for example, contain some the same experiments but with matching data), they are combined correctly. 
    Note: relies on makeDataframe() working. '''
    dec_df = makeDataframe(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds)
    mix_df = makeDataframe(some_of_both_experiments_indices, some_of_both_experiments_means, some_of_both_experiments_stds)
    df = combineDataframes(dec_df, mix_df)

    for i in range(len(dec_df)):
        assert dec_df['mean'].iloc[i] in df['mean'].iloc
        assert dec_df['std'].iloc[i] in df['std'].iloc
    for i in range(len(mix_df)):
        assert mix_df['mean'].iloc[i] in df['mean'].iloc
        assert mix_df['std'].iloc[i] in df['std'].iloc


@pytest.mark.xfail
def test_combineDataframes_contradictoryDataframes(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds, contradictory_of_DEC_8_2023_stds):
    ''' Tests that when the two dataframes have some contradictory overlap (for example, contain some the same experiments but with non-matching data), an error is thrown.
    Note: relies on makeDataframe() working. '''
    dec_df = makeDataframe(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds)
    bad_df = makeDataframe(DEC_8_2023_indices, DEC_8_2023_means, contradictory_of_DEC_8_2023_stds)
    combineDataframes(dec_df, bad_df)


def test_combineDataframes_floatingPointErrorDataframe(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds, some_of_both_experiments_indices, some_of_both_experiments_means, rounded_some_of_both_experiments_stds):
    ''' Tests that when the two series have some overlap with slight difference, it does not have an error.
    Note: relies on makeDataframe() working. '''
    dec_df = makeDataframe(DEC_8_2023_indices, DEC_8_2023_means, DEC_8_2023_stds)
    off_df = makeDataframe(some_of_both_experiments_indices, some_of_both_experiments_means, rounded_some_of_both_experiments_stds)
    df = combineDataframes(dec_df, off_df)

    rounded_dec_df = dec_df.round(10)
    rounded_off_df = off_df.round(10)
    rounded_df = df.round(10)

    for i in range(len(dec_df)):
        assert rounded_dec_df['mean'].iloc[i] in rounded_df['mean'].iloc
        assert rounded_dec_df['std'].iloc[i] in rounded_df['std'].iloc
    for i in range(len(off_df)):
        assert rounded_off_df['mean'].iloc[i] in rounded_df['mean'].iloc
        assert rounded_off_df['std'].iloc[i] in rounded_df['std'].iloc