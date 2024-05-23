'''

Code by Lucie Wolf, Winter 2024

This code takes the outputs (such as RMSEs, MAPEs, etc.) from the outputs folder and puts them into 
a dataframe, then stores that dataframe in the csv file with a name specified on the command line

To run the code: 
    python interpret_outputs.py csv_name.csv --overwrite
        Use with caution. Overwrites the previous csv completely.
    python interpret_outputs.py csv_name.csv --append
        Suggested. Appends the new dictionaries to the previous csv, throws an error and does not continue if two dictionaries have the same experiment name.
    Exactly one of --overwrite or --append must be used.

    python interpret_outputs.py csv_name.csv --hide_file_errors
        This is an optional flag. If used, it will not show errors with specific files, though it will show any other errors.

'''

import pandas as pd
import ast
import os
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_name')
    parser.add_argument('--append', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--hide_file_errors', action='store_true')
    args = parser.parse_args()

    if args.csv_name[-4:] != '.csv':
        raise Exception('The file to save the pandas dataframe in must be a csv file and should end in ".csv".')

    if args.overwrite == args.append:
        raise Exception('Must have exactly one of the overwrite and append flags set.')
    
    if args.append and not os.path.exists(args.csv_name):
        raise Exception('Cannot append to a csv file that does not exist.')
    
    if args.overwrite:
        print(f"Overwriting previous dataframe at {args.csv_name}.")
    else:
        print(f"Adding to previous dataframe at {args.csv_name}.")
    
    return args.append, args.hide_file_errors, args.csv_name


def loopAllFiles(hide_file_errors, outer_dir=''):
    # Get a dictionary with a precise statistic with the run (including the experiment, model, ph, patient, etc.) 
    # and statistic-type as the key and numeric value as the value
    indices = []
    means = []
    stds = []
    for dir_path, _, file_names in os.walk(outer_dir+'experiments'): # outer_dir used if data is stored in subfolders, though currently it is not hence it is only used when running tests
        if 'outputs' not in dir_path: # We only want to look at the outputs folder, not the plots or other ones
            continue

        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            
            try:
                mean_dicts, std_dicts = processSingleFile(file_path) 
                # The two dictionaries outputted are the means and stds respectively
                
                for metric in mean_dicts.keys(): # The metrics should line up between the two dictionaries since they're from the same run, so we can just use one of them
                    indices.append(f'{file_path}/{metric}')
                    means.append(mean_dicts[metric])
                    stds.append(std_dicts[metric])
            
            except Exception as e: # If there was an error processing the file
                if not hide_file_errors:
                    print(f'Error with file: {file_path}.\nNo or invalid dictionaries/outputs found.')
                    print()
    return indices, means, stds


def processSingleFile(file_path):
    # Get the first dictionary from a specific txt file
    f = open(file_path, "r")
    output = f.read()
    f.close()

    # Get the dictionaries from the output string if there is an output string, otherwise do nothing
    start = output.rindex('(') + 1
    end = output.rindex(')')

    file_dicts = getDictsFromStr(output[start:end])
    return file_dicts # Note: throws an error if there are no dictionaries, the file doesn't exist, etc.


def getDictsFromStr(dicts_str):
    # Get all the dictionaries from one string of dictionaries (in this case, will return two)
    file_dicts = []

    # Get the indices of the start and end of each dictionary
    starts = getCharInds(dicts_str, '{')
    ends = getCharInds(dicts_str, '}')
    
    for i in range(len(starts)):
        start = starts[i]
        end = ends[i] + 1
        dict = ast.literal_eval(dicts_str[start:end])
        file_dicts.append(dict)
    
    return file_dicts


def getCharInds(s, char):
    # Get all the indices of a character in a string
    return [i for i, ltr in enumerate(s) if ltr == char]


def getIndexTuples(indices):
    # Get the index tuples for the dataframe from the dictionary key/file path
    tuples = []
    for index in indices:
        _, experiment, _, model, ph, population_patient, metric = index.split('/') # remove 'experiments' from the start, 'outputs' from middle and get info from the key

        ph = int(ph[3:]) # change from 'ph-n' to n
        population, patient = population_patient.split('_') # Get the population and patient id from the patient name
        patient = patient[:-4] # change from 'patient_id.txt' to 'patient_id'
        tuples.append(tuple([experiment, model, ph, population, patient, metric]))
    
    return tuples


def makeDataframe(indices, means, stds):
    # Make a single dataframe from the two big dictionaries
    tuples = getIndexTuples(indices)
    col_names = ['experiment', 'model', 'ph', 'population', 'patient', 'metric']
    df_index = pd.MultiIndex.from_tuples(tuples, names=col_names)
    df = pd.DataFrame({'mean' : means, 'std' : stds}, index=df_index)
    return df


def loadDataframe(csv_name):
    # Import the old dataframe from the csv file
    num_cols = len(pd.read_csv(csv_name).columns) # Get the total number of columns
    df = pd.read_csv(csv_name, index_col=list(range(num_cols - 2)))
    df.name = None
    return df


def combineDataframes(df1, df2):
    # Combine two dataframes, throwing an error if there is a conflict
    
    # Check for conflicts
    overlapping_indices = df1.index.intersection(df2.index)
    for index in overlapping_indices:
        if (abs(df1.loc[index]['mean'] - df2.loc[index]['mean']) >= 1e-10) or (abs(df1.loc[index]['std'] - df2.loc[index]['std']) >= 1e-10): # If more than very slightly off (potentially due to some small flukey error)
            e = f'''
            Conflict: {index} is in both the original and new dataframes but the values are different.
            
            Original value: {df1.loc[index]}.
            New value:      {df2.loc[index]}
            Difference:     {df1.loc[index] - df2.loc[index]}

            Aborting.'''
            raise Exception(e)

    # Combine the dataframes
    s_final = df1.combine_first(df2)
    return s_final


def main():
    appending, hide_file_errors, csv_name = parseArgs()

    indices, means, stds = loopAllFiles(hide_file_errors)
    df = makeDataframe(indices, means, stds)
    
    if appending:
        df_orig = loadDataframe(csv_name)
        df = combineDataframes(df_orig, df)
    
    df.to_csv(csv_name)
    

if __name__ == '__main__':
    main()