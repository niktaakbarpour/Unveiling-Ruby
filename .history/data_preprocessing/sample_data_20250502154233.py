from utils.common import logger

def main():
    import pandas as pd

    input_file = 'results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet_corrected_topic_number.csv'
    output_file = 'results/data/sampled_output.csv'
    df = pd.read_csv(input_file)


    def sample_n_rows(group, n=15):
        if len(group) > n:
            return group.sample(n)
        return group


    df_sampled = df.groupby('topic', group_keys=False).apply(sample_n_rows)


    df_sampled.to_csv(output_file, index=False)

    logger.info(f"Sampled file saved to {output_file}")

if __name__ == '__main__':
    main()