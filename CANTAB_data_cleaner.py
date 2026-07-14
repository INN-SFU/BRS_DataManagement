import pandas as pd

IDs_correction_rules = [

    {
        "wrong_id": "1287",
        "correct_id": "0287",
        "registered_date": "2025.07.10 14:13:20",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": "1469",
        "correct_id": "0469",
        "registered_date": "2025.10.29 11:43:25",
        "reason": "Typo in registered ID",
    },

    {
        "wrong_id": "5533",
        "correct_id": "0553",
        "registered_date": "2025.12.12 13:36:17",
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
def apply_correct_id(df, id_col='new subject ID', date_col='Visit Start (Local)', date_format='%Y.%m.%d %H:%M:%S'):
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

    df[date_col] = df[date_col].dt.strftime(date_format)

    return df

# Read the CSV file without specifying dtype initially
file_path = '/Users/brs/Documents/cantab_downloads/desc-summary_date-20250612_cantab.csv'

# Read the CSV to get the column names first
df = pd.read_csv(file_path)

# Specify the dtype for the Participant ID column (assuming it's column 6, index 5)
dtype_spec = {df.columns[5]: str}  # Adjust index if the Participant ID column is different

# Now read the CSV again with the specified dtype for the Participant ID column
df = pd.read_csv(file_path, dtype=dtype_spec)

fixed_df = apply_correct_id(df)

fixed_df['new subject ID'] = fixed_df['fixed_id']

fixed_df = fixed_df.drop(columns=['raw_id','fixed_id', 'id_resolution_reason'])

# Columns 19 to 23 (0-indexed, so columns 18 to 22)
columns_to_check = fixed_df.columns[18:23]

df_cleaned = fixed_df.copy()
# Remove rows where all columns 19 to 23 have the value 'NOT_RUN'
df_cleaned = fixed_df[~fixed_df[columns_to_check].eq('NOT_RUN').all(axis=1)]

# Remove all data in Columns 7 and 8 (index 6 and 7) except for the header
df_cleaned[df_cleaned.columns[6]] = None  # Column 7 (index 6)
df_cleaned[df_cleaned.columns[7]] = None  # Column 8 (index 7)

print(f"Before removing excluded participant IDs: {len(df_cleaned)}")

# List of IDs to be removed
excluded_IDs = ['0197', '0307', '0376', '0678']

# Remove rows that match with excluded IDs
df_cleaned = df_cleaned[~df_cleaned['new subject ID'].isin(excluded_IDs)].reset_index(drop=True)

print(f"After removing excluded participant IDs: {len(df_cleaned)}")

df_nodups = df_cleaned.drop_duplicates(subset='new subject ID', keep='last', inplace=False)

# Save the cleaned data back to the same CSV file (overwrite the original)
tsv_path = file_path.replace('.csv', '.tsv')
df_nodups.to_csv(tsv_path, sep='\t', index=False, encoding="utf-8")

print(f"Original file has been replaced with the cleaned data: {file_path}")