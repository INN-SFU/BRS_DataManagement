import csv
import sys
from io import StringIO
import re 

# Ensure the script has the necessary command-line arguments
if len(sys.argv) < 3:
    print("Usage: python /path/to/sleepDiary_anonymization.py </path/to/input_non-anonymized_sleep_diary_tsv> <participant_ID>")
    sys.exit(1)

input_file = sys.argv[1]
participant_id = sys.argv[2]
output_file = f"{participant_id}_sleepDiary.tsv"

# Column indices to extract from the input TSV and their corresponding headers
columns_to_extract = {
    1: "start_time",
    2: "end_time",
    5: "progress",
    6: "duration",
    7: "finished",
    8: "record_time",
    #12: "email",  # This will be replaced by true_participant_ID in the output
    18: "participant-recorded_participant_ID",
    19: "lights_off",
    20: "lights_on",
    21: "time_tried_to_fall_asleep",
    22: "time_to_fall_asleep",
    23: "wakeup",
    24: "alarm",
    25: "bed_until_getting_up",
    26: "wake_at_night",
    27: "wake_at_night_when_1",
    28: "wake_at_night_how_long_1",
    29: "wake_at_night_when_2",
    30: "wake_at_night_how_long_2",
    31: "wake_at_night_when_3",
    32: "wake_at_night_how_long_3",
    33: "wake_at_night_when_4",
    34: "wake_at_night_how_long_4",
    35: "sleep_disturbance",
    36: "sleep_disturbance_text",
    37: "how_sleep",
    38: "how_feel",
    39: "nap",
    40: "nap_start_1",
    41: "nap_end_1",
    42: "nap_start_2",
    43: "nap_end_2",
    44: "medication",
    45: "medication_list",
    46: "took_off_watch",
    47: "took_off_watch_reason",
    48: "actiwatch_removed",
    49: "actiwatch_put_back_on",
    50: "comments",
}


def format_time(time_str):
    # Convert to uppercase
    time_str = time_str.upper()
    
    # Add space between time and AM/PM if necessary
    time_str = re.sub(r'(\d{2}:\d{2})(AM|PM)', r'\1 \2', time_str)
    
    # Remove leading zero from HH if present
    time_str = re.sub(r'^0(\d:\d{2} [AP]M)', r'\1', time_str)
    
    return time_str


try:

    # Process the input TSV and write the output
    with open(input_file, mode="r", newline="", encoding="utf-16") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
             
        lines = [line.replace('\r\n', '\n').replace('\r', '\n') for line in infile]
        modified_file = StringIO("".join(lines))
             
        reader = csv.reader(modified_file, delimiter="\t")
        writer = csv.writer(outfile, delimiter="\t")

        # Replace "email" header with "true_participant_ID" in the output
        output_headers = list(columns_to_extract.values())
        output_headers = ["participant_ID"] + output_headers + ["qualtrics_or_transcribed"]
        writer.writerow(output_headers)

        # Skip the first 3 rows
        for _ in range(3):
            next(reader)

        # Write filtered and deanonymized rows
        for row in reader:
            filtered_row = [participant_id] + [row[index - 1] for index in columns_to_extract.keys()] + ["qualtrics"]
            if participant_id[4:] != row[17]:
                print(f"WARNING: Participant has filled out incorrect participant ID. Participant-provided: {row[17]}. User-specified: {participant_id[4:]}. Manual inspection recommended.")
            #filtered_row = [participant_id, row[index-1] for index in columns_to_extract.keys()]

             # Transform the "medication" column
            medication_index = list(columns_to_extract.keys()).index(44) + 1  # +1 because of the added participant_ID column
            if filtered_row[medication_index].startswith("Yes"):
                filtered_row[medication_index] = "Yes"
            elif filtered_row[medication_index].startswith("Decline"):
                filtered_row[medication_index] = "Decline"
            
            # Transform time-related columns
            time_columns = [19, 20, 21, 23, 27, 29, 31, 33, 40, 41, 42, 43, 48, 49]
            for col in time_columns:
                col_index = list(columns_to_extract.keys()).index(col) + 1  # +1 because of the added participant_ID column
                if filtered_row[col_index]:
                    filtered_row[col_index] = format_time(filtered_row[col_index])

            writer.writerow(filtered_row)

    print(f"Deanonymized TSV saved as {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
