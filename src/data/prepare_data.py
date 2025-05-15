# Clean data

# This script cleans the data from the CSV file and fills in missing values

import pandas as pd
import numpy as np

def add_time_features(df : pd.DataFrame) -> pd.DataFrame:
    """
    Extracts time features from the 'time' column in the dataframe.
    Converts the 'time' column stored as minutes since start of year to minutes, of day and day of year.
    Replaces the 'time' column with the new sin and cos cyclical features.
    """
    
    if 'sin_minutes_of_day' in df.columns and 'cos_minutes_of_day' in df.columns and 'sin_day_of_year' in df.columns and 'cos_day_of_year' in df.columns:
        return df
    if 'time' not in df.columns:
        raise ValueError("The DataFrame does not contain a 'time' column.")

    minutes_of_day = df['time'] % (24 * 60)
    day_of_year = df['time'] // (24 * 60)
    df['sin_minutes_of_day'] = np.sin(2 * np.pi * minutes_of_day / (24 * 60))
    df['cos_minutes_of_day'] = np.cos(2 * np.pi * minutes_of_day / (24 * 60))
    df['sin_day_of_year'] = np.sin(2 * np.pi * day_of_year / 365)
    df['cos_day_of_year'] = np.cos(2 * np.pi * day_of_year / 365)
    df.drop(columns=['time'], inplace=True)
    return df

def add_temp_diff(df : pd.DataFrame) -> pd.DataFrame:
    """
    Adds a new column 'temp_diff' to the dataframe, which is the difference between 'indoor-temp' and 'outdoor-temp'.
    """

    if 'temp_diff' in df.columns:
        return df
    if 'indoor-temp' not in df.columns or 'outdoor-temp' not in df.columns:
        raise ValueError("The DataFrame does not contain 'indoor-temp' or 'outdoor-temp' columns.")

    df['temp_diff'] = df['indoor-temp'] - df['outdoor-temp']
    return df

def add_rolling_features(df : pd.DataFrame, window_size: int = 5) -> pd.DataFrame:
    """
    Adds rolling features to the dataframe.
    The rolling features are the mean and standard deviation of 'indoor-temp', 'outdoor-temp', and 'temp_diff' over the last `window_size` time steps.
    """

    if 'rolling_mean_indoor_temp' in df.columns and 'rolling_std_indoor_temp' in df.columns:
        return df
    if 'indoor-temp' not in df.columns or 'outdoor-temp' not in df.columns or 'temp_diff' not in df.columns:
        raise ValueError("The DataFrame does not contain 'indoor-temp', 'outdoor-temp', or 'temp_diff' columns.")

    df['rolling_mean_indoor_temp'] = df['indoor-temp'].rolling(window=window_size).mean()
    df['rolling_std_indoor_temp'] = df['indoor-temp'].rolling(window=window_size).std()
    df['rolling_mean_outdoor_temp'] = df['outdoor-temp'].rolling(window=window_size).mean()
    df['rolling_std_outdoor_temp'] = df['outdoor-temp'].rolling(window=window_size).std()
    df['rolling_mean_temp_diff'] = df['temp_diff'].rolling(window=window_size).mean()
    df['rolling_std_temp_diff'] = df['temp_diff'].rolling(window=window_size).std()
    return df

def add_lagged_features(df : pd.DataFrame, lag: int = 1) -> pd.DataFrame:
    """
    Adds lagged features to the dataframe.
    The lagged features are the values of 'indoor-temp', 'outdoor-temp', and 'temp_diff' at the previous `lag` time steps.
    """

    if 'lagged_indoor_temp' in df.columns and 'lagged_outdoor_temp' in df.columns and 'lagged_temp_diff' in df.columns:
        return df
    if 'indoor-temp' not in df.columns or 'outdoor-temp' not in df.columns or 'temp_diff' not in df.columns:
        raise ValueError("The DataFrame does not contain 'indoor-temp', 'outdoor-temp', or 'temp_diff' columns.")

    df['lagged_indoor_temp'] = df['indoor-temp'].shift(lag)
    df['lagged_outdoor_temp'] = df['outdoor-temp'].shift(lag)
    df['lagged_temp_diff'] = df['temp_diff'].shift(lag)
    return df