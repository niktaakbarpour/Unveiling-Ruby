# ruby_survey_analysis.py

import pandas as pd
import numpy as np
from tqdm import tqdm
from utils.common import logger

# Constants
TIME_COLUMNS = ['Q12_{}'.format(i) for i in range(1, 36)]
DIFFICULTY_COLUMNS = ['Q9_{}'.format(i) for i in range(1, 36)]
SENTENCE_TO_NUMBER = {
    'less than 15 minutes': 1,
    'between 15 to 30 minutes': 2,
    'between 30 to 60 minutes': 3,
    'between 1 and 2 hours': 4,
    'more than 2 hours': 5
}


def load_survey_data(path):
    df = pd.read_csv(path)
    logger.info("Survey data loaded successfully.")
    return df


def clean_descriptions(raw_descriptions):
    cleaned = []
    for desc in raw_descriptions:
        if isinstance(desc, str) and '-' in desc:
            cleaned.append(desc.split('-')[-1].strip())
        else:
            cleaned.append('')
    return cleaned


def extract_response_distribution(df, columns, is_time_column=False):
    """
    Returns a list of dictionaries with rating counts for each question.
    """
    results = []
    for idx, col in tqdm(enumerate(columns), total=len(columns)):
        series = df[col].map(SENTENCE_TO_NUMBER) if is_time_column else pd.to_numeric(df[col], errors='coerce')
        filtered = series[(series >= 1) & (series <= 5)]
        counts = filtered.value_counts().sort_index()

        results.append({
            'column': col,
            'norm_count_1': counts.get(1, 0),
            'norm_count_2': counts.get(2, 0),
            'norm_count_3': counts.get(3, 0),
            'norm_count_4': counts.get(4, 0),
            'norm_count_5': counts.get(5, 0),
        })
    return pd.DataFrame(results)


def compute_averages(df_counts, value_map):
    total = sum(df_counts[f'norm_count_{i}'] for i in range(1, 6))
    if total == 0:
        return 0
    weighted_sum = sum(df_counts[f'norm_count_{i}'] * value_map[i] for i in range(1, 6))
    return weighted_sum / total


def group_by_description(df, descriptions):
    df['description'] = descriptions
    grouped = df.groupby('description').agg({
        'norm_count_1': 'sum',
        'norm_count_2': 'sum',
        'norm_count_3': 'sum',
        'norm_count_4': 'sum',
        'norm_count_5': 'sum',
    }).reset_index()
    return grouped


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


# visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from utils.common import logger


def plot_difficulty_vs_time(df, save_path='difficulty_bubble_chart.pdf'):
    """
    Generate a scatter plot showing difficulty vs. resolution time.
    Bubble color reflects StackOverflow response time.
    """
    norm = mpl.colors.Normalize(vmin=df['response_time'].min(), vmax=df['response_time'].max())
    cmap = plt.get_cmap('Spectral')

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        df['avg_time'],
        df['avg_difficulty'],
        s=200,
        c=df['response_time'],
        cmap=cmap,
        norm=norm,
        alpha=0.8,
        edgecolor='k'
    )

    cbar = plt.colorbar(scatter)
    cbar.set_label('Avg. SO Response Time (minutes)')

    for _, row in df.iterrows():
        plt.annotate(
            row['description'],
            (row['avg_time'], row['avg_difficulty']),
            fontsize=8,
            ha='center',
            va='bottom',
            alpha=0.7
        )

    plt.xlabel('Avg. Time to Resolve (Survey, mins)')
    plt.ylabel('Avg. Difficulty (Survey, scaled 0–100)')
    plt.title('Perceived Difficulty vs Resolution Time (Ruby Topics)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    logger.info(f"Plot saved to {save_path}")



# main.py

from ruby_survey_analysis import (
    load_survey_data,
    clean_descriptions,
    extract_response_distribution,
    group_by_description
)
from merge_and_compute import merge_with_stackoverflow, compute_average_metrics
from visualization import plot_difficulty_vs_time

SURVEY_PATH = 'survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv'
SO_NO_ANSWER_PATH = 'results/data/no_accepted_answers_step3.csv'
SO_RESPONSE_TIME_PATH = 'results/data/median_response_time_step3.csv'


def main():
    # Load and prepare survey data
    df = load_survey_data(SURVEY_PATH)
    desc_time = clean_descriptions(df.iloc[0, 72:107].tolist())
    desc_diff = clean_descriptions(df.iloc[0, 26:61].tolist())

    time_dist = extract_response_distribution(df, ['Q12_{}'.format(i) for i in range(1, 36)], is_time_column=True)
    diff_dist = extract_response_distribution(df, ['Q9_{}'.format(i) for i in range(1, 36)], is_time_column=False)

    time_grouped = group_by_description(time_dist, desc_time)
    diff_grouped = group_by_description(diff_dist, desc_diff)

    # Merge with StackOverflow data and compute averages
    combined_df = merge_with_stackoverflow(time_grouped, diff_grouped, SO_NO_ANSWER_PATH, SO_RESPONSE_TIME_PATH)
    final_df = compute_average_metrics(combined_df)

    # Visualize
    plot_difficulty_vs_time(final_df)


if __name__ == '__main__':
    main()
