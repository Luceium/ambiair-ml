# Clean data

# This script cleans the data from the CSV file and fills in missing values

import pandas as pd
import numpy as np

def extract_time_features(df):
    """
    Extracts time features from the 'time' column in the dataframe.
    Converts the 'time' column stored as minutes since start of year to minutes, of day and day of year.
    Replaces the 'time' column with the new sin and cos cyclical features.
    """
    minutes_of_day = df['time'] % (24 * 60)
    day_of_year = df['time'] // (24 * 60)
    df['sin_minutes_of_day'] = np.sin(2 * np.pi * minutes_of_day / (24 * 60))
    df['cos_minutes_of_day'] = np.cos(2 * np.pi * minutes_of_day / (24 * 60))
    df['sin_day_of_year'] = np.sin(2 * np.pi * day_of_year / 365)
    df['cos_day_of_year'] = np.cos(2 * np.pi * day_of_year / 365)
    df.drop(columns=['time'], inplace=True)
    return df