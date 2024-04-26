import pandas as pd
import numpy as np
import os
from pathlib import Path
import re

# Fill in which data to clean/merge into one
data = "data/new"
# Fill in which files should be cleaned/merged
filename = "metropolitan-stop-and-search"
# Fill in where cleaned/merged data should go
finished = "data/cleaned_merged"


def merging(dt = data, merging_on = filename, savelocation = finished):
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
merging()