import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python /path/to/script.py </path/to/input_csv>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)  # Read all rows into a list

    if rows:
        rows[0].append("qualtrics_or_transcribed")  # Add the new column header
        for row in rows[1:]:
            row.append("transcribed")  # Add the value "transcribed" to each data row

    with open(input_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)  # Write all rows back to the file

    print(f"Column 'qualtrics_or_transcribed' added with value 'transcribed' for all rows in {input_file}.")

except FileNotFoundError:
    print(f"Error: File '{input_file}' not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
