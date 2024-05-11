import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

############################ LOADING THE DATA SETS ############################

df1 = pd.read_csv('data/Borough-Table 1.csv', delimiter=';', decimal=",")
df2 = pd.read_csv('data/MPS Custody - Arrests - 2019 01 to 2024 03.csv', delimiter=';')

#processing the PAS dataset
df1 = df1.drop(columns = ['Survey', 'MPS', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'])
df1['Date'] = pd.to_datetime(df1['Date'], format='%m/%d/%y').dt.year

#processing the arrest dataset
df2 = df2.drop(columns = ['Arrest Month', 'Arrest Month Name', 'Gender', 'Age Group', 'Domestic Abuse Flag', 'First Arrest Offnece'])
df2 = df2.rename(columns={'Ethnicity (4+1)': 'Ethnicity'})
df2 = df2.rename(columns= {'Arrest Year': 'Date'})
df2['Date'] = pd.to_datetime(df2['Date']).astype(str).str.extract(r'(\d{4})$')
df2['Date'] = pd.to_datetime(df2['Date']).dt.year

print("Data loaded and processed successfully")

#merged dataset
df_merged = pd.merge(df1, df2, on=['Date'], how='outer')
df_merged = df_merged.dropna()

print("Data merged successfully")

############################ TRAINING THE REGRESSION MODEL ############################
def trust_factors(df_merged, one_hot):
    '''
    df_merged: The merged dataset with at lest columns having Proportion and Boroughs
    one_hot: List of columns to be one-hot encoded
    '''
    boroughs = df_merged['Borough'].unique()

    borough_coefs = {}

    # One-Hot Encoding for 'Measure' column
    for i in one_hot:
        df_merged = pd.get_dummies(df_merged, columns=[i])

    for borough in boroughs:
        df_borough = df_merged[df_merged['Borough'] == borough]
        
        X = df_borough.drop(['Proportion', 'Borough'], axis=1)
        y = df_borough['Proportion']
        columns = X.columns

        # Normalize features on the X
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        #coeffcients
        borough_coefs[borough] = dict(zip(columns, model.coef_))
        print(f"Coefficients for {borough}: {dict(zip(columns, model.coef_))}") 

        #MSE
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"MSE for {borough}: {mse}\n")

    # # Plot coefficients for each borough
    # plt.figure(figsize=(15, 10))

    # fig, ax = plt.subplots()

    # for borough, coefs in borough_coefs.items():
    #     ax.bar(coefs.keys(), coefs.values(), label=borough)

    # ax.set_xlabel('Coefficient Name')
    # ax.set_ylabel('Coefficient Value')

    # # Set legend size
    # ax.legend(prop={'size': 6})

    # # Rotate x-axis labels
    # plt.xticks(rotation=45)

    # plt.show()


trust_factors(df_merged, ['Measure', 'Ethnicity'])