import pandas as pd
from data_analysis import analyze_data

def preprocess_data():
    data = analyze_data()

    # Drop any rows with null values
    data.dropna(axis=0, how='any', inplace=True)
    
    return data

# preprocess_data()

