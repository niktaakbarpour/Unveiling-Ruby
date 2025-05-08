from utils.common import logger
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_and_prepare_data(filepath):
    """Load CSV and prepare it for plotting."""
    df = pd.read_csv(filepath)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'])  # Ensure datetime format
    df['Year'] = df['CreationDate'].dt.year  # Extract year
    return df

def create_output_dir(directory):
    """Create output directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)
    return directory

def plot_topic_counts_by_year(df, output_dir):
    """Generate and save line plots for question counts per year by topic."""
    for topic in df['topic'].unique():
        topic_data = df[df['topic'] == topic]
        counts_per_year = topic_data['Year'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.plot(counts_per_year.index, counts_per_year.values, marker='o', linestyle='-')
        plt.title(f'Number of Questions Over Years for Topic: {topic}')
        plt.xlabel('Year')
        plt.ylabel('Number of Questions')
        plt.grid(True)
        plt.tight_layout()

        output_file = os.path.join(output_dir, f'topic_{topic}_by_year.png')
        plt.savefig(output_file)
        plt.close()

    logger.info(f'Plots saved in directory: {output_dir}')

def main():
    input_csv = 'results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet_corrected_topic_number.csv'
    output_dir = 'results/data/images'

    df = load_and_prepare_data(input_csv)
    output_dir = create_output_dir(output_dir)
    plot_topic_counts_by_year(df, output_dir)

if __name__ == '__main__':
    main()
