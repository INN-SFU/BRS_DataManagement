import csv
import sys

# Ensure the script has the necessary command-line arguments
if len(sys.argv) < 3:
    print("Usage: python sleepDiary_anonymization.py <input_csv> <email_id_csv> <output_csv>")
    sys.exit(1)

input_file = sys.argv[1]
email_id_file = sys.argv[2]
output_file = sys.argv[3]

# Column indices to extract from the input CSV and their corresponding headers
columns_to_extract = {
    12: "email",  # This will be replaced by true_participant_ID in the output
    18: "participant_ID",
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
    # Load the email to participant_id mapping from the second CSV
    email_to_participant_id = {}
    with open(email_id_file, mode="r", newline="", encoding="utf-8") as email_file:
        reader = csv.reader(email_file)
        next(reader)  # Skip the header
        for row in reader:
            email = row[1].strip()
            participant_id = row[2].strip()
            email_to_participant_id[email] = participant_id

    # Process the input CSV and write the output
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Replace "email" header with "true_participant_ID" in the output
        output_headers = list(columns_to_extract.values())
        output_headers[0] = "true_participant_ID"
        writer.writerow(output_headers)

        # Skip the first 3 rows
        for _ in range(3):
            next(reader)

        # Write filtered and deanonymized rows
        for row in reader:
            email = row[11].strip()
            true_participant_id = email_to_participant_id.get(email, "UNKNOWN")
            filtered_row = [true_participant_id if index == 12 else row[index-1] for index in columns_to_extract.keys()]
            writer.writerow(filtered_row)

    print(f"Deanonymized CSV saved as {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
