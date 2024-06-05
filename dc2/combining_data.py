import pandas as pd
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor

EDA = False # set to True to show the head of each dataset
data_path = Path('data/Final datasets cleaned')
yearly_data = ['employment_cleaned.csv', 'ethnic_groups_cleaned.csv']

if EDA:
# print the head of each dataset
    for file in data_path.iterdir():
        if file.suffix != '.csv':
            continue
        print(file.name)
        df = pd.read_csv(file)
        print(df.head())
        print('\n')

# Get the start and end date of the datasets
start_dates = {}
end_dates = {}
for file in data_path.iterdir():
    if file.suffix != '.csv':
        continue
    df = pd.read_csv(file)
    print(file.name) 
    start_dates[file.name] = df['Date'].min()
    end_dates[file.name] = df['Date'].max()

min_date = min(start_dates.values())
max_date = max(end_dates.values())
all_dates = pd.date_range(min_date, max_date)

# print the min and max dates
print('\n')
for file, start_date in start_dates.items():
    print(f'{file} starts on {start_date}')

print('\n')
for file, end_date in end_dates.items():
    print(f'{file} ends on {end_date}')

pas_path = data_path / 'pas_cleaned.csv'
main_df = pd.read_csv(pas_path)
mistyped_boroughs = {
        'Barking And Dagenham': 'Barking and Dagenham',
        'City of Westminster': 'Westminster',
        'Hammersmith And Fulham': 'Hammersmith and Fulham',
        'Kensington And Chelsea': 'Kensington and Chelsea',
        'Kingston upon Thames': 'Kingston',
        'Kingston Upon Thames': 'Kingston',
        'Richmond upon Thames': 'Richmond',
        'Richmond Upon Thames': 'Richmond',
        'Hammersmith & Fulham': 'Hammersmith and Fulham',
        'Kensington & Chelsea': 'Kensington and Chelsea',
        'Barking & Dagenham': 'Barking and Dagenham',
}


main_df['Borough'] = main_df['Borough'].replace(mistyped_boroughs)
all_boroughs = main_df['Borough'].unique()
print(main_df.head())

custody_arrest_df = pd.read_csv(data_path / 'custody_arrests_cleaned.csv')
if 'Borough' not in custody_arrest_df.columns:
    boroughs_df = pd.DataFrame({'Borough': list(all_boroughs)})
    custody_arrest_df = custody_arrest_df.merge(boroughs_df, how='cross')
    # save the new DataFrame
    custody_arrest_df.to_csv(data_path / 'custody_arrests_cleaned.csv', index=False)


for file in data_path.iterdir():
    if file.suffix != '.csv':
        continue
    if file.name in yearly_data:
        continue
    if file.name == 'pas_cleaned.csv':
        continue
    if file.name == 'combined_data.csv':
        continue
    df = pd.read_csv(file)
    df['Borough'] = df['Borough'].replace(mistyped_boroughs)
    #add the name of the file to the column names
    df.columns = [f'{file.stem}_{col}' if col not in ['Date', 'Borough'] else col for col in df.columns]

    # Group all the dates to the nearest quarter
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.to_period('Q').dt.to_timestamp()
    df = df.groupby(['Date', 'Borough']).mean().reset_index()

    # Join the data to the main DataFrame
    main_df['Date'] = pd.to_datetime(main_df['Date'])
    main_df['Date'] = main_df['Date'].dt.to_period('Q').dt.to_timestamp()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.to_period('Q').dt.to_timestamp()
    print(file.name)
    print(df)
    main_df = pd.merge(main_df, df, on=['Date', 'Borough'], how='left')



for dataset in yearly_data:
    df = pd.read_csv(data_path / dataset)

    #add the name of the file to the column names
    df.columns = [f'{dataset}_{col}' if col not in ['Date', 'Borough'] else col for col in df.columns]
    # Add duplicate the data for each month
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    months_df = pd.DataFrame({'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]})
    df = df.merge(months_df, how='cross')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    df.drop(columns=['Year', 'Month'], inplace=True)

    # Group all the dates to the nearest quarter
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.to_period('Q').dt.to_timestamp()
    df = df.groupby(['Date', 'Borough']).mean().reset_index()

    # Join the data to the main DataFrame
    main_df['Date'] = pd.to_datetime(main_df['Date'])
    main_df['Date'] = main_df['Date'].dt.to_period('Q').dt.to_timestamp()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.to_period('Q').dt.to_timestamp()
    main_df = pd.merge(main_df, df, on=['Date', 'Borough'], how='left')

print(main_df.head())
main_df.to_csv(data_path / 'combined_data.csv', index=False)

lagged_columns = [
    "time_spent_cleaned_Abstraction Type_Aid",
    "time_spent_cleaned_Abstraction Type_CAD",
    "time_spent_cleaned_Abstraction Type_Court",
    "time_spent_cleaned_Abstraction Type_Custody",
    "time_spent_cleaned_Abstraction Type_Local Aid",
    "time_spent_cleaned_Abstraction Type_Not Abstracted",
    "time_spent_cleaned_Abstraction Type_Staffing Up",
    "time_spent_cleaned_Abstraction Type_Training",
    "use_of_force_cleaned_CED Used",
    "use_of_force_cleaned_Firearms Aimed",
#    "outcomes_cleaned_Outcome type_Formal action is not in the public interest",
#    "outcomes_cleaned_Outcome type_Investigation complete; no suspect identified",
#    "outcomes_cleaned_Outcome type_Local resolution",
#    "outcomes_cleaned_Outcome type_Offender given a caution",
#    "outcomes_cleaned_Outcome type_Offender given a drugs possession warning",
#    "outcomes_cleaned_Outcome type_Offender given penalty notice",
#    "outcomes_cleaned_Outcome type_Suspect charged",
#    "outcomes_cleaned_Outcome type_Suspect charged as part of another case",
#    "outcomes_cleaned_Outcome type_Unable to prosecute suspect",
#    "outcomes_cleaned_Total",
]

# Add a time lag for the lagged columns
borough_counts = len(all_boroughs)
for col in lagged_columns:
    # sort by date and boroughs
    main_df = main_df.sort_values(['Date', 'Borough'])
    main_df[f'{col}_lag'] = main_df[col].shift(borough_counts - 1)

# Final preperation for regression
# drop duplicates
# fill NA with column mean
main_df = pd.get_dummies(main_df, columns=['Borough'], drop_first=True, dtype=int)

# Add a binary column for covid
covid_start = pd.to_datetime('2020-03-26') # First day of lockdown
covid_end = pd.to_datetime('2021-07-19') # End of most legal limits
main_df['Covid'] = 0
main_df.loc[(main_df['Date'] >= covid_start) & (main_df['Date'] <= covid_end), 'Covid'] = 1


# Ensure 'Date' is in datetime format if needed and extract useful time-based features
main_df['Date'] = pd.to_datetime(main_df['Date'])
main_df['Year'] = main_df['Date'].dt.year
main_df['Month'] = main_df['Date'].dt.month
# make a dummy for the year
main_df = pd.get_dummies(main_df, columns=['Year', 'Month'], drop_first=True, dtype=int)

main_df.fillna(main_df.mean(), inplace=True)
# Add a date column in unix time
main_df['Date'] = pd.to_datetime(main_df['Date'])
main_df['Date'] = main_df['Date'].astype(int) / 10**9



# rename target to Y
target = 'Proportion Relied on to be there'

main_df.rename(columns={target: 'Y'}, inplace=True)

# Perform VIF to remove strongly colinear variables
main_X = main_df.copy()
vif_data = pd.DataFrame()
vif_data["feature"] = main_X.columns
vif_data["VIF"] = [variance_inflation_factor(main_X.values, i) for i in range(len(main_X.columns))]
print(vif_data)
vif_data = vif_data[vif_data["VIF"] < 10]

main_df = main_df[vif_data["feature"].values.tolist()]



# Save the combined DataFrame
main_df.to_csv(data_path / 'combined_data.csv', index=False)
print(main_df)


