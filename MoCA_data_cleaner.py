import pandas as pd
from datetime import datetime

# Function to standardize date field from MoCA csv file
def parse_mixed_date(date_str):
    if pd.isna(date_str):
        return pd.NaT

    date_str = str(date_str).strip()

    try:
        if "-" in date_str:
            # dd-mm-yyyy
            return pd.to_datetime(date_str, format="%d-%m-%Y")
        elif "/" in date_str:
            # mm/dd/yyyy
            return pd.to_datetime(date_str, format="%m/%d/%Y")
        else:
            return pd.NaT
    except ValueError:
        return pd.NaT

# Define the cutoff date for your study
cutoff_date = datetime(2024, 10, 23)

# Read the CSV file into a pandas DataFrame
file_path = "/Users/brs/Documents/moca_downloads/desc-summary_date-250502_moca.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Apply functon to your date column
df['Test Upload Date'] = df['Test Upload Date'].apply(parse_mixed_date)

# Ensure the date column is in datetime format
df['Test Date'] = pd.to_datetime(df.iloc[:, 3], format='%d-%m-%Y')

# Delete unnecessary spaces at the beginning of IDs
df['Institute File number'] = df['Institute File number'].str.strip()

# Remove 'sub-' part of the id, if exists
df['Institute File number'] = df['Institute File number'].str.replace('sub-', '')

# Filter out rows with a test date before the cutoff date
filtered_df = df[df['Test Date'] >= cutoff_date]
print(f"Before removing excluded participant IDs: {len(filtered_df)}")

# List of IDs to be removed
excluded_IDs = ['BRS0197', 'BRS0307', 'BRS0376']

# Remove rows that match with excluded IDs
filtered_df = filtered_df[~filtered_df['Institute File number'].isin(excluded_IDs)].reset_index(drop=True)

print(f"After removing excluded participant IDs: {len(filtered_df)}")

# Overwrite the original file with the filtered data
filtered_df.to_csv(file_path, index=False)
# Save to TSV with UTF-8 encoding
output_file = file_path.replace(".csv", ".tsv")
filtered_df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

print(f"The filtered data has been saved as a TSV: {output_file}")

print(f"The original file has been updated with the filtered data: {file_path}")