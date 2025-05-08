from utils.common import logger

def main():
    import pandas as pd

    input_file = 'results/data/posts_using_arc.csv'
    output_file = 'results/data/sorted_posts_using_arc.csv'

    # Load the CSV file
    df = pd.read_csv(input_file)

    # Sort the DataFrame by the 'topic' column
    df_sorted = df.sort_values(by='topic')

    # Save the sorted DataFrame to a new file
    df_sorted.to_csv(output_file, index=False)

    logger.info(f"CSV file sorted by 'topic' and saved as '{output_file}'.")

if __name__ == '__main__':
    main()
