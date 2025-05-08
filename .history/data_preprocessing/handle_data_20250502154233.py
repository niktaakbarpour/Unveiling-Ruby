from utils.common import logger

def main():
    import pandas as pd

    path_dataset = './results/data/deduplicated_data2.csv'
    df = pd.read_csv(path_dataset)

    nan_indices = df[df['CombinedText'].isna()].index
    non_string_indices = df[~df['CombinedText'].apply(lambda x: isinstance(x, str))].index

    logger.info("Indices of rows with NaN values in 'CombinedText' column:", nan_indices)
    logger.info("Indices of rows with non-string values in 'CombinedText' column:", non_string_indices)

if __name__ == '__main__':
    main()