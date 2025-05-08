from utils.common import logger
import pandas as pd
from datetime import datetime

def convert_date_format(date_str):
    """
    Converts a date string from 'dd/mm/yyyy HH:MM' to 'mm/dd/yyyy hh:mm:ss AM/PM'.
    If the input is NaN or malformed, returns it unchanged.
    """
    if pd.isna(date_str):
        return date_str
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M').strftime('%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        return date_str

def standardize_dates(input_file, output_file):
    """
    Loads a CSV, converts date formats in the 'accepted_answer_creation_date' column,
    and saves the result to a new CSV.
    """
    data = pd.read_csv(input_file)
    data['accepted_answer_creation_date'] = data['accepted_answer_creation_date'].apply(convert_date_format)
    data.to_csv(output_file, index=False)
    logger.info(f"The CSV file with standardized dates has been saved to {output_file}")

def main():
    input_path = 'results/data/final_dataset.csv'
    output_path = 'results/data/final_dataset_standardized_dates.csv'
    standardize_dates(input_path, output_path)

if __name__ == '__main__':
    main()
