import pandas as pd
from pathlib import Path

data_path = Path('data/Final datasets raw')
clean_data_path = Path('../data/Final datasets cleaned')

# Define the datasets that have been pre-processed propperly
time_spent_path = data_path / 'time_spent.csv'

# save the cleaned datasets
time_spent_cleaned_path = clean_data_path / 'time_spent_cleaned.csv'

if not clean_data_path.exists():
    clean_data_path.mkdir()

if not time_spent_cleaned_path.exists():
    time_spent = pd.read_csv(time_spent_path)
    time_spent.to_csv(time_spent_cleaned_path, index=False)


def clean_use_of_force(path):
    df = pd.read_csv(path)
    df.rename(columns={'IncidentDate': 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    return df

use_of_force_cleaned_path = clean_data_path / 'use_of_force_cleaned.csv'
if not use_of_force_cleaned_path.exists():
    use_of_force_path = data_path / 'use_of_force_cleaned.csv'
    use_of_force = clean_use_of_force(use_of_force_path)
    use_of_force.to_csv(use_of_force_cleaned_path, index=False)

# Cleaning granular data
def clean_granular_data(path):
    df = pd.read_csv(path)

    # define the regex string for cleaning the date it is now in (number) (apr 2020) format
    date_regex = r'\d+ \(([a-zA-Z]{3} \d{4})\)'
    df['Date'] = df['Month'].str.extract(date_regex)
    
    # convert the date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%b %Y')
    # drop the month column
    df.drop(columns=['Month'], inplace=True)

    # turn all columns except date and borough to dummy variables
    all_columns = df.columns
    columns_to_dummy = all_columns[~all_columns.isin(['Date', 'Borough'])]
    # encode as numeric
    df = pd.get_dummies(df, columns=columns_to_dummy, dtype=int)
    df = df.groupby(['Date', 'Borough']).mean().reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()

    return df

cleaned_granular_path = clean_data_path / 'granular_cleaned.csv'
if not cleaned_granular_path.exists():
    granular_path = data_path / 'granular_merged.csv'
    cleaned_granular = clean_granular_data(granular_path)
    cleaned_granular.to_csv(cleaned_granular_path, index=False)

def clean_strengths(path):
    df = pd.read_csv(path, delimiter=';', thousands=',')
    # drop the borough column
    df.drop(columns=['Business Group', 'OCU', 'Team'], inplace=True)
    df.rename(columns={'Department': 'Borough'}, inplace=True)
    df['Borough'] = df['Borough'].str.replace('Borough', '').str.strip()
    # unstack Rank and FTE
    df = df.groupby(['Date', 'Borough', 'Rank']).sum()
    df = df.unstack().reset_index()
    df.columns = df.columns.droplevel()

    # name the first column Date and the second Borough
    columns = ['Date', 'Borough', 'Rank Constable', 'Rank PSCO']
    df.columns = columns
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    return df


cleaned_strengths_path = clean_data_path / 'strengths_cleaned.csv'
if not cleaned_strengths_path.exists():
    strengths_path = data_path / 'Strengths.csv'
    cleaned_strengths = clean_strengths(strengths_path)
    cleaned_strengths.to_csv(cleaned_strengths_path, index=False)


def clean_pas(path):
    df = pd.read_csv(path, delimiter=';', thousands=',')
    df.drop(columns=['Survey', 'MPS', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], inplace=True)
    df = df.groupby(['Date', 'Borough', 'Measure']).mean()
    df = df.unstack().reset_index()
    #delete the first row
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    return df

clean_pas_path = clean_data_path / 'pas_cleaned.csv'
if not clean_pas_path.exists():
    pas_path = data_path / 'PAS.csv'
    cleaned_pas = clean_pas(pas_path)
    cleaned_pas.to_csv(clean_pas_path, index=False)

def clean_stops(path):
    df = pd.read_csv(path)
    df.rename(columns={'Borough of Stop': 'Borough'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Year_Month'], format='%Y-%m')
    df.drop(columns=['MPS Area', 'Borough Code', 'Count', 'Year_Month'], inplace=True)

    all_columns = df.columns
    columns_to_dummy = all_columns[~all_columns.isin(['Date', 'Borough'])]
    df = pd.get_dummies(df, columns=columns_to_dummy, dtype=int)
    df = df.groupby(['Date', 'Borough']).mean().reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    return df


clean_stops_path = clean_data_path / 'stops_cleaned.csv'
if not clean_stops_path.exists():
    stops_path = data_path / 'stops.csv'
    stops = clean_stops(stops_path)
    stops.to_csv(clean_stops_path, index=False)



def clean_custody_arrest(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['date'], format = '%m/%d/%Y')
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    df.drop(columns=['date'], inplace=True)
    return df
    

custody_arrest_cleaned_path = clean_data_path / 'custody_arrests_cleaned.csv'
if not custody_arrest_cleaned_path.exists():
    custody_arrest_path = data_path / 'custody_arrests_cleaned(in).csv' # This one does not have boroughs
    custody_arrest = clean_custody_arrest(custody_arrest_path)
    custody_arrest.to_csv(custody_arrest_cleaned_path, index=False)

def clean_employment(path):
    df = pd.read_csv(path, thousands=',')
    df['Date'] = pd.to_datetime(df['Year'], format='%Y')
    df.drop(columns=['Code', 'Year', 'Unnamed: 0'], inplace=True)
    df.rename(columns={'Area': 'Borough'}, inplace=True)
    return df

clean_employment_path = clean_data_path / 'employment_cleaned.csv'
if not clean_employment_path.exists():
    employment_path = data_path / 'employment-status.csv'
    employment = clean_employment(employment_path)
    employment.to_csv(clean_employment_path, index=False)

def clean_ethnic_groups(path):
    df = pd.read_csv(path, thousands=',')
    df['Date'] = pd.to_datetime(df['Date_Year'], format='%Y')
    df.drop(columns=['Date_Year', 'Code', 'Unnamed: 0'], inplace=True)
    df.rename(columns={'Area': 'Borough'}, inplace=True)
    # make all race columns numeric
    df['White'] = pd.to_numeric(df['White'], errors='coerce')
    df['Asian'] = pd.to_numeric(df['Asian'], errors='coerce')
    df['Black'] = pd.to_numeric(df['Black'], errors='coerce')
    df['Mixed/ Other'] = pd.to_numeric(df['Mixed/ Other'], errors='coerce')

    
    # add ratio columns
    df['White %'] = df['White'] / df['Total']
    df['Asian %'] = df['Asian'] / df['Total']
    df['Black %'] = df['Black'] / df['Total']
    df['Mixed/ Other %'] = df['Mixed/ Other'] / df['Total']
    return df

clean_ethnic_groups_path = clean_data_path / 'ethnic_groups_cleaned.csv'
if not clean_ethnic_groups_path.exists():
    ethnic_groups_path = data_path / 'ethnic-groups.csv'
    ethnic_groups = clean_ethnic_groups(ethnic_groups_path)
    ethnic_groups.to_csv(clean_ethnic_groups_path, index=False)

def clean_outcomes(path):
    df = pd.read_csv(path)
    df['Borough'] = df['LSOA name'].str.extract(r'([a-zA-Z ]+)')
    # strip the borough column
    df['Borough'] = df['Borough'].str.strip()
    df['Date'] = pd.to_datetime(df['Month'], format='%Y-%m')
    df.drop(columns=['Crime ID', 'Reported by', 'Falls within', 'Longitude', 'Latitude', 'Location', 'LSOA code', 'LSOA name', 'Month', 'Unnamed: 0'], inplace=True)
    df = pd.get_dummies(df, columns=['Outcome type'], dtype=int)
    # frop NA values
    df.dropna(inplace=True)
    # add a total column with only 1s
    df['Total'] = 1
    df = df.groupby(['Date', 'Borough']).sum().reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M').dt.to_timestamp()
    return df




clean_outcomes_path = clean_data_path / 'outcomes_cleaned.csv'
if not clean_outcomes_path.exists():
    outcomes_path = data_path / 'outcomes.csv'
    outcomes = clean_outcomes(outcomes_path)
    outcomes.to_csv(clean_outcomes_path, index=False)
