from pathlib import Path
import pandas as pd

data_path = Path("../data/Final datasets raw/use_of_force.csv")

# Read the data
use_of_force = pd.read_csv(data_path, delimiter=";")

# if IncidentDate IncidentTime Borough are the same, then data is duplicated drop the duplicate row
use_of_force = use_of_force.drop_duplicates(subset=['IncidentDate', 'IncidentTime', 'Borough'])

kept_cols = ["IncidentDate", "Borough", "CED Used", "Firearms Aimed", "SubjectEthnicity"]

# Keep only the columns we need
use_of_force = use_of_force[kept_cols]

# Turn the subject ethnicity column into a one-hot encoded column
use_of_force = pd.get_dummies(use_of_force, columns=["SubjectEthnicity"])

# Turn CED used into a binary column, if there is a string value
use_of_force["CED Used"] = use_of_force["CED Used"].apply(lambda x: 1 if type(x)==str else 0)

# Turn Firearms Aimed into a binary column
use_of_force["Firearms Aimed"] = use_of_force["Firearms Aimed"].apply(lambda x: 1 if x=="Yes" else 0)

# Add a column ForceUsed that is always 1
use_of_force["UseOfForceCount"] = 1

# group by date and borough
use_of_force = use_of_force.groupby(["IncidentDate", "Borough"]).sum().reset_index()
print(use_of_force.head())

save_path = Path("../data/Final datasets cleaned/use_of_force_cleaned.csv")
use_of_force.to_csv(save_path, index=False)
