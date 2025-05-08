from utils.common import logger

import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.ticker import MaxNLocator


def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
    return df.dropna(subset=['CreationDate'])


def create_output_directory(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def get_yearly_counts(df, topic_col, topic):
    filtered_df = df[df[topic_col] == topic]
    total_per_year = df.groupby('Year').size()
    topic_per_year = filtered_df.groupby('Year').size()
    percentage = (topic_per_year / total_per_year).fillna(0) * 100
    return topic_per_year, percentage


def plot_topic_trend(topic, years, counts, percentages, output_dir):
    fig, ax1 = plt.subplots(figsize=(8, 4.5))

    ax1.plot(years, counts, color='#003f5c', label='#')
    ax1.tick_params(axis='y', labelsize=15)
    ax2 = ax1.twinx()
    ax2.plot(years, percentages, color='#ffa600', label='%')
    ax2.tick_params(axis='y', labelsize=15)
    ax1.set_xticks([2008, 2012, 2016, 2020, 2024])
    ax1.tick_params(axis='x', labelsize=15)

    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_visible(False)

    mid_y1 = (ax1.get_ylim()[0] + ax1.get_ylim()[1]) / 2
    mid_y2 = (ax2.get_ylim()[0] + ax2.get_ylim()[1]) / 2

    ax1.text(ax1.get_xlim()[0] - 2.5, mid_y1, '%', color='#ffa600', fontsize=15,
             va='center', ha='center', rotation='vertical')
    ax2.text(ax2.get_xlim()[1] + 2, mid_y2, '#', color='#003f5c', fontsize=15,
             va='center', ha='center', rotation='vertical')

    ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))

    filename = f"{output_dir}/{topic.replace('/', '_')}_line_chart.pdf"
    plt.savefig(filename)
    plt.close(fig)


def process_and_plot(df, topic_col, output_dir):
    create_output_directory(output_dir)
    df['Year'] = df['CreationDate'].dt.year
    unique_topics = df[topic_col].unique()

    for topic in tqdm(unique_topics):
        topic_counts, percentages = get_yearly_counts(df, topic_col, topic)
        if topic_counts.empty:
            logger.info(f"No data for topic: {topic}")
            continue
        plot_topic_trend(topic, topic_counts.index, topic_counts.values, percentages.values, output_dir)


def main():
    df = load_data('results/data/final_category.csv')
    process_and_plot(df, 'category', 'results/line_charts_step3')


if __name__ == '__main__':
    main()