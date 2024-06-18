import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

# outdated

# Pairplot to visualize relationships
data_path = Path('../data/Final datasets cleaned/combined_data.csv')
df = pd.read_csv(data_path)
#print(df.columns)
#sns.pairplot(df)
#plt.show()
#
## Correlation matrix to understand feature relationships
#corr_matrix = df.corr()
#sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
#plt.show()
# Convert categorical columns to numeric if necessary
# Example: If 'Borough' is a categorical feature, we encode it
# Handle missing values (if any)
# For simplicity, we'll drop rows with missing values, but other imputation methods can be used
df.fillna(0, inplace=True)
df = pd.get_dummies(df, columns=['Borough'], drop_first=True)

# Ensure 'Date' is in datetime format if needed and extract useful time-based features
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
# make a dummy for the year
df = pd.get_dummies(df, columns=['Year'], drop_first=True)

df['Month'] = df['Date'].dt.month
# Drop the original 'Date' column if it's not needed anymore
df.drop(columns=['Date'], inplace=True)

# rename target to Y
target = 'Proportion Trust MPS_x'
target = 'Proportion Relied on to be there'

df.rename(columns={target: 'Y'}, inplace=True)

# save the data
df.to_csv('data/Final datasets cleaned/combined_data_final.csv', index=False)


# Assuming 'Target' is the column we want to predict

X = df.drop(columns=[target])
y = df[target]

from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data and train the Lasso regression model
model = make_pipeline(StandardScaler(), Lasso(alpha=1.0))

# Fit the model
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Display the model coefficients
lasso = model.named_steps['lasso']
coefficients = pd.DataFrame(lasso.coef_, X.columns, columns=['Coefficient'])
standard_errors = pd.DataFrame(lasso.coef_, X.columns, columns=['Standard Error'])
print(coefficients)
coefficients_pvals = pd.DataFrame(lasso.coef_, X.columns, columns=['P-Value'])
print(coefficients_pvals)

# print the most important features
important_features = coefficients[coefficients['Coefficient'] != 0]
important_features = important_features.sort_values(by='Coefficient', ascending=False)
print(important_features[:15])

print(important_features)

