import pandas as pd
# missing raw data

######################################
# merging PAS and Stop and search
df1 = pd.read_csv('../data/Final datasets raw/Borough-Table 1.csv', delimiter=';', decimal=",")
df2 = pd.read_csv('../data/Final datasets raw/stop-and-search/Stops_LDS_Extract_24Months_.csv', delimiter=',')

#processing the PAS dataset
df1 = df1.drop(columns = ['Survey', 'Measure', 'MPS', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'])
df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%y').dt.strftime('%b-%Y')

# aggregation
df1= df1.groupby(['Date', 'Borough'], as_index=False).mean()


#processing the stop and search dataset

df2 = df2.rename(columns= {'Borough of Stop': 'Borough', 'Year_Month': 'Date'})
df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m').dt.strftime('%b-%Y')

#One hot encoding and aggregation
df2 = df2.drop(columns=['Borough Code', 'Gender', 'Ethnic Appearance Code', 'EA Group', 'Self-defined Ethnicity Code', 'SDE Group', 'Count'])
df2 = pd.get_dummies(df2, columns = ['Age_Group', 'MPS Area', 'Search Type', 'Subject', 'Reason for Stop', 'Outcome', 'Outcome Reason'])
df2= df2.groupby(['Date', 'Borough'], as_index=False).mean()


#merged dataset
df_merged = pd.merge(df1, df2, on=['Date', 'Borough'])
df_merged = df_merged.fillna(0)

# print(df_merged.info)

######################################
#Further mergining with Custody Arrests

df3 = pd.read_csv("../data/Final datasets raw/custody_arrests_cleaned(in).csv", delimiter=",")
df3 = df3.rename(columns= {'date': 'Date'})
df3['Date'] = pd.to_datetime(df3['Date'], format='%m/%d/%Y').dt.strftime('%b-%Y')

#One hot encoding and aggregation
df3= df3.groupby('Date', as_index=False).mean()

df_merged1 = pd.merge(df_merged, df3, on=['Date'])

# Drop any NaN values if necessary
df_merged1 = df_merged1.fillna(0)


# print(df_merged1.info)


########################################
#Further merging with Police Force Strength
df4 = pd.read_csv("../data/Final datasets raw/Police_Force_Strength.csv", delimiter = ",")
df4['Date'] = pd.to_datetime(df4['Date'], format='%b-%y').dt.strftime('%b-%Y')

#One hot encoding and aggregation
df4= df4.groupby('Date', as_index=False).mean()

df_merged2 = pd.merge(df_merged1, df4, on=['Date'])

# Drop any NaN values if necessary
df_merged2 = df_merged2.fillna(0)


df_merged2.to_csv("../data/Arrest-PAS-stop&search-force-merged.csv", sep = ",", index=False)