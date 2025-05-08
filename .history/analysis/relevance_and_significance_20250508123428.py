import pandas as pd
from utils.common import logger


def calculate_relevance(row):
    """
    Calculate relevance as NoQ_in_F / NoQ_in_T.
    """
    return row['NoQ_in_F'] / row['NoQ_in_T'] if row['NoQ_in_T'] != 0 else 0


def calculate_significance(row, total_questions=245467):
    """
    Calculate significance as NoQ_in_F / total number of questions.
    """
    return row['NoQ_in_F'] / total_questions


def add_columns_to_csv(input_csv, output_csv, total_questions=245467):
    """
    Load CSV, compute relevance and significance columns, and save the result.
    """
    df = pd.read_csv(input_csv)

    df['Relevance'] = df.apply(calculate_relevance, axis=1)
    df['Significance'] = df.apply(lambda row: calculate_significance(row, total_questions), axis=1)

    df.to_csv(output_csv, index=False)
    logger.info(f"Updated CSV with relevance and significance saved to: {output_csv}")


def main():
    input_csv = 'new_csvs/output_counts.csv'    # Replace with actual path
    output_csv = 'new_csvs/output_counts.csv'   # Overwrites the same file; adjust if needed

    add_columns_to_csv(input_csv, output_csv)


if __name__ == '__main__':
    main()
