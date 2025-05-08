import pandas as pd
from datetime import datetime

def convert_date_format(date_str):
    if pd.isna(date_str):
        return date_str
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M').strftime('%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        return date_str

input_file = 'results/data/final_dataset.csv'
data = pd.read_csv(input_file)
data['accepted_answer_creation_date'] = data['accepted_answer_creation_date'].apply(convert_date_format)
output_file = 'results/data/final_dataset_standardized_dates.csv'
data.to_csv(output_file, index=False)

print(f"The CSV file with standardized dates has been saved to {output_file}")
