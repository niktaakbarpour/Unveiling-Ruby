from utils.common import logger

def main():
    import pandas as pd

    file_path = 'results/data/sampled_output2.csv'

    df = pd.read_csv(file_path)

    df['Label1'] = df['Label1'].astype(bool)
    df['Label2'] = df['Label2'].astype(bool)

    count_true_rows = len(df[(df['Label1'] == False) & (df['Label2'] == True)])

    logger.info(f"Number of rows where both Label1 and Label2 are TRUE: {count_true_rows}")

if __name__ == '__main__':
    main()