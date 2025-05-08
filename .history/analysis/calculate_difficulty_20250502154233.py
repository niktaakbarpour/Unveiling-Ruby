from utils.common import logger
import pandas as pd

# Define your input file path
input_file = 'results/data/final_category.csv'  # TODO: Replace with actual input file path

def calculate_no_answer_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the percentage of questions with no answers per topic."""
    return df.groupby('category').apply(
        lambda x: (x['AnswerCount'] == 0).mean() * 100
    ).reset_index(name='no_answer_percentage')

def calculate_percentage_without_accepted_answers(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the percentage of questions without accepted answers."""
    return df.groupby('category').apply(
        lambda x: x['accepted_answer_id'].isna().mean() * 100
    ).reset_index(name='percentage_without_acc_answer')

def calculate_median_response_time(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate median response time from creation to accepted answer."""
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df['accepted_answer_creation_date'] = pd.to_datetime(df['accepted_answer_creation_date'], errors='coerce')
    df['response_time'] = (df['accepted_answer_creation_date'] - df['CreationDate']).dt.total_seconds() / 60
    return df.dropna(subset=['accepted_answer_creation_date']).groupby('category')['response_time'].mean().reset_index()

def main():
    # Load dataset
    df = pd.read_csv(input_file)

    # No answer percentage
    no_answer_df = calculate_no_answer_percentage(df)
    output_path_1 = 'results/data/no_answer_percentage_step3.csv'
    no_answer_df.to_csv(output_path_1, index=False)
    logger.info(f"No-answer percentage saved to {output_path_1}")

    # Percentage without accepted answers
    acc_ans_df = calculate_percentage_without_accepted_answers(df)
    output_path_2 = 'results/data/no_accepted_answers_step3_2.csv'
    acc_ans_df.to_csv(output_path_2, index=False)
    logger.info(f"Accepted-answer absence percentage saved to {output_path_2}")

    # Median response time
    median_time_df = calculate_median_response_time(df)
    output_path_3 = 'results/data/median_response_time_step3.csv'
    median_time_df.to_csv(output_path_3, index=False)
    logger.info(f"Median response time saved to {output_path_3}")

if __name__ == '__main__':
    main()
