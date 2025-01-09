import csv
import sys

# Ensure the script has the necessary command-line arguments
if len(sys.argv) < 2:
    print("Usage: python /path/to/sleepDiary_anonymization.py </path/to/input_non-anonymized_sleep_diary_csv> <participant_ID>")
    sys.exit(1)

input_file = sys.argv[1]
participant_id = sys.argv[2]
output_file = f"{participant_id}_sleepDiary.tsv"

# Column indices to extract from the input CSV and their corresponding headers
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

try:

    # Process the input CSV and write the output
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Replace "email" header with "true_participant_ID" in the output
        output_headers = list(columns_to_extract.values())
        output_headers[0] = "participant_ID"
        writer.writerow(output_headers)

        # Skip the first 3 rows
        for _ in range(3):
            next(reader)

        # Write filtered and deanonymized rows
        for row in reader:
            filtered_row = [participant_id] + [row[index - 1] for index in columns_to_extract.keys()]
            if participant_id != row[17]:
                print(f"WARNING: Participant has filled out incorrect participant ID. Participant-provided: {row[17]}. User-specified: {participant_id}. Manual inspection recommended.")
            #filtered_row = [participant_id, row[index-1] for index in columns_to_extract.keys()]
            writer.writerow(filtered_row)

    print(f"Deanonymized CSV saved as {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
