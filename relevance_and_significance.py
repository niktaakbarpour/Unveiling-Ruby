import pandas as pd

def calculate_relevance(row):
    # Calculate Relevance by dividing NoQ_in_F by NoQ_in_T
    return row['NoQ_in_F'] / row['NoQ_in_T'] if row['NoQ_in_T'] != 0 else 0

def calculate_significance(row):
    # Calculate Significance by dividing NoQ_in_F by a specified value (e.g., 245467)
    return row['NoQ_in_F'] / 245467

def add_columns_to_csv(input_csv_filename, output_csv_filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv_filename)

    # Add 'Relevance' column
    df['Relevance'] = df.apply(calculate_relevance, axis=1)

    # Add 'Significance' column
    df['Significance'] = df.apply(calculate_significance, axis=1)

    # Write the updated DataFrame to the output CSV file
    df.to_csv(output_csv_filename, index=False)

if __name__ == "__main__":
    input_csv_filename = 'new_csvs/output_counts.csv'   # Replace with your actual CSV file path
    output_csv_filename = 'new_csvs/output_counts.csv'  # Replace with your desired output CSV file path

    add_columns_to_csv(input_csv_filename, output_csv_filename)
