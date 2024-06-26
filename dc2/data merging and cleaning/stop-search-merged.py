import pandas as pd
# needs raw

df_ss = pd.read_csv("../data/Final datasets raw/stop-and-search/Stops_LDS_Extract_24Months_.csv", delimiter = ",")
df_MPS = pd.read_csv("data/Final datasets raw/Borough-Table 1.csv", delimiter = ";", decimal=",")

df_ss = df_ss.rename(columns={"Borough of Stop": "Borough"})

merged_df = pd.merge(df_MPS, df_ss, on= "Borough")
# print(merged_df.head())
# print(merged_df.info())

merged_df.to_csv("data/Final datasets cleaned/Stop-and-Search-merged.csv", sep = ";", index=False)