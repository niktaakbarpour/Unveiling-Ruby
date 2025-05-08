from utils.common import logger

def main():
    import os
    import pandas as pd

    def concatenate_csv_files(input_dir: str, output_filename: str) -> pd.DataFrame:
        """
        Concatenate all CSV files in a directory into one DataFrame.

        Args:
            input_dir (str): Path to the directory containing CSV files.
            output_filename (str): Filename for the concatenated output CSV.

        Returns:
            pd.DataFrame: The combined DataFrame from all CSVs.
        """
        csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
        combined_df = pd.concat(
            [pd.read_csv(os.path.join(input_dir, f)) for f in csv_files],
            ignore_index=True
        )
        output_path = os.path.join(input_dir, output_filename)
        combined_df.to_csv(output_path, index=False)
        logger.info(f"✅ Concatenated data saved to: {output_path}")
        return combined_df


    def remove_duplicates(df: pd.DataFrame, subset_col: str, output_path: str) -> pd.DataFrame:
        """
        Remove duplicate entries from the DataFrame based on a column.

        Args:
            df (pd.DataFrame): Input DataFrame.
            subset_col (str): Column name to check for duplicates.
            output_path (str): Path to save the deduplicated DataFrame.

        Returns:
            pd.DataFrame: Deduplicated DataFrame.
        """
        dedup_df = df.drop_duplicates(subset=subset_col, keep='first')
        dedup_df.to_csv(output_path, index=False)
        logger.info(f"✅ Deduplicated data saved to: {output_path}")
        return dedup_df


    if __name__ == "__main__":
        input_dir = "./results"
        concat_output = "concatenated_data.csv"
        dedup_output = "./results/deduplicated_data.csv"

        combined_df = concatenate_csv_files(input_dir, concat_output)
        remove_duplicates(combined_df, subset_col="Id", output_path=dedup_output)

if __name__ == '__main__':
    main()