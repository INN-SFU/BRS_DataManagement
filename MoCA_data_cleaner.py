import pandas as pd
from datetime import datetime

# Define the cutoff date for your study
cutoff_date = datetime(2024, 10, 23)

# Read the CSV file into a pandas DataFrame
file_path = "/Users/brs/Documents/moca_downloads/desc-summary_date-250502_moca.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Ensure the date column is in datetime format
df['Test Date'] = pd.to_datetime(df.iloc[:, 3], format='%d-%m-%Y')

# Filter out rows with a test date before the cutoff date
filtered_df = df[df['Test Date'] >= cutoff_date]

# Overwrite the original file with the filtered data
filtered_df.to_csv(file_path, index=False)

print(f"The original file has been updated with the filtered data: {file_path}")