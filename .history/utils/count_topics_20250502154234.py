from utils.common import logger

def main():
    import pandas as pd

    input_file = 'results/data/final_dataset_standardized_dates.csv' 
    df = pd.read_csv(input_file)

    topic_counts = df['topic_name'].value_counts()

    new_df = pd.DataFrame({
        'topic_name': topic_counts.index,
        'count': topic_counts.values
    })

    output_file = 'results/data/topic_counts.csv'
    new_df.to_csv(output_file, index=False)

    logger.info(f"New CSV file saved as {output_file}")

if __name__ == '__main__':
    main()