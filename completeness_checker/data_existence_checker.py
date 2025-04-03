import sys
import pandas as pd
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(
    description="Check the existence of various data files for BRS study."
)

# Define command-line arguments
parser.add_argument(
    "date_completeness", help="The date for the data completeness file (YYYYMMDD)."
)
parser.add_argument(
    "date_cantab", help="The date for the CANTAB summary file (YYYYMMDD)."
)
parser.add_argument(
    "date_psqi", help="The date for the PSQI summary file (YYYYMMDD)."
)
parser.add_argument(
    "date_moca", help="The date for the MoCA summary file (YYYYMMDD)."
)

# Parse arguments
args = parser.parse_args()

# Assign arguments to variables
desired_date_completeness = args.date_completeness
desired_date_cantab = args.date_cantab
desired_date_psqi = args.date_psqi
desired_date_moca = args.date_moca

# Load the CSV file into a DataFrame
file_name = f'~/projects/ctb-rmcintos/globus-share/BRS/staging/data_completeness_date-{desired_date_completeness}.tsv'  # Replace this with the actual filename format
df = pd.read_csv(file_name, sep='\t', header=0, encoding='latin1')

# Directory where the test files are stored
base_directory = '~/projects/ctb-rmcintos/globus-share/BRS/staging'

# Function to check if the file exists for each file type
def check_file_existence(participant_id, file_type):
    # Remove the prefix based on the file type
    if file_type == "CANTAB":
        # Remove the full "sub-BRS" prefix for CANTAB
        participant_id = int(participant_id.replace("sub-BRS", ""))
    elif file_type in ["MoCA", "PSQI"]:
        # Remove only the "sub-" prefix for MoCA and PSQI
        participant_id = participant_id.replace("sub-", "")
    
    # Define file naming conventions based on column and file type
    if file_type == "MST":
        file_name = f"{participant_id}/cognitive/{participant_id}_mst.txt"
        file_path = os.path.join(base_directory, file_name)
    elif file_type == "CANTAB":
        file_name = f"desc-summary_date-{desired_date_cantab}_CANTAB.tsv"  # Replace with actual date format
        file_path = os.path.join(base_directory, file_name)
        # Check if the participant_id exists in the CANTAB CSV
        try:
            cantab_df = pd.read_csv(file_path, sep='\t', header=0)
            if participant_id in cantab_df.iloc[:, 4].values:  # Column 5 (index 4) contains the participant_id
                return True
            else:
                return False
        except FileNotFoundError:
            return False
    elif file_type == "MoCA":
        file_name = f"desc-summary_date-{desired_date_moca}_MoCA.tsv"  # Replace with actual date format
        file_path = os.path.join(base_directory, file_name)
        # Check if the participant_id exists in the MoCA CSV
        try:
            moca_df = pd.read_csv(file_path, sep='\t', header=0)
            if participant_id in moca_df.iloc[:, 2].values:  # Column 3 (index 2) contains the participant_id
                return True
            else:
                return False
        except FileNotFoundError:
            return False
    elif file_type == "PSQI":
        file_name = f"desc-summary_date-{desired_date_psqi}_PSQI.tsv"  # Replace with actual date format
        file_path = os.path.join(base_directory, file_name)
        # Check if the participant_id exists in the PSQI CSV
        try:
            psqi_df = pd.read_csv(file_path, sep='\t', header=0, encoding='latin1')
            if participant_id in psqi_df.iloc[:, 10].values:  # Column 11 (index 10) contains the participant_id
                return True
            else:
                return False
        except FileNotFoundError:
            return False
    elif file_type == "SleepDiary":
        file_name = f"{participant_id}/sleep/sleepDiary/{participant_id}_sleepDiary.tsv"
        file_path = os.path.join(base_directory, file_name)
    elif file_type == "EEG.muse":
        file_name = f"{participant_id}/eeg/{participant_id}_task-rest_eeg.muse"
        file_path = os.path.join(base_directory, file_name)
    elif file_type == "EEG.edf":
        file_name = f"{participant_id}/eeg/{participant_id}_task-rest_eeg.edf"
        file_path = os.path.join(base_directory, file_name)
    
    return os.path.exists(file_path)

# Iterate through each row (participant)
for index, row in df.iterrows():
    participant_id = row['subject ID']
    
    # Check each test for the participant
    if row['MST (1=1, 0=0)'] == 1:  # Column 3 corresponds to mst.txt
        file_exists = check_file_existence(participant_id, "MST")
        if not file_exists:
            print(f"Warning: mst.txt for {participant_id} not found!")
        else:
            print(f"mst.txt for {participant_id} exists.")
    
    if row['CANTAB'] == 1:  # Column 4 corresponds to desc-summary_CANTAB.tsv
        file_exists = check_file_existence(participant_id, "CANTAB")
        if not file_exists:
            print(f"Warning: CANTAB entry for {participant_id} not found!")
        else:
            print(f"CANTAB entry for {participant_id} exists.")
    
    if row['MoCA'] == 1:  # Column 5 corresponds to desc-summary_MoCA.tsv
        file_exists = check_file_existence(participant_id, "MoCA")
        if not file_exists:
            print(f"Warning: MoCA entry for {participant_id} not found!")
        else:
            print(f"MoCA entry for {participant_id} exists.")
    
    if row['PSQI'] == 1:  # Column 6 corresponds to desc-summary_PSQI.tsv
        file_exists = check_file_existence(participant_id, "PSQI")
        if not file_exists:
            print(f"Warning: PSQI entry for {participant_id} not found!")
        else:
            print(f"PSQI entry for {participant_id} exists.")
    
    if row['Sleep Diary'] == 1:  # Column 6 corresponds to sleepDiary.tsv
        file_exists = check_file_existence(participant_id, "SleepDiary")
        if not file_exists:
            print(f"Warning: Sleep Diary for {participant_id} not found!")
        else:
            print(f"sleepDiary for {participant_id} exists.")
    
    if row['Muse EEG'] == 1:  # Column 7 corresponds to task-rest_eeg.muse
        file_exists = check_file_existence(participant_id, "EEG.muse")
        if not file_exists:
            print(f"Warning: task-rest_eeg.muse for {participant_id} not found!")
        else:
            print(f"task-rest_eeg.muse for {participant_id} exists.")

    if row['Muse EEG'] == 1:  # Column 7 corresponds to task-rest_eeg.edf
        file_exists = check_file_existence(participant_id, "EEG.edf")
        if not file_exists:
            print(f"Warning: task-rest_eeg.edf for {participant_id} not found!")
        else:
            print(f"task-rest_eeg.edf for {participant_id} exists.")
