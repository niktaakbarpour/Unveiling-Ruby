from utils.common import logger
import pandas as pd

def find_invalid_combinedtext_rows(csv_path):
    """
    Identifies rows in the dataset where the 'CombinedText' column is either NaN or not a string.
    Logs the indices of such rows.
    """
    df = pd.read_csv(csv_path)

    nan_indices = df[df['CombinedText'].isna()].index.tolist()
    non_string_indices = df[~df['CombinedText'].apply(lambda x: isinstance(x, str))].index.tolist()

    logger.info(f"Found {len(nan_indices)} rows with NaN in 'CombinedText': {nan_indices}")
    logger.info(f"Found {len(non_string_indices)} rows with non-string values in 'CombinedText': {non_string_indices}")

def main():
    csv_path = './results/data/deduplicated_data2.csv'
    find_invalid_combinedtext_rows(csv_path)

if __name__ == '__main__':
    main()
