import pandas as pd
from datetime import datetime

IDs_correction_rules = [

    {
        "wrong_id": 'BRS0190',
        "correct_id":'BRS0196',
        "registered_date": "5/30/2025  12:26:14",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": 'BRS0281',
        "correct_id":'BRS0280',
        "registered_date": "7/24/2025  10:25:30",
        "reason": "Typo in registered ID",
    }

]

# Define a function to TBA
def normalize_ids(value: str) -> str:
    return (
        str(value)
        .strip()
        .upper()
        .replace(" ", "")
    )

# Define a function to TBA
def apply_correct_id(df, id_col='QID1', date_col='RecordedDate'):
    df = df.copy()
    
    df["raw_id"] = df[id_col].astype(str)

    df["fixed_id"] = df[id_col].apply(normalize_ids)

    df["id_resolution_reason"] = "original"

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    print(df[date_col])

    for rule in IDs_correction_rules:
        rule_date = pd.to_datetime(rule["registered_date"], errors="coerce")

        print(f"Wrong ID: {rule["wrong_id"]}")
        print(f"Correct ID: {rule["correct_id"]}")
        print(f"Date: {rule_date}")

        mask = (
            (df[id_col] == normalize_ids(rule["wrong_id"])) &
            (df[date_col] == rule_date)
        )

        print(df[mask])

        df.loc[mask, "fixed_id"] = normalize_ids(rule["correct_id"])
        df.loc[mask, "id_resolution_reason"] = rule["reason"]

    #df[date_col] = df[date_col].dt.strftime(date_format)

    return df

# Load the CSV file
input_file = "/Users/cjimenez/Documents/BRS/DataManagement/Data_Transfer/Completeness-files/bdigad_downloads/desc-summary_date-20260428_bdigad.csv"
df = pd.read_csv(input_file, encoding="utf-8")
print(f"Initial number of rows: {len(df)}")

fixed_df = apply_correct_id(df)

export_df = fixed_df.copy()
export_df['QID1'] = export_df['fixed_id']

export_df = export_df.drop(columns=['raw_id','fixed_id', 'id_resolution_reason'])

# Rename BDI columns Q46–Q66 to QBDI1–QBDI21
bdi_cols = [f"Q{q}" for q in range(46, 67)]
bdi_renamed = {old: f"QBDI{i+1}" for i, old in enumerate(bdi_cols)}

# Rename BAI (GAD-7) columns Q68_1–Q68_7 to QGAD1–QGAD7
gad_cols = [f"Q68_{i}" for i in range(1, 8)]
gad_renamed = {old: f"QGAD{i}" for i, old in enumerate(gad_cols)}

# Apply renaming
export_df.rename(columns={**bdi_renamed, **gad_renamed}, inplace=True)

# List of IDs to be removed
excluded_IDs = ['BRS0197', 'BRS0307', 'BRS0376']

# Remove rows that match with excluded IDs
export_df = export_df[~export_df.iloc[:, 10].isin(excluded_IDs)].reset_index(drop=True)
print(f"After excluded participant IDs: {len(export_df)}")

# Save to TSV with UTF-8 encoding
output_file = input_file.replace(".csv", ".tsv")
export_df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

print(f"Saved cleaned TSV file to {output_file}")
