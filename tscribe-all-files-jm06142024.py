import os
import json
import tscribe
##@jmasci 6.16.2024
## based on https://pypi.org/project/tscribe/

def process_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            outname = filename[:-5] + ".csv"
            tscribe.write(filename, format="csv", save_as=outname)

# Specify the directory containing the JSON files
json_directory = os.getcwd()

# Call the function to process the JSON files
process_json_files(json_directory)