import pandas as pd
from pathlib import Path

EDA = False # set to True to show the head of each dataset
data_path = Path('data/Final datasets cleaned')
yearly_data = ['custody_arrests_cleaned.csv', 'employment_cleaned.csv', 'ethnic_groups_cleaned.csv']

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
all_boroughs = set()
for file in data_path.iterdir():
    if file.suffix != '.csv':
        continue
    df = pd.read_csv(file)
    print(file.name) 
    start_dates[file.name] = df['Date'].min()
    end_dates[file.name] = df['Date'].max()
    if 'Borough' in df.columns:
        all_boroughs.update(df['Borough'].unique())

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
print(main_df.head())
for file in data_path.iterdir():
    if file.suffix != '.csv':
        continue
    if file.name in yearly_data:
        continue
    if file.name == 'pas_cleaned.csv':
        continue
    df = pd.read_csv(file)
    #add the name of the file to the column names
    df.columns = [f'{file.stem}_{col}' if col not in ['Date', 'Borough'] else col for col in df.columns]

    # Create a MultiIndex with all combinations of dates and boroughs
    df = df.groupby(['Date', 'Borough']).sum().reset_index()
    multi_index = pd.MultiIndex.from_product([all_dates, all_boroughs], names=['Date', 'Borough'])

    # Reindex the DataFrame to include all combinations, filling missing values with 0
    #df = df.set_index(['Date', 'Borough']).reindex(multi_index, fill_value=0).reset_index()
    # Join the data to the main DataFrame
    main_df['Date'] = pd.to_datetime(main_df['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    main_df = pd.merge(main_df, df, on=['Date', 'Borough'], how='left')


for dataset in yearly_data:
    df = pd.read_csv(data_path / dataset)

    # If there are no boroughs, duplicate the data for each borough
    if 'Borough' not in df.columns:
        boroughs = all_boroughs
        boroughs_df = pd.DataFrame({'Borough': list(boroughs)})
        df = df.merge(boroughs_df, how='cross')

    #add the name of the file to the column names
    df.columns = [f'{dataset}_{col}' if col not in ['Date', 'Borough'] else col for col in df.columns]
    # Add duplicate the data for each month
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    months_df = pd.DataFrame({'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]})
    df = df.merge(months_df, how='cross')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    df.drop(columns=['Year', 'Month'], inplace=True)

    main_df['Date'] = pd.to_datetime(main_df['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    main_df = pd.merge(main_df, df, on=['Date', 'Borough'], how='left')

print(main_df.head())
main_df.to_csv(data_path / 'combined_data.csv', index=False)
# Final preperation for regression
# fill NA with column mean
main_df = pd.get_dummies(main_df, columns=['Borough'], drop_first=True, dtype=int)

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
target = 'Proportion Trust MPS_x'
target = 'Proportion Relied on to be there'

main_df.rename(columns={target: 'Y'}, inplace=True)


# Save the combined DataFrame
main_df.to_csv(data_path / 'combined_data.csv', index=False)
print(main_df)


