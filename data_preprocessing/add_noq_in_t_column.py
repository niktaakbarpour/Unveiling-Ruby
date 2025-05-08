import pandas as pd
from utils.common import logger  # Ensure logger setup exists in utils/common.py

def add_noq_in_t_column(csv_filename: str, txt_filename: str, output_filename: str) -> None:
    """
    Adds a new column 'NoQ_in_T' (number of questions per tag) to a CSV file
    based on counts from a separate text file.

    Args:
        csv_filename (str): Path to the input CSV file.
        txt_filename (str): Path to the tag counts text file.
        output_filename (str): Path to write the updated CSV.
    """
    df = pd.read_csv(csv_filename)

    # Read tag counts from text file
    tag_counts = {}
    with open(txt_filename, 'r') as txt_file:
        for line in txt_file:
            try:
                tag, count = line.strip().split(': ')
                tag_counts[tag] = int(count)
            except ValueError:
                logger.warning(f"Skipping malformed line: {line.strip()}")

    # Add new column to DataFrame
    df['NoQ_in_T'] = df['Tag'].map(tag_counts)

    # Append to file without writing the header again
    df.to_csv(output_filename, mode='a', header=False, index=False)
    logger.info(f"✅ Appended 'NoQ_in_T' column and saved to {output_filename}")

def main():
    csv_filename = 'new_csvs/output_counts.csv'  # TODO: update with actual path
    txt_filename = 'tags/tag_counts.txt'         # TODO: update with actual path
    output_filename = 'new_csvs/output_counts.csv'  # TODO: update with actual output path

    add_noq_in_t_column(csv_filename, txt_filename, output_filename)

if __name__ == "__main__":
    main()
