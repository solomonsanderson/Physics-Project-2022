'''Code for importing data from the provided data files'''


import pandas as pd


def load_data(path):
    '''Imports .data files.
    Parameters: 
     - path : the path of the file to be imported
    Returns:
     - Pandas data frame of the data file'''
    data = pd.read_csv(path, delim_whitespace = True , header=None)
    return data
    