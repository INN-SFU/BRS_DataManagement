# Instructions: Using [sleepDiary_anonymization.py](https://github.com/INN-SFU/BRS_DataManagement/blob/main/diary_anonymization/sleepDiary_anonymization.py)

This script processes a non-anonymized diary CSV file (from Qualtrics) for a **single participant** and creates an anonymized output CSV. The output includes the participant ID as the first column, followed by key columns of data extracted from the input file. No sensitive data should result in the output file.

Usage:
`python /path/to/sleepDiary_anonymization.py /path/to/example_non-anonymized_diary.csv participant_ID`

This command will generate `<participant_ID>_sleepDiary.csv` in your current working directory (the directory you run the python command from).

# Instructions: Using [append_column_to_qualtrics_diary.py](https://github.com/INN-SFU/BRS_DataManagement/blob/main/diary_anonymization/append_column_to_qualtrics_diary.py)

This script creates an additional "qualtrics_or_transcribed" column to a csv, with value "qualtrics" for each row. This intended for use with older anonymized CSV files (from qualtrics) for a **single participant** and overwrites the input CSV (which is an ouput of an older version of the sleepDiary_anonymization.py script). No other data in the file is altered. **Be sure to test this script on copies of input files before overwriting** 

Usage:
`python /path/to/sleepDiary_anonymization.py /path/to/example_non-anonymized_diary.csv participant_ID`

This command will generate `<participant_ID>_sleepDiary.csv` in your current working directory (the directory you run the python command from).
