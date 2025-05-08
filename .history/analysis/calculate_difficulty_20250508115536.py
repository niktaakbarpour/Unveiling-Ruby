import pandas as pd
from utils.common import logger

# Define input file path
INPUT_FILE = 'results/data/final_category.csv'  # TODO: Replace with actual input path


def calculate_no_answer_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the percentage of questions with no answers for each topic category.

    Args:
        df (pd.DataFrame): Input DataFrame with 'AnswerCount' and 'category'.

    Returns:
        pd.DataFrame: Category-wise percentage of questions with no answers.
    """
    return df.groupby('category').apply(
        lambda x: (x['AnswerCount'] == 0).mean() * 100
    ).reset_index(name='no_answer_percentage')


def calculate_percentage_without_accepted_answers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the percentage of questions without accepted answers per category.

    Args:
        df (pd.DataFrame): Input DataFrame with 'accepted_answer_id' and 'category'.

    Returns:
        pd.DataFrame: Category-wise percentage of questions without accepted answers.
    """
    return df.groupby('category').apply(
        lambda x: x['accepted_answer_id'].isna().mean() * 100
    ).reset_index(name='percentage_without_acc_answer')


def calculate_median_response_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average response time (in minutes) to accepted answers per category.

    Args:
        df (pd.DataFrame): Input DataFrame with 'CreationDate' and 'accepted_answer_creation_date'.

    Returns:
        pd.DataFrame: Category-wise average response time.
    """
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df['accepted_answer_creation_date'] = pd.to_datetime(df['accepted_answer_creation_date'], errors='coerce')
    df['response_time'] = (df['accepted_answer_creation_date'] - df['CreationDate']).dt.total_seconds() / 60

    return (
        df.dropna(subset=['accepted_answer_creation_date'])
        .groupby('category')['response_time']
        .mean()
        .reset_index()
    )


def save_dataframe_to_csv(df: pd.DataFrame, path: str, message: str):
    """
    Save a DataFrame to a CSV file and log a message.

    Args:
        df (pd.DataFrame): Data to save.
        path (str): Output file path.
        message (str): Message to log after saving.
    """
    df.to_csv(path, index=False)
    logger.info(f"{message} saved to {path}")


def main():
    # Load dataset
    df = pd.read_csv(INPUT_FILE)

    # Compute and save: no-answer percentage
    no_answer_df = calculate_no_answer_percentage(df)
    save_dataframe_to_csv(no_answer_df, 'results/data/no_answer_percentage_step3.csv', "No-answer percentage")

    # Compute and save: percentage without accepted answers
    acc_ans_df = calculate_percentage_without_accepted_answers(df)
    save_dataframe_to_csv(acc_ans_df, 'results/data/no_accepted_answers_step3_2.csv', "Accepted-answer absence percentage")

    # Compute and save: median response time
    median_time_df = calculate_median_response_time(df)
    save_dataframe_to_csv(median_time_df, 'results/data/median_response_time_step3.csv', "Median response time")


if __name__ == '__main__':
    main()
