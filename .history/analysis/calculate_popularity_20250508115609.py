import pandas as pd
from utils.common import logger

INPUT_FILE = 'results/data/final_category.csv'
OUTPUT_FILE = 'results/data/average_score_step3.csv'


def load_and_clean_data(file_path):
    """
    Load the CSV file and filter rows with numeric 'Score'.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Filtered DataFrame with valid numeric 'Score'.
    """
    data = pd.read_csv(file_path)
    numeric_mask = pd.to_numeric(data['Score'], errors='coerce').notna()
    filtered_data = data[numeric_mask].copy()
    filtered_data['Score'] = pd.to_numeric(filtered_data['Score'])
    return filtered_data


def compute_average_score(df):
    """
    Compute average score grouped by category.

    Args:
        df (pd.DataFrame): DataFrame with numeric 'Score' and 'category'.

    Returns:
        pd.DataFrame: DataFrame with average score per category.
    """
    return df.groupby('category')['Score'].mean().reset_index()


def save_average_score(df, output_path):
    """
    Save the average score DataFrame to a CSV file and log the result.

    Args:
        df (pd.DataFrame): DataFrame to save.
        output_path (str): Path to save the CSV file.
    """
    df.to_csv(output_path, index=False)
    logger.info(f"The average score per topic has been saved to {output_path}")


def main():
    df = load_and_clean_data(INPUT_FILE)
    average_scores = compute_average_score(df)
    save_average_score(average_scores, OUTPUT_FILE)
    logger.info(f"Average scores:\n{average_scores}")


if __name__ == '__main__':
    main()
