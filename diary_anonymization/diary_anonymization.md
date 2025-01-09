# Instructions: Using sleepDiary_anonymization.py

This script processes a non-anonymized diary CSV file (from Qualtrics) for a **single participant** and creates an anonymized output CSV. The output includes the participant ID as the first column, followed by key columns of data extracted from the input file. No sensitive data should result in the output file.

Usage:
`python /path/to/sleepDiary_anonymization.py /path/to/example_non-anonymized_diary.csv participant_ID`

This command will generate `<participant_ID>_sleepDiary.csv` in your current working directory (the directory you run the python command from).
