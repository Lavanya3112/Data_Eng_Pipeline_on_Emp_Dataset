import pandas as pd
import os

df = pd.read_csv(r"C:\Users\hp\Downloads\Employee_DE_Pipeline\Data\employee_raw_data.csv")

print("\nOriginal Data")
print(df.head())
print("Shape:", df.shape)

# Standardize Department
def standardize_department(value):
    if pd.isna(value):
        return "Unknown"
    v = str(value).strip().lower()
    if v in ["sales", "sale"]:
        return "Sales"
    if v in ["it", "i.t.", "information technology"]:
        return "IT"
    if v in ["hr", "h.r.", "human resources"]:
        return "HR"
    if v in ["finance", "fin"]:
        return "Finance"
    if v in ["marketing", "mktg"]:
        return "Marketing"
    return "Other"

df["department"] = df["department"].apply(standardize_department)
print("\nStandardize Department")
print(df["department"].unique())

# Standardize Work Mode
def standardize_work_mode(value):
    if pd.isna(value):
        return "Unknown"
    v = str(value).strip().lower()
    if v in ["remote", "wfh", "work from home"]:
        return "Remote"
    if v in ["hybrid"]:
        return "Hybrid"
    if v in ["onsite", "on-site", "office"]:
        return "Onsite"
    return "Other"

df["work_mode"] = df["work_mode"].apply(standardize_work_mode)
print("\nStandardize Work Mode")
print(df["work_mode"].unique())

# Standardize Gender
def standardize_gender(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    v = str(value).strip().lower()
    if v in ["male", "m"]:
        return "Male"
    if v in ["female", "f"]:
        return "Female"
    return "Other"

df["gender"] = df["gender"].apply(standardize_gender)
print("\nStandardize Gender")
print(df["gender"].unique())

# Standardize Education Level
def standardize_education(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    v = str(value).strip().lower()
    if v in ["bachelor's", "bachelors", "bsc", "bachelor"]:
        return "Bachelor's"
    if v in ["master's", "masters", "msc", "master"]:
        return "Master's"
    if v in ["phd", "ph.d.", "doctorate"]:
        return "PhD"
    if v in ["diploma", "dip"]:
        return "Diploma"
    return "Other"

df["education_level"] = df["education_level"].apply(standardize_education)
print("\nStandardize Education Level")
print(df["education_level"].unique())

# Handle Incorrect / Missing Numeric Entries
print("\nHandle Incorrect and Missing Numeric Values")

# experience_years: remove negative/incorrect values, then fill missing with median
df["experience_years"] = pd.to_numeric(df["experience_years"], errors="coerce")
df.loc[df["experience_years"] < 0, "experience_years"] = None
df["experience_years"] = df["experience_years"].fillna(df["experience_years"].median())

# salary: fill missing with median
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["salary"] = df["salary"].fillna(df["salary"].median())

# satisfaction_score: valid range is 1-5, fix out-of-range and missing
df["satisfaction_score"] = pd.to_numeric(df["satisfaction_score"], errors="coerce")
df.loc[df["satisfaction_score"] > 5, "satisfaction_score"] = None
df["satisfaction_score"] = df["satisfaction_score"].fillna(df["satisfaction_score"].median())

print(df.head())

# Remove Duplicates
print("\nRemove Duplicates")
before = len(df)
df = df.drop_duplicates(subset=["employee_id"]).reset_index(drop=True)
print(f"Removed {before - len(df)} duplicate rows")

# Save Cleaned Dataset
print("\nSave the Cleaned Dataset")

os.makedirs("Data/Cleaned_Data", exist_ok=True)

df.to_csv("Data/Cleaned_Data/employee_cleaned.csv", index=False)
df.to_json("Data/Cleaned_Data/employee_cleaned.json", orient="records", indent=4)
df.to_parquet("Data/Cleaned_Data/employee_cleaned.parquet")

print("Cleaned data saved successfully. Final shape:", df.shape)
