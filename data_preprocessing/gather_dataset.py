import os
import pandas as pd
from utils.common import logger  # Make sure you have this setup in utils/common.py

def concatenate_csv_files(directory: str, output_file: str) -> pd.DataFrame:
    """
    Concatenates all CSV files in the given directory into a single DataFrame.

    Args:
        directory (str): Path to directory containing CSV files.
        output_file (str): Filename to save the concatenated output.

    Returns:
        pd.DataFrame: Concatenated DataFrame.
    """
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    concatenated_df = pd.concat(
        [pd.read_csv(os.path.join(directory, file)) for file in csv_files],
        ignore_index=True
    )
    output_path = os.path.join(directory, output_file)
    concatenated_df.to_csv(output_path, index=False)
    logger.info(f"✅ Concatenated CSVs saved to {output_path}")
    return concatenated_df

def deduplicate_dataframe(df: pd.DataFrame, output_file: str, subset_col='Id') -> pd.DataFrame:
    """
    Removes duplicates from the DataFrame and saves it.

    Args:
        df (pd.DataFrame): Input DataFrame.
        output_file (str): Path to save deduplicated CSV.
        subset_col (str): Column name to identify duplicates.

    Returns:
        pd.DataFrame: Deduplicated DataFrame.
    """
    dedup_df = df.drop_duplicates(subset=subset_col, keep='first')
    dedup_df.to_csv(output_file, index=False)
    logger.info(f"✅ Deduplicated data saved to {output_file}")
    return dedup_df

def main():
    directory = './results'
    concat_output = 'concatenated_data.csv'
    dedup_output = 'deduplicated_data.csv'

    concatenated_df = concatenate_csv_files(directory, concat_output)
    deduplicate_dataframe(concatenated_df, os.path.join(directory, dedup_output))

if __name__ == '__main__':
    main()
