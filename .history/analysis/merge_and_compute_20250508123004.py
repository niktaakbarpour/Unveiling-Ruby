# merge_and_compute.py

import pandas as pd
from ruby_survey_analysis import compute_averages
from utils.common import logger


TIME_VALUE_MAP = {1: 7.5, 2: 22.5, 3: 45, 4: 90, 5: 120}
DIFFICULTY_VALUE_MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}


def merge_with_stackoverflow(survey_time_df, survey_difficulty_df, so_no_answer_path, so_response_time_path):
    # Load StackOverflow metrics
    so_df1 = pd.read_csv(so_no_answer_path)
    so_df2 = pd.read_csv(so_response_time_path)

    # Merge survey time and difficulty
    combined = pd.merge(survey_time_df, survey_difficulty_df, on='description', suffixes=('_time', '_difficulty'))
    combined = pd.merge(combined, so_df1, left_on='description', right_on='category')
    combined = pd.merge(combined, so_df2, on='category')
    logger.info("Merged combined survey and SO data.")
    return combined


def compute_average_metrics(combined_df):
    combined_df['avg_time'] = combined_df.apply(
        lambda row: compute_averages(row.filter(like='norm_count_').filter(like='_time'), TIME_VALUE_MAP), axis=1
    )

    combined_df['avg_difficulty'] = combined_df.apply(
        lambda row: (compute_averages(row.filter(like='norm_count_').filter(like='_difficulty'), DIFFICULTY_VALUE_MAP) - 1) * 25, axis=1
    )

    logger.info("Computed average time and difficulty for each category.")
    return combined_df[['description', 'avg_time', 'avg_difficulty', 'response_time', 'without_accepted_answer', 'category']]
