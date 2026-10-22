# importing the required modules
import glob
import os
import pandas as pd
import sys

# Ensure the script has the necessary command-line arguments
if len(sys.argv) < 3:
    print("Usage: python paper-SD_tsv_convertor.py </path/to/paper/sleep-diaries/folder> <Batch_folder_name>")
    sys.exit(1)

try:
    # specifying the path to csv files
    sd_folder_path = sys.argv[1] #sd = Sleep diaries
    batch_folder_name = sys.argv[2]

    input_path = sd_folder_path + '/' + batch_folder_name + '/validated_sleep_diaries'
    output_path = sd_folder_path + '/' + batch_folder_name + '/anonymized_sleep_diaries'

    # csv files in the path
    files = glob.glob(input_path + "/*.xlsx")

    # checking all the csv files in the 
    # specified path
    for filepath in files:
    
        # reading content of csv file
        df = pd.read_excel(filepath, index_col=None)

        file_name = os.path.basename(filepath) 
        print(file_name)

        full_path = os.path.join(output_path, file_name)
        output_file = full_path.replace(".xlsx", ".tsv")
        output_name = os.path.basename(output_file) 
        
        df.to_csv(output_file, sep='\t', index=False, encoding='utf-8')

        print(f"Original {file_name} file has been converted to {output_name}")

except Exception as e:
    print(f"An error occurred: {e}")
