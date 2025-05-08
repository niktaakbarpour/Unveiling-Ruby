from utils.common import logger
import pandas as pd

def sample_rows_by_topic(df, group_col='topic', n=15):
    """
    Samples up to `n` rows from each group defined by `group_col`.
    If a group has fewer than `n` rows, all rows are retained.
    """
    return df.groupby(group_col, group_keys=False).apply(lambda group: group.sample(n=min(n, len(group))))

def main():
    input_file = 'results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet_corrected_topic_number.csv'
    output_file = 'results/data/sampled_output.csv'

    df = pd.read_csv(input_file)
    logger.info(f"Loaded {len(df)} rows from {input_file}")

    df_sampled = sample_rows_by_topic(df, group_col='topic', n=15)
    df_sampled.to_csv(output_file, index=False)

    logger.info(f"Sampled {len(df_sampled)} rows across {df['topic'].nunique()} topics")
    logger.info(f"Sampled file saved to {output_file}")

if __name__ == '__main__':
    main()
