
# load the data
#data <- read.csv("data/Final datasets cleaned/no_multicollinearity.csv")
data <- read.csv("data/Final datasets cleaned/combined_data.csv")

# print the columns

# remove columns from the data to avoid multicollinearity
#columns_to_remove <- c(
#  "stops_cleaned_Age_Group_Unknown",
#  "stops_cleaned_Subject_Person",
#  "stops_cleaned_Reason.for.Stop_A.Stolen.property..s.1.PACE.",
#  "stops_cleaned_Outcome_1.No.further.action",
#  "stops_cleaned_Outcome.Reason_B.Drugs",
#  "stops_cleaned_Gender_F",
#  "stops_cleaned_Ethnic.Appearance.Code_0.Unknown",
#  "stops_cleaned_EA.Group_Other",
#  "stops_cleaned_Self.defined.Ethnicity.Code_O9.Any.other.et",
#  "stops_cleaned_SDE.Group_Other",
#  "time_spent_cleaned_Abstraction.Type_Not.Abstracted",
#  "granular_cleaned_Household_Other",
#  "granular_cleaned_Birth.country_UK",
#  "granular_cleaned_Disability_No",
#  "granular_cleaned_Religion_No.religion",
#  "granular_cleaned_Gender_Female",
#  "granular_cleaned_Age_Refused",
#  "granular_cleaned_Orientation_Refused",
#  "granular_cleaned_Ethnicity_Other",
#  "granular_cleaned_Qualification_Other",
#  "granular_cleaned_Employment_Other",
#  "use_of_force_cleaned_SubjectEthnicity_Other",
#  "custody_arrests_cleaned.csv_Gender_Female",
#  "custody_arrests_cleaned.csv_Age.Group_Not.Recorded",
#  "custody_arrests_cleaned.csv_Ethnicity..4.1._Other",
#  "custody_arrests_cleaned.csv_First.Arrest.Offnece_Other.Offence",
#  "custody_arrests_cleaned.csv_Domestic.Abuse.Flag_No",
#  "ethnic_groups_cleaned.csv_Mixed..Other..",
#  "Borough_Barnet",
#  "Year_2015"
#)

# data <- data[, !(names(data) %in% columns_to_remove)]

# remove the X column
data <- data[, -1]
print(names(data))



# perform a regression
m1 <- lm(data = data, formula = Y ~ .)
summary(m1)

