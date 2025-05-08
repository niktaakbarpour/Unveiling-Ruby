from utils.common import logger

def main():
    import pandas as pd

    def add_noq_in_t_column(csv_filename, txt_filename, output_filename):
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(csv_filename)

        # Read the text file and extract tag names and counts
        with open(txt_filename, 'r') as txt_file:
            tag_counts = {}
            for line in txt_file:
                tag, count = line.strip().split(': ')
                tag_counts[tag] = int(count)

        # Add a new column 'NoQ_in_T' to the DataFrame
        df['NoQ_in_T'] = df['Tag'].map(tag_counts)

        # Write the updated DataFrame to the existing CSV file without overwriting
        df.to_csv(output_filename, mode='a', header=False, index=False)

    if __name__ == "__main__":
        csv_filename = 'new_csvs/output_counts.csv'  # Replace with your actual CSV file path
        txt_filename = 'tags/tag_counts.txt'  # Replace with your actual text file path
        output_filename = 'new_csvs/output_counts.csv'  # Replace with your desired output CSV file path

        add_noq_in_t_column(csv_filename, txt_filename, output_filename)

if __name__ == '__main__':
    main()