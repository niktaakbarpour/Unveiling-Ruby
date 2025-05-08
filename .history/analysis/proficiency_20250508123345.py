import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from utils.common import logger


def filter_respondents_by_experience(df, experience_column_idx, filter_values):
    """
    Filter survey respondents based on experience values in a specified column.
    """
    return df[df.iloc[:, experience_column_idx].isin(filter_values)]


def extract_difficulty_ratings(df, description_row_idx, question_columns):
    """
    Extract and normalize difficulty ratings from the survey.
    """
    category_labels = df.iloc[description_row_idx, 26:61].tolist()
    df[question_columns] = df[question_columns].apply(pd.to_numeric, errors='coerce')

    records = []
    for idx, col in tqdm(enumerate(question_columns), total=len(question_columns)):
        valid_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
        counts = valid_data.value_counts().sort_index()
        records.append({
            'column': col,
            'description': category_labels[idx],
            'norm_count_1': counts.get(1, 0),
            'norm_count_2': counts.get(2, 0),
            'norm_count_3': counts.get(3, 0),
            'norm_count_4': counts.get(4, 0),
            'norm_count_5': counts.get(5, 0)
        })

    return pd.DataFrame(records)


def group_difficulty_by_description(df):
    """
    Group normalized difficulty counts by topic description.
    """
    return df.groupby('description').agg({
        'norm_count_1': 'sum',
        'norm_count_2': 'sum',
        'norm_count_3': 'sum',
        'norm_count_4': 'sum',
        'norm_count_5': 'sum'
    }).reset_index()


def main():
    # Load survey data
    df = pd.read_csv('survey/survey_data.csv')

    # Define your experience-based filter
    filter_values = ["Less than a year", "Between one and two years"]
    experience_column_idx = 25

    # Filter for specific experience group and save to CSV
    filtered_df = filter_respondents_by_experience(df, experience_column_idx, filter_values)
    logger.info(f"Filtered respondent count: {len(filtered_df)}")
    filtered_df.to_csv('survey/expert.csv', index=False)

    # Load separate file (e.g., novice responses)
    df_novice = pd.read_csv('survey/novice.csv')

    # Define columns and compute difficulty rating distributions
    question_columns = ['Q9_{}'.format(i) for i in range(1, 36)]
    difficulty_data = extract_difficulty_ratings(df_novice, -1, question_columns)

    logger.info(difficulty_data)

    grouped_data = group_difficulty_by_description(difficulty_data)
    logger.info(grouped_data)


if __name__ == '__main__':
    main()
