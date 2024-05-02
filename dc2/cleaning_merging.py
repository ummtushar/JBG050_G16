import pandas as pd
import numpy as np
import os
from pathlib import Path
import re



def merging(dt, merging_on, savelocation):
    """
    Datafolder should contain folders for each month with some name format.
    Examples: {year}-{month}
    {year}_{month}
    Then within those folders the csv files to be merged should start with the same date format followed by what is in the file (aka which files should be merged), with a "-" in between
    Example: {date_format}-{filename}
    """
    list = os.listdir(Path(dt))
    df = pd.DataFrame()
    for i in range(len(list)):
        try:
            df_temp = pd.read_csv(f"{dt}/{list[i]}/{list[i]}-{merging_on}.csv")
            df_temp["Month"] = list[i]
            df = df._append(df_temp)
        except:
            print(f"{list[i]} {merging_on} does not exist")

    df.to_csv(Path(f"{savelocation}/merged-{merging_on}.csv"), sep=",")
    return df

# Fill in which data to clean/merge into one
data = "data/new"
# Fill in which files should be cleaned/merged
filename = "metropolitan-stop-and-search"
# Fill in where cleaned/merged data should go
finished = "data/cleaned_merged"
#merging(data, filename, finished)


def categorical_encode_and_expand(df, categorical, numeric):
    """
    df: dataframe
    categorical: name of the categorical column
    numeric: name of the numeric column
    """
    # in numeric columns replace all . with nothing and all , with .
    df[numeric] = df[numeric].apply(lambda x: re.sub(r'\.', '', x))
    df[numeric] = df[numeric].apply(lambda x: x.replace(',', '.'))

    # Create dummy variables for the categorical column
    df_encoded = pd.get_dummies(df, columns=[categorical])

    
    # Fill in the new columns with the numeric values
    for col in df_encoded.columns:
        if col.startswith(categorical + '_'):
            category = col.split('_')[-1]  # Extract category name from column name
            df_encoded[col] = df_encoded.apply(lambda row: float(row[numeric]) if row[categorical + '_' + category] == 1 else 0, axis=1)

    # Group by non-categorical columns and sum up values in categorical columns
    df_encoded.drop(columns=[numeric], inplace=True)
    non_categorical_cols = [col for col in df.columns if col != categorical and col != numeric]
    df_encoded = df_encoded.groupby(non_categorical_cols).sum()

    df_encoded.reset_index(inplace=True)

    return df_encoded

abstractions_path = Path("data/DWO Abstractions/Sheet1-Table 1.csv") 
df = pd.read_csv(abstractions_path, sep = ';')
df["Date"] = pd.to_datetime(df["Month of Abstraction"])
df["Date"] = df["Date"].dt.to_period('M').dt.to_timestamp()
# make date the first column
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
df = df.drop(columns = ["Month of Abstraction", "Abstracted From Duty", "Team", "BCU"])

# Remove the word "Borough" from the Borough column
df["Borough"] = df["Borough"].apply(lambda x: x.replace("Borough", "").strip())


categorical = "Abstraction Type"
numeric = "Abstraction Minutes"
time_spent_df = categorical_encode_and_expand(df, categorical, numeric)
print(time_spent_df.head())
#print(categorical_one_hot_encode(df, categorical, numeric))
attitude_path = Path("data/PAS.csv")
df = pd.read_csv(attitude_path, sep = ';')
df = df.drop(columns = ["Survey", "MPS", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9"])
df["Proportion"] = df["Proportion"].apply(lambda x: re.sub(r'\.', '', x))
df["Proportion"] = df["Proportion"].apply(lambda x: x.replace(',', '.'))
# format the date column to always be the first of the month
df["Date"] = pd.to_datetime(df["Date"])
df["Date"] = df["Date"].dt.to_period('M').dt.to_timestamp()
# Keep only the rows where Measure is "Trust MPS"
df = df[df["Measure"] == "Trust MPS"]
df = df.drop(columns = ["Measure"])
print(df.head())

merged_df = pd.merge(df, time_spent_df, on = ["Date", "Borough"])
print("MERGED DF")
print(merged_df.head())

# Perform a ridge regression on merged data, predictiong the "Porportion" column
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

merged_df.drop(columns = ["Date", "Borough"], inplace=True)

X = merged_df.drop(columns = ["Proportion"])
y = merged_df["Proportion"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
y_pred = ridge.predict(X_test)
print(mean_squared_error(y_test, y_pred))

# Print the coefficients with their corresponding column names as a dictionary
coefficients = dict(zip(X.columns, ridge.coef_))
print(coefficients)


