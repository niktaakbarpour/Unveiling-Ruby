import pandas as pd
import os

def concatenate_csv_files(input_folder, output_file):
    # Get a list of all CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the concatenated data
    concatenated_data = pd.DataFrame()

    # Loop through each CSV file and concatenate it to the DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(file_path)
        concatenated_data = pd.concat([concatenated_data, df], ignore_index=True)

    # Write the concatenated data to a new CSV file
    concatenated_data.to_csv(output_file, index=False)

# Example usage
input_folder = '..\Downloads\prev_csvs'
output_file = '..\Downloads\concatenated_data.csv'
concatenate_csv_files(input_folder, output_file)