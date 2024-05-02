import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


df1 = pd.read_csv('data/Borough-Table 1.csv', delimiter=';', decimal=",")
df2 = pd.read_csv('data/MPS Custody - Arrests - 2019 01 to 2024 03.csv', delimiter=';')

df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%y').dt.year
# df1['Date'] = pd.to_datetime(df1['Date'])
df2 = df2.rename(columns= {'Arrest Year': 'Date'})

df2['Date'] = pd.to_datetime(df2['Date']).astype(str).str.extract(r'(\d{4})$')
df2['Date'] = pd.to_datetime(df2['Date']).dt.year

#processing the PAS dataset
df1 = df1.drop(columns = ['Survey', 'MPS', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'])
# df1 = df1.groupby(by = ['Date', 'Borough', 'Measure']).mean()
# df1 = df1.loc[2019:,:]
# print(df1.head())
# print(df1.dtypes)

#processing the arrest dataset
df2 = df2.drop(columns = ['Arrest Month', 'Arrest Month Name', 'Gender', 'Age Group', 'Domestic Abuse Flag', 'First Arrest Offnece'])
df2 = df2.rename(columns={'Ethnicity (4+1)': 'Ethnicity'})
# df2 = df2.groupby(by=["Date", 'Ethnicity (4+1)']).mean()
# print(df2.head())
# print(df2.dtypes)


#merged dataset
df_merged = pd.merge(df1, df2, on=['Date'], how='outer')
df_merged = df_merged.dropna()
# print(df_merged.head())

# linear regression
boroughs = df_merged['Borough'].unique()

# One-Hot Encoding for 'Measure' column
df_merged = pd.get_dummies(df_merged, columns=['Measure'])
df_merged = pd.get_dummies(df_merged, columns=['Ethnicity'])

# # Label Encoding for 'Ethnicity' column
# le = LabelEncoder()
# df_merged['Ethnicity'] = le.fit_transform(df_merged['Ethnicity'])
# ethnicity_mapping = {index: label for index, label in enumerate(le.classes_)}

for borough in boroughs:
    df_borough = df_merged[df_merged['Borough'] == borough]
    
    X = df_borough.drop(['Proportion', 'Borough'], axis=1)
    y = df_borough['Proportion']

    # Normalize features on the X
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    # print(f"Score for {borough}: {model.score(X_test, y_test)}")

    #coeffcients
    print(f"Coefficients for {borough}: {model.coef_}")

    #MSE
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE for {borough}: {mse}\n")