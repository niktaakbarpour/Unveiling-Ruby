import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import pearsonr
from utils.common import logger

# Placeholder input file
INPUT_FILE = 'path/to/final_category.csv'  # TODO: Replace with actual path
OUTPUT_FIGURE = 'receive_accepted_answer_distribution.pdf'


def load_and_merge_datasets():
    """Load and merge datasets for correlation analysis."""
    df1 = pd.read_csv('results/data/no_answer_percentage_step1.csv', usecols=[0, 1])
    df2 = pd.read_csv('results/data/no_accepted_answers_step1.csv', usecols=[0, 1])
    df3 = pd.read_csv('results/data/median_response_time_step1.csv', usecols=[0, 1])

    merged_1_2 = pd.merge(df1, df2, on='topic_name', suffixes=('_1', '_2'))
    merged_1_3 = pd.merge(df1, df3, on='topic_name', suffixes=('_1', '_3'))
    merged_2_3 = pd.merge(df2, df3, on='topic_name', suffixes=('_2', '_3'))

    return merged_1_2, merged_1_3, merged_2_3


def calculate_correlation(df, col_a, col_b):
    """Calculate Pearson correlation between two columns."""
    data = df[[col_a, col_b]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(data) > 1:
        return pearsonr(data[col_a], data[col_b])[0]
    logger.info(f"Not enough valid data for correlation between {col_a} and {col_b}.")
    return None


def classify_response_time(data):
    """Calculate response time and classify it into 5 categories."""
    data['CreationDate'] = pd.to_datetime(data['CreationDate'], errors='coerce')
    data['accepted_answer_creation_date'] = pd.to_datetime(data['accepted_answer_creation_date'], errors='coerce')
    data['response_time'] = (data['accepted_answer_creation_date'] - data['CreationDate']).dt.total_seconds() / 60

    bins = [-1, 15, 30, 60, 120, float('inf')]
    labels = [1, 2, 3, 4, 5]
    data['response_time_category'] = pd.cut(data['response_time'], bins=bins, labels=labels)
    return data.dropna(subset=['category', 'response_time_category'])


def count_response_time_categories(data):
    """Count response time categories within each topic category."""
    counts = defaultdict(lambda: {str(i): 0 for i in range(1, 6)})

    for _, row in data.iterrows():
        category = row['category']
        cat = str(int(row['response_time_category']))
        counts[category][cat] += 1
    return counts


def normalize_counts(category_counts, max_length=100):
    """Normalize counts for bar chart length."""
    normalized = []
    for category, counts in category_counts.items():
        total = sum(counts.values())
        norm = {k: (v / total) * max_length for k, v in counts.items()}
        normalized.append({'category': category, **norm})
    return sorted(normalized, key=lambda x: x['4'] + x['5'])


def simplify_category_name(name):
    """Map full category names to display names."""
    mapping = {
        "Development Environment and Infrastructure": "Dev. Env.",
        "Software Architecture and Performance": "Arch.",
        "Web Application Development": "App. Dev.",
        "Application Quality and Security": "App. Quality",
        "Core Ruby Concepts": "Core",
        "Data Management and Processing": "Data"
    }
    return mapping.get(name, name)


def plot_stacked_bar_chart(data_to_plot, max_length=100, output_file=OUTPUT_FIGURE):
    """Generate and save a normalized stacked bar chart of response times."""
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]
    label_fontsize = 16

    plt.figure(figsize=(12, 3))
    for idx, item in enumerate(data_to_plot):
        y = item['category']
        display_name = simplify_category_name(y)
        values = [item[str(i)] for i in range(1, 6)]
        left = 0

        for i, v in enumerate(values):
            plt.barh(y, v, left=left, color=colors[i], label=f'Category {i+1}' if idx == 0 else "")
            if v > 0:
                plt.text(left + v / 2, idx - 0.25, f'{(v / sum(values)) * 100:.1f}%', ha='center', color='black', fontsize=label_fontsize)
            left += v

        percent_early = item['1'] + item['2']
        percent_late = item['4'] + item['5']

        plt.text(-7.5, idx, display_name, va='center', ha='right', fontsize=14)
        plt.text(0, idx, f'{percent_early:.1f}%', va='center', ha='right', fontsize=15)
        plt.text(left + 0.5, idx, f'{percent_late:.1f}%', va='center', ha='left', fontsize=15)

    plt.xlim(0, max_length)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1), title='Response Time')
    plt.box(False)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()
    logger.info(f"Stacked bar chart saved to {output_file}")


def main():
    # Load and correlate three metrics
    merged_1_2, merged_1_3, merged_2_3 = load_and_merge_datasets()

    corr_1_2 = calculate_correlation(merged_1_2, 'no_answer_percentage_1', 'without_accepted_answer_2')
    corr_1_3 = calculate_correlation(merged_1_3, 'no_answer_percentage_1', 'response_time_3')
    corr_2_3 = calculate_correlation(merged_2_3, 'without_accepted_answer_2', 'response_time_3')

    logger.info(f"Correlation between file1 and file2: {corr_1_2}")
    logger.info(f"Correlation between file1 and file3: {corr_1_3}")
    logger.info(f"Correlation between file2 and file3: {corr_2_3}")

    # Load response time data
    data = pd.read_csv(INPUT_FILE)
    data = classify_response_time(data)
    category_counts = count_response_time_categories(data)
    normalized_data = normalize_counts(category_counts)
    plot_stacked_bar_chart(normalized_data)


if __name__ == '__main__':
    main()
