import pandas as pd
import re
from datetime import datetime

# Load the TSV file into a pandas DataFrame with the correct encoding
file_path = '/Users/brs/Documents/psqi_downloads/desc-summary_date-250303_psqi.tsv'
df = pd.read_csv(file_path, sep='\t', encoding='ISO-8859-1')  # Try 'ISO-8859-1' encoding

# Define a function to check if a participant ID follows the correct format
def is_valid_participant_id(participant_id):
    # Ensure the ID is a string and matches the correct format
    if isinstance(participant_id, str):  # Only apply the regex if it's a string
        return bool(re.match(r'^BRS\d{4}$', participant_id))
    return False

# Remove rows with invalid participant IDs
df = df[df.iloc[:, 10].apply(is_valid_participant_id)]  # Column 11 is index 10 in Python

# Remove rows with participant ID "BRS9999"
df = df[df.iloc[:, 10] != 'BRS9999']

# Remove rows where participant ID is "BRS1234" and the date is before March 1st, 2025
def filter_brs1234_date(row):
    if row.iloc[10] == 'BRS1234':  # Access the 11th column by position (index 10)
        # Convert the date string to a datetime object
        try:
            date = datetime.strptime(row.iloc[11], '%d/%m/%Y')  # Access the 12th column by position (index 11)
            # Compare the date with March 1st, 2025
            return date >= datetime(2025, 3, 1)
        except ValueError:
            # If the date conversion fails, return False (remove the row)
            return False
    return True

df = df[df.apply(filter_brs1234_date, axis=1)]  # Apply the filtering function row-wise

# Overwrite the original file with the cleaned data
df.to_csv(file_path, sep='\t', index=False)

print("Data cleaning complete. Original file has been overwritten.")