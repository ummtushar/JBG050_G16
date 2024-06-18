import pandas as pd
from pathlib import Path
# needs raw data

custody_arrests_path = Path("../data/Final datasets raw/custody_arrests.csv")
df = pd.read_csv(custody_arrests_path, delimiter=";")

#merge year and month into one date column
df["date"] = pd.to_datetime(df["Arrest Year"].astype(str) + df["Arrest Month"].astype(str), format="%Y%m")

#drop year and month columns
df = df.drop(columns=["Arrest Year", "Arrest Month", "Arrest Month Name"])

# one hot encode the other columns
all_columns = list(df.columns)
all_columns.remove("date")
all_columns.remove("Arrest Count")
df = pd.get_dummies(df, columns= all_columns, dtype=int)

# compute the mean arrest count for each date
mean_arrests = df.groupby("date")["Arrest Count"].mean()
mean_arrests = mean_arrests.reset_index()

# rename the column
mean_arrests.columns = ["date", "mean_arrests"]

# aggregate the other columns
df.drop(columns=["Arrest Count"], inplace=True)
df = df.groupby("date").sum()
df = df.reset_index()

# merge the two dataframes
df = pd.merge(df, mean_arrests, on="date")

print(df.head())

# save the data
save_path = Path("data/Final datasets cleaned/custody_arrests_cleaned.csv")
df.to_csv(save_path, index=False)



