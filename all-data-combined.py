import pandas as pd

df1 = pd.read_csv('data/Borough-Table 1.csv', delimiter=';', decimal=",")
df2 = pd.read_csv('data/MPS Custody - Arrests - 2019 01 to 2024 03.csv', delimiter=';')

#processing the PAS dataset
df1 = df1.drop(columns = ['Survey', 'Measure', 'MPS', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'])
df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%y').dt.year

# #one hot and aggregation
df1= df1.groupby(['Date', 'Borough'], as_index=False).mean()
# df1 = df1.reset_index()



#processing the arrest dataset
df2 = df2.drop(columns = ['Arrest Month', 'Arrest Month Name'])
df2 = df2.rename(columns={'Ethnicity (4+1)': 'Ethnicity'})
df2 = df2.rename(columns= {'Arrest Year': 'Date'})
df2['Date'] = pd.to_datetime(df2['Date']).astype(str).str.extract(r'(\d{4})$')
df2['Date'] = pd.to_datetime(df2['Date']).dt.year


#One hot encoding and aggregation
df2 = pd.get_dummies(df2, columns = ['Gender', 'Age Group', 'Ethnicity', 'First Arrest Offnece', 'Domestic Abuse Flag'])
df2= df2.groupby('Date', as_index=False).mean()
# df2 = df2.reset_index()


#merged dataset
df_merged = pd.merge(df1, df2, on=['Date'])
df_merged = df_merged.fillna(0)

# print(df_merged.info)

######################################
#Further mergining with Custody Arrests

df3 = pd.read_csv("data/custody_arrests_cleaned(in).csv", delimiter=",")
df3 = df3.rename(columns= {'date': 'Date'})
df3['Date'] = pd.to_datetime(df3['Date'], format='%m/%d/%Y').dt.year

#One hot encoding and aggregation
df3= df3.groupby('Date', as_index=False).mean()

df_merged1 = pd.merge(df_merged, df3, on=['Date'])

# Drop any NaN values if necessary
df_merged1 = df_merged1.fillna(0)


# print(df_merged1.info)


########################################
#Further merging with Police Force Strength
df4 = pd.read_csv("data/Police_Force_Strength.csv", delimiter = ",")
df4['Date'] = pd.to_datetime(df4['Date'], format='%b-%y').dt.year

#One hot encoding and aggregation
df4= df4.groupby('Date', as_index=False).mean()

df_merged2 = pd.merge(df_merged1, df4, on=['Date'])

# Drop any NaN values if necessary
df_merged2 = df_merged2.fillna(0)


print(df_merged2.info)