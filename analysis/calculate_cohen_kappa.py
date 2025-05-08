import pandas as pd
from utils.common import logger


def load_and_process_csv(file_path):
    """
    Load the CSV file and convert 'Label1' and 'Label2' columns to boolean.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame with boolean labels.
    """
    df = pd.read_csv(file_path)
    df['Label1'] = df['Label1'].astype(bool)
    df['Label2'] = df['Label2'].astype(bool)
    return df


def count_label_condition(df):
    """
    Count rows where Label1 is False and Label2 is True.

    Args:
        df (pd.DataFrame): DataFrame with 'Label1' and 'Label2' columns.

    Returns:
        int: Number of matching rows.
    """
    return len(df[(df['Label1'] == False) & (df['Label2'] == True)])


def main():
    file_path = 'results/data/sampled_output2.csv'
    df = load_and_process_csv(file_path)
    count = count_label_condition(df)
    logger.info(f"Number of rows where Label1 is FALSE and Label2 is TRUE: {count}")


if __name__ == '__main__':
    main()
