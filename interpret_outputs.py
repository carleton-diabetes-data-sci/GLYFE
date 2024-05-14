'''

Code by Lucie Wolf, Winter 2024

This code takes the outputs (such as RMSEs, MAPEs, etc.) from the outputs folder and puts them into a dataframe/series, then stores that dataframe in a csv file with a name given on the command line

To run the code: 
    python interpret_outputs.py csv_name.csv --overwrite
        Use with caution. Overwrites the previous dataframe completely.
    python interpret_outputs.py csv_name.csv --append
        Suggested. Appends the new dictionaries to the previous dataframe, throws an error and does not continue if two dictionaries have the same experiment name.
    Exactly one of --overwrite or --append must be used.

    python interpret_outputs.py csv_name.csv --hide_file_errors
        This is an optional flag. If used, it will not show errors with specific files, though it will show any other errors.

'''

import pandas as pd
import ast
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_name')
    parser.add_argument('--append', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--hide_file_errors', action='store_true')
    args = parser.parse_args()

    if args.csv_name[-4:] != '.csv':
        raise Exception('The file to save the dataframe in must be a csv file and should end in ".csv".')

    if args.overwrite == args.append:
        raise Exception('Must have exactly one of the overwrite and append flags set.')
    
    if args.overwrite:
        print(f"Overwriting previous dataframe at {args.csv_name}.")
    else:
        print(f"Adding to previous dataframe at {args.csv_name}.")
    
    return args.overwrite, args.hide_file_errors, args.csv_name


def loop_all_files(hide_file_errors):
    # Get all the dictionaries from the outputs folder
    dicts = {}
    for dir_path, _, file_names in os.walk('experiments'):
        if 'outputs' not in dir_path:
            continue

        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            
            try:
                mean_dicts, std_dicts = process_single_file(file_path) # The two dictionaries outputted are the means and stds respectively
                
                for metric in mean_dicts.keys():
                    key_name_mean = f'{file_path}/{metric}/mean'
                    key_name_std = f'{file_path}/{metric}/std'
                    dicts[key_name_mean] = mean_dicts[metric]
                    dicts[key_name_std] = std_dicts[metric]
            
            except Exception as e: # If there was an error processing the file
                if not hide_file_errors:
                    print(f'Error with file: {file_path}')
                    print('No dictionaries/outputs found')
                    print(e)
                    print()
    return dicts


def process_single_file(file_path):
    # Get the first dictionary from a specific txt file
    f = open(file_path, "r")
    output = f.read()
    f.close()

    # Get the dictionaries from the output string if there is an output string, otherwise do nothing
    start = output.rindex('(') + 1
    end = output.rindex(')')

    file_dicts = get_dicts_from_str(output[start:end])
    return file_dicts # Note: throws an error if there are no dictionaries, the file doesn't exist, etc.


def get_dicts_from_str(dicts_str):
    # Get all the dictionaries from one string of dictionaries
    file_dicts = []

    # Get the indices of the start and end of each dictionary
    starts = get_char_inds(dicts_str, '{')
    ends = get_char_inds(dicts_str, '}')
    
    for i in range(len(starts)):
        start = starts[i]
        end = ends[i] + 1
        dict = ast.literal_eval(dicts_str[start:end])
        file_dicts.append(dict)
    
    return file_dicts


def get_char_inds(s, char):
    # Get all the indices of a character in a string
    return [i for i, ltr in enumerate(s) if ltr == char]


def get_index_tuples(dicts):
    # Get the index tuples for the dataframe/series
    tuples = []
    for key in dicts.keys():
        _, model, experiment, ph, population_patient, metric, calculation = key.split('/') # remove 'outputs' from the start and split the file path by '/'

        ph = int(ph[3:]) # change from 'ph-n' to 'n'
        population, patient = population_patient.split('_') # Get the population and patient from the patient name
        patient = int(patient[:-4]) # change from 'patient.txt' to 'patient'
        tuples.append(tuple([model, experiment, ph, population, patient, metric, calculation]))
    
    return tuples


def make_df_from_dict(dicts):
    # Make a single dataframe/series from the dictionaries
    tuples = get_index_tuples(dicts)
    col_names = ['model', 'experiment', 'ph', 'population', 'patient', 'metric', 'calculation']

    df_index = pd.MultiIndex.from_tuples(tuples, names=col_names)
    df = pd.Series(dicts.values(), index=df_index)
    return df


def load_df(csv_name):
    # Import the old dataframe from the csv
    num_cols = len(pd.read_csv(csv_name).columns) # Get the total number of columns
    df = pd.read_csv(csv_name, index_col=list(range(num_cols - 1)))
    df = df.squeeze()
    df.name = None
    return df


def combine_dfs(df1, df2):
    # Combine two dataframes, throwing an error if there is a conflict
    
    # Check for conflicts
    overlapping_indices = df1.index.intersection(df2.index)
    for index in overlapping_indices:
        if abs(df1.loc[index] - df2.loc[index]) >= 10 ** -5: # if they are not the same value (or are slightly off since python struggles with exact values with floats)
            raise Exception(f'Conflict: {index} is in both dataframes but the values are different.')

    # Combine the dataframes
    df_final = df1.combine_first(df2)
    return df_final


def append_to_df(df_new, csv_name):
    # Append the new dataframe to the old dataframe
    try:
        df_old = load_df(csv_name)
        return combine_dfs(df_old, df_new)
    except Exception:
        print('No previous dataframe csv found. Creating new csv.')
        return df_new


def main():
    should_overwrite, hide_file_errors, csv_name = parse_args()

    all_dicts = loop_all_files(hide_file_errors)
    df = make_df_from_dict(all_dicts)
    
    if not should_overwrite:
        df = append_to_df(df, csv_name) 
    
    df.to_csv(csv_name)
    

if __name__ == '__main__':
    main()