from utils.common import logger
import pandas as pd

def create_configurations(input_csv_filename, output_csv_filename):
    """
    Reads a CSV file, filters tags based on multiple threshold combinations of
    Relevance and Significance, and writes the resulting tag sets to a new CSV.
    """
    # Load the input data
    df = pd.read_csv(input_csv_filename)

    # Define threshold values
    relevance_thresholds = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    significance_thresholds = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]

    configurations = []

    # Iterate over all combinations of thresholds
    for relevance_threshold in relevance_thresholds:
        for significance_threshold in significance_thresholds:
            # Filter rows based on both thresholds
            filtered_tags = df[
                (df['Relevance'] >= relevance_threshold) &
                (df['Significance'] >= significance_threshold)
            ]['Tag'].tolist()

            # Store the configuration result
            configurations.append({
                'Relevance': relevance_threshold,
                'Significance': significance_threshold,
                'Tags': ', '.join(filtered_tags)
            })

    # Convert to DataFrame and save to output
    result_df = pd.DataFrame(configurations)
    result_df.to_csv(output_csv_filename, index=False)

    logger.info(f"Configurations saved to {output_csv_filename}")

def main():
    input_csv_filename = 'new_csvs/output_counts.csv'
    output_csv_filename = 'new_csvs/filtered_tags2.csv'
    create_configurations(input_csv_filename, output_csv_filename)

if __name__ == '__main__':
    main()
