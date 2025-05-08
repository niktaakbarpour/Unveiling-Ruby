from utils.common import logger
import pandas as pd

def count_topic_occurrences(input_file, output_file):
    """
    Reads a CSV, counts occurrences of each topic in the 'topic_name' column,
    and saves the result as a new CSV file with 'topic_name' and 'count' columns.
    """
    df = pd.read_csv(input_file)

    # Count topic occurrences
    topic_counts = df['topic_name'].value_counts()

    # Create a DataFrame from the counts
    result_df = pd.DataFrame({
        'topic_name': topic_counts.index,
        'count': topic_counts.values
    })

    # Save the result
    result_df.to_csv(output_file, index=False)
    logger.info(f"✅ Topic counts saved to '{output_file}'")

def main():
    input_file = 'results/data/final_dataset_standardized_dates.csv'
    output_file = 'results/data/topic_counts.csv'
    count_topic_occurrences(input_file, output_file)

if __name__ == '__main__':
    main()
