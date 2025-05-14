# Impute missing values
def impute_missing_values(df):
    """
    Imputes missing values in the DataFrame.
    """
    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)
    return df
