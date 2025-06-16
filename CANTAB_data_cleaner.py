import pandas as pd

# Read the CSV file without specifying dtype initially
file_path = '/Users/brs/Documents/cantab_downloads/desc-summary_date-20250612_cantab.csv'

# Read the CSV to get the column names first
df = pd.read_csv(file_path)

# Specify the dtype for the Participant ID column (assuming it's column 5, index 4)
dtype_spec = {df.columns[4]: str}  # Adjust index if the Participant ID column is different

# Now read the CSV again with the specified dtype for the Participant ID column
df = pd.read_csv(file_path, dtype=dtype_spec)

# Columns 19 to 23 (0-indexed, so columns 18 to 22)
columns_to_check = df.columns[18:23]

# Remove rows where all columns 19 to 23 have the value 'NOT_RUN'
df_cleaned = df[~df[columns_to_check].eq('NOT_RUN').all(axis=1)]

# Remove all data in Columns 6 and 7 (index 5 and 6) except for the header
df_cleaned[df_cleaned.columns[5]] = None  # Column 6 (index 5)
df_cleaned[df_cleaned.columns[6]] = None  # Column 7 (index 6)

# Save the cleaned data back to the same CSV file (overwrite the original)
df_cleaned.to_csv(file_path, index=False)

print(f"Original file has been replaced with the cleaned data: {file_path}")