# /scripts/process_file.py
import pandas as pd

def read_asc_file(file_path):
    data = pd.read_csv(file_path, sep='\t', header=None, names=['Shift', 'Intensity'])
    return data['Shift'].tolist(), data['Intensity'].tolist()
