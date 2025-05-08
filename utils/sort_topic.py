from utils.common import logger

def main():
    import pandas as pd

    # Load the CSV file into a DataFrame
    df = pd.read_csv('results/data/posts_using_arc.csv')

    # Sort the DataFrame based on the 'topic' column
    df_sorted = df.sort_values(by='topic')

    # Write the sorted DataFrame back to a new CSV filecd 
    df_sorted.to_csv('results/data/sorted_posts_using_arc.csv', index=False)

    logger.info("CSV file sorted by topic column and saved as 'sorted_file.csv'.")

if __name__ == '__main__':
    main()