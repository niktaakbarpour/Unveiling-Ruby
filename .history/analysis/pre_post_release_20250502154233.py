from utils.common import logger

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import Normalize
    from matplotlib.cm import get_cmap
    from matplotlib.colors import LinearSegmentedColormap
    import seaborn as sns

    df = pd.read_csv('results/data/final_category.csv', low_memory=False)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)

    df = df.dropna(subset=['CreationDate'])

    before = pd.to_datetime('2021-10-30')
    after = pd.to_datetime('2023-12-30')
    release_date = pd.to_datetime('2022-11-30')

    Add a 'Release' column: 'Before' for before release date, 'After' for after
    Apply the lambda function to categorize 'Before' and 'After'
    df['Release'] = df['CreationDate'].apply(lambda x: 'Before' if x <= release_date and x >= before else ('After' if x >= release_date and x < after else 'Other'))
    df['Release'] = df['CreationDate'].apply(lambda x: 'Before' if x <= release_date else ('After' if x >= release_date else 'Other'))


    Filter to include only 'Before' and 'After' categories
    df_filtered = df[df['Release'].isin(['Before', 'After'])]

    # Group by week of the year and count the number of questions per week
    df_filtered['Week'] = df_filtered['CreationDate'].dt.to_period('D').apply(lambda r: r.start_time)

    # Group data by week and release category
    grouped = df_filtered.groupby(['Week', 'Release']).size().reset_index(name='QuestionCount')

    # Plot
    plt.figure(figsize=(12, 8))

    # Create the line plot using seaborn
    sns.lineplot(
        data=grouped,
        x='Week',
        y='QuestionCount',
        hue='Release',
        palette=['#969696', '#a6cee3'],  # Custom colors (grey and light blue)
        linewidth=1.5
    )

    # Add a vertical line to indicate the release date
    plt.axvline(pd.to_datetime('2022-11-30'), color='black', linestyle='--')

    # Customize labels and title
    plt.title('Number of Questions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Questions')
    plt.xticks(rotation=45)

    # Show plot
    plt.tight_layout()
    plt.show()


    total_questions_per_month = df.groupby(['Year', 'Month']).size()

    # total_questions_per_month = total_questions_per_month.reset_index(name='Count')

    total_questions_per_month['Date'] = pd.to_datetime(total_questions_per_month[['Year', 'Month']].assign(DAY=1))

    # total_questions_per_month = total_questions_per_month.sort_values('Date')

if __name__ == '__main__':
    main()