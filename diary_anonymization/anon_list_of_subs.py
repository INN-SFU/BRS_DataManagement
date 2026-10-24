import subprocess
from pathlib import Path
import sys

# Ensure the script has the necessary command-line arguments
if len(sys.argv) < 2:
    print("Usage: python anon_list_of_subs.py </path/to/Batch_YYYYMMDD/folder>")
    sys.exit(1)

folder_path = sys.argv[1]

# Path to the text file containing subject IDs (one per line)
subject_file = Path(folder_path + '/subject_ids.txt')
script_path = Path(r"./sleepDiary_anonymization.py")
input_dir = Path(folder_path + '/deanonymized_sleep_diaries')
output_dir = Path(folder_path + '/anonymized_sleep_diaries')  # optional if your script saves elsewhere

# Make sure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Read subject IDs
with open(subject_file, "r") as f:
    subjects = [line.strip() for line in f if line.strip()]

# Loop over subjects and run the anonymization script
for subj in subjects:
    input_file = input_dir / f"{subj}_deanonymized_sleepDiary.tsv"
    # The second argument seems to be the subject ID (without path)
    command = ["python", str(script_path), str(input_file), str(output_dir), subj]
    
    print(f"Running: python sleepDiary_anonymization.py on {subj}_deanonymized_sleepDiary.tsv")
    subprocess.run(command)
