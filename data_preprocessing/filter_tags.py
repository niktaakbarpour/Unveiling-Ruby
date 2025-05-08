from utils.common import logger

def main():
    import pandas as pd

    def create_configurations(input_csv_filename, output_csv_filename):
        # Read the original CSV file into a pandas DataFrame
        df = pd.read_csv(input_csv_filename)

    # Define the thresholds for Relevance and Significance
        relevance_thresholds = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
        significance_thresholds = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]

        configurations = []

    # Generate configurations for each combination of thresholds
        for relevance_threshold in relevance_thresholds:
            for significance_threshold in significance_thresholds:
                # Filter tags based on conditions
                filtered_tags = df[
                    (df['Relevance'] >= relevance_threshold) & 
                    (df['Significance'] >= significance_threshold)
                ]['Tag'].tolist()

                # Append configuration to the list
                configurations.append({
                    'Relevance': relevance_threshold,
                    'Significance': significance_threshold,
                    'Tags': ', '.join(filtered_tags)
                })

        # Create a new DataFrame from the list of configurations
        result_df = pd.DataFrame(configurations)

        # Write the new DataFrame to the output CSV file
        result_df.to_csv(output_csv_filename, index=False)

    if __name__ == "__main__":
        input_csv_filename = 'new_csvs/output_counts.csv'      # Replace with your actual CSV file path
        output_csv_filename = 'new_csvs/filtered_tags2.csv'  # Replace with your desired output CSV file path

        create_configurations(input_csv_filename, output_csv_filename)

if __name__ == '__main__':
    main()