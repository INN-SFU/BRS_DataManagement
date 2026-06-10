import pandas as pd
# Read the CSV file without specifying dtype initially
file_path = '/Users/cjimenez/Documents/BRS/DataManagement/Data_Transfer/Completeness-files/data_completeness_downloads/data_completeness_date-20260525.csv'

# List of IDs to be removed
excluded_IDs = ['sub-BRS0197', 'sub-BRS0307', 'sub-BRS0376']

# Read the CSV 
df = pd.read_csv(file_path)
print(f"Before removing excluded participant IDs: {len(df)}")

# Define column indexes for anonymizing excluded rows
id_idx = 0
datetime_idx = 1
columns_range = range(2, 14)

# Create mask based on ID column
mask = df.iloc[:, id_idx].isin(excluded_IDs)

# Apply -1 to selected non-datetime columns
df.iloc[mask, columns_range] = -1

# Apply NaT to datetime column
df.iloc[mask, datetime_idx] = pd.NaT

# Save cleaned data to a new TSV file with UTF-8 encoding
output_file = file_path.replace(".csv", ".tsv")
df.to_csv(output_file, sep="\t", index=False, encoding="utf-8")

print(f"Data cleaning complete. Saved to {output_file}")