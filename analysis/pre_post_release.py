import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.common import logger


def load_and_prepare_data(file_path):
    """
    Load the dataset and parse dates.
    """
    df = pd.read_csv(file_path, low_memory=False)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
    df = df.dropna(subset=['CreationDate'])
    return df


def add_release_labels(df, release_date, start_range, end_range):
    """
    Label entries as 'Before', 'After', or 'Other' based on release date.
    """
    df['Release'] = df['CreationDate'].apply(
        lambda x: 'Before' if x <= release_date and x >= start_range else (
            'After' if x >= release_date and x < end_range else 'Other'
        )
    )
    return df[df['Release'].isin(['Before', 'After'])]


def plot_question_trends(df_filtered, release_date):
    """
    Plot the number of questions over time before and after release.
    """
    df_filtered['Week'] = df_filtered['CreationDate'].dt.to_period('D').apply(lambda r: r.start_time)

    grouped = df_filtered.groupby(['Week', 'Release']).size().reset_index(name='QuestionCount')

    plt.figure(figsize=(12, 8))
    sns.lineplot(
        data=grouped,
        x='Week',
        y='QuestionCount',
        hue='Release',
        palette=['#969696', '#a6cee3'],
        linewidth=1.5
    )
    plt.axvline(release_date, color='black', linestyle='--')
    plt.title('Number of Questions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Questions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    logger.info("Time trend plot created successfully.")


def main():
    input_file = 'results/data/final_category.csv'
    df = load_and_prepare_data(input_file)

    release_date = pd.to_datetime('2022-11-30')
    before_date = pd.to_datetime('2021-10-30')
    after_date = pd.to_datetime('2023-12-30')

    df_labeled = add_release_labels(df, release_date, before_date, after_date)
    plot_question_trends(df_labeled, release_date)

    # Optional: Monthly statistics (not plotted or used here)
    df['Year'] = df['CreationDate'].dt.year
    df['Month'] = df['CreationDate'].dt.month
    monthly_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')
    monthly_counts['Date'] = pd.to_datetime(monthly_counts[['Year', 'Month']].assign(DAY=1))
    logger.info("Monthly question stats prepared (not plotted).")


if __name__ == '__main__':
    main()
