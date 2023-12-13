import pandas as pd
import os
import ast


def loop_files():
    # Get all the dictionaries from the outputs folder
    all_dicts = {}
    for dir_path, _, file_names in os.walk('outputs'):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            file_dicts = process_txt(file_path)
            for (metric, val) in file_dicts.items():
                key_name = f'{file_path}/{metric}'
                all_dicts[key_name] = val
    return all_dicts

def process_txt(file_path):
    # Get the first dictionary from a specific txt file
    f = open(file_path, "r")
    output = f.read()
    f.close()

    # Get the dictionaries from the output string if there is an output string, otherwise do nothing
    try:
        start = output.rindex('(') + 1
        end = output.rindex(')')

        file_dicts = get_dicts_from_str(output[start:end])
        return file_dicts[0]
    
    except Exception as e:
        print('Error with file: ' + file_path)
        print(e)
        return {}

def get_dicts_from_str(dicts_str):
    # Get all the dictionaries from one string of dictionaries
    file_dicts = []

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

def get_index_tuples(all_dicts):
    tuples = []
    for key in all_dicts.keys():
        components = key.split('/')[1:]
        components[2] = components[2][3:] # change from ph-x to x
        components[3] = components[3][:-4] # change from patient.txt to patient
        tuples.append(tuple(components))
    return tuples

def make_df(all_dicts, col_names):
    tuples = get_index_tuples(all_dicts)
    col_names = ['model', 'experiment', 'ph', 'patient', 'metric']

    index = pd.MultiIndex.from_tuples(tuples, names=col_names)
    df = pd.Series(all_dicts.values(), index=index)
    return df

def main():
    all_dicts = loop_files()
    df = make_df(all_dicts, col_names)
    print(df)

if __name__ == '__main__':
    main()