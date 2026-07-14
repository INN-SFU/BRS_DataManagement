import pandas as pd
import re
from datetime import datetime

IDs_correction_rules = [

    {
        "wrong_id": 'BRS0012',
        "correct_id":'BRS0011',
        "registered_date": "02/12/2024",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": 'BRS0072',
        "correct_id":'BRS0074',
        "registered_date": "27/02/2025",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": 'BRS0262',
        "correct_id":'BRS0162',
        "registered_date": "30/04/2025",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": 'BRS0533',
        "correct_id":'BRS0553',
        "registered_date": "12/12/2025",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": 'BRS0000',
        "correct_id":'BRS0575',
        "registered_date": "02/04/2026",
        "reason": "Typo in registered ID",
    }
]


def normalize_ids(value: str) -> str:
    return (
        str(value)
        .strip()
        .upper()
        .replace(" ", "")
    )


def apply_correct_id(df, id_col='QID1', date_col='QID2', date_format='%d/%m/%Y'):
    df = df.copy()
    
    df["raw_id"] = df[id_col].astype(str)

    df["fixed_id"] = df[id_col].apply(normalize_ids)

    df["id_resolution_reason"] = "original"

    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce").dt.normalize()

    for rule in IDs_correction_rules:
        rule_date = pd.to_datetime(rule["registered_date"], dayfirst=True). normalize()

        print(f"Wrong ID: {rule["wrong_id"]}")
        print(f"Correct ID: {rule["correct_id"]}")
        print(f"Date: {rule["registered_date"]}")

        mask = (
            (df[id_col] == normalize_ids(rule["wrong_id"])) &
            (df[date_col] == rule_date)
        )

        print(df[mask])

        df.loc[mask, "fixed_id"] = normalize_ids(rule["correct_id"])
        df.loc[mask, "id_resolution_reason"] = rule["reason"]

    df[date_col] = df[date_col].dt.strftime(date_format)

    return df

# Define a function to check if a participant ID follows the correct format
def is_valid_participant_id(participant_id):
    # Ensure the ID is a string and matches the correct format
    if isinstance(participant_id, str):  # Only apply the regex if it's a string
        return bool(re.match(r'^BRS\d{4}$', participant_id))
    return False

# Load the CSV file into a pandas DataFrame with the correct encoding
file_path = '/Users/brs/Documents/psqi_downloads/desc-summary_date-250303_psqi.tsv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try 'ISO-8859-1' encoding
print(f"Initial number of rows: {len(df)}")

fixed_df = apply_correct_id(df)

print(fixed_df.columns.tolist())

export_df = fixed_df.copy()
export_df['QID1'] = export_df['fixed_id']

export_df = export_df.drop(columns=['raw_id','fixed_id', 'id_resolution_reason'])

# List of IDs to be excluded
excluded_IDs = ['BRS0197', 'BRS0307', 'BRS0376']

# Remove rows with invalid participant IDs
export_df = export_df[export_df.iloc[:, 10].apply(is_valid_participant_id)]  # Column 11 is index 10 in Python
print(f"After removing invalid participant IDs: {len(export_df)}")

# Remove rows that match with excluded IDs
export_df = export_df[~export_df.iloc[:, 10].isin(excluded_IDs)].reset_index(drop=True)
print(f"After excluded participant IDs: {len(export_df)}")

# Remove rows with participant ID "BRS9999"
export_df = export_df[export_df.iloc[:, 10] != 'BRS9999']
print(f"After removing BRS9999: {len(export_df)}")

export_df = export_df[export_df.iloc[:, 10] != 'BRS1234']  # Apply the filtering function row-wise
print(f"After filtering BRS1234: {len(export_df)}")

export_df = export_df.drop_duplicates(subset='QID1', keep='last', inplace=False)

# Save cleaned data to a new TSV file with UTF-8 encoding
output_file = file_path.replace(".csv", ".tsv")
export_df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

print("Data cleaning complete. Original file has been overwritten.")