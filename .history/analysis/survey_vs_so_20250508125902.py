import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.stats import shapiro, ttest_rel
import seaborn as sns

# ========== CONFIGURATION ==========
SURVEY_FILE = 'survey/survey_data.csv'
COLUMNS = [f'Q9_{i}' for i in range(1, 36)]
COLUMNS_Q12 = [f'Q12_{i}' for i in range(1, 36)]
MAX_LENGTH = 100

SENTENCE_TO_MINUTES = {
    'less than 15 minutes': 7.5,
    'between 15 to 30 minutes': 22.5,
    'between 30 to 60 minutes': 45,
    'between 1 and 2 hours': 90,
    'more than 2 hours': 120
}

# ========== UTILITY FUNCTIONS ==========

def clean_descriptions(raw_descriptions):
    return [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in raw_descriptions]

def compute_weighted_average(counts):
    total = sum(counts.values())
    return sum(i * counts.get(i, 0) for i in range(1, 6)) / total if total else 0

def adjust_category_name(name):
    words = name.split()
    return ' '.join(words[:2]) if len(name) > 18 else name

def run_shapiro_test(label, series):
    stat, p = shapiro(series)
    result = "looks normally distributed." if p > 0.05 else "does not look normally distributed."
    print(f"Shapiro-Wilk Test for {label}: Statistic = {stat:.4f}, p = {p:.4f} → {result}")

def run_ttest(series1, series2):
    t_stat, p_value = ttest_rel(series1, series2)
    print(f"T-test Statistic = {t_stat:.4f}, p-value = {p_value:.4f}")

# ========== PLOTTING FUNCTIONS ==========

def plot_dot_chart(df, x1, x2, y_labels, filename, title, xlabel):
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]

    plt.figure(figsize=(12, len(df) * 0.4))
    plt.scatter(df[x1], np.arange(len(df)), label='Survey', color=colors[0], marker='o')
    plt.scatter(df[x2], np.arange(len(df)), label='StackOverflow', color=colors[4], marker='x')

    for i in range(len(df)):
        plt.plot([df[x1].iloc[i], df[x2].iloc[i]], [i, i], color='gray', linestyle='--', alpha=0.7)

    plt.yticks(np.arange(len(df)), y_labels, fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_radar_chart(labels, survey_values, so_values, filename, title):
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
    survey_values += [survey_values[0]]
    so_values += [so_values[0]]

    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, survey_values, color=colors[0], linewidth=2, label='Survey')
    ax.fill(angles, survey_values, color=colors[0], alpha=0.25)
    ax.plot(angles, so_values, color=colors[4], linewidth=2, linestyle='--', label='StackOverflow')
    ax.fill(angles, so_values, color=colors[4], alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9, ha='right', rotation=45)
    ax.set_yticklabels([])
    plt.title(title)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_correlation_regression(x, y, df, filename, xlabel, ylabel, title):
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]
    plt.figure(figsize=(8, 4))
    sns.regplot(x=x, y=y, data=df, scatter=True, color=colors[0], ci=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# ========== ANALYSIS WORKFLOW ==========

def difficulty_analysis(df, so_df, row_idx, so_col, prefix):
    descriptions = df.iloc[row_idx, 26:61].tolist()
    cleaned_desc = clean_descriptions(descriptions)
    df[COLUMNS] = df[COLUMNS].apply(pd.to_numeric, errors='coerce')

    data = []
    for idx, col in enumerate(COLUMNS):
        filtered = df[col][(df[col] >= 1) & (df[col] <= 5)]
        counts = filtered.value_counts().sort_index()
        avg = compute_weighted_average(counts)
        data.append({'description': cleaned_desc[idx], 'average': (avg - 1) * 25})

    combined_df = pd.DataFrame(data).merge(so_df, left_on='description', right_on=so_col)

    plot_dot_chart(combined_df, 'average', 'without_accepted_answer',
                   combined_df[so_col], f'{prefix}_dot_chart.pdf',
                   f'{prefix.title()} Survey vs SO Difficulty', 'Difficulty Level (0–100)')

    run_shapiro_test('Survey', combined_df['average'])
    run_shapiro_test('SO', combined_df['without_accepted_answer'])
    run_ttest(combined_df['average'], combined_df['without_accepted_answer'])

    plot_radar_chart(
        [adjust_category_name(c) for c in combined_df[so_col].tolist()],
        combined_df['average'].tolist(),
        combined_df['without_accepted_answer'].tolist(),
        f'{prefix}_radar_chart.pdf',
        f'{prefix.title()} Radar Chart: Survey vs SO Difficulty'
    )

def time_analysis(df, so_df):
    category_labels = df.iloc[-1, 26:61].tolist()

    data_time = []
    for idx, col in enumerate(COLUMNS_Q12):
        mapped = df[col].map(SENTENCE_TO_MINUTES)
        counts = mapped.value_counts()
        total = counts.sum()
        weighted_avg = sum(v * counts.get(k, 0) for k, v in SENTENCE_TO_MINUTES.items()) / total
        data_time.append({'description': category_labels[idx], 'avg_time': weighted_avg})

    avg_time_df = pd.DataFrame(data_time)
    combined_df = avg_time_df.merge(so_df, left_on='description', right_on='category')

    plot_radar_chart(
        [adjust_category_name(c) for c in combined_df['category']],
        combined_df['avg_time'].tolist(),
        combined_df['response_time'].tolist(),
        'time_radar_chart.pdf',
        'Survey Time vs StackOverflow Response Time'
    )

    run_shapiro_test('Survey Time', combined_df['avg_time'])
    run_shapiro_test('SO Response Time', combined_df['response_time'])
    run_ttest(combined_df['avg_time'], combined_df['response_time'])

    plot_correlation_regression(
        'avg_time', 'response_time', combined_df,
        'time_correlation.pdf',
        'Avg Survey Time (min)', 'SO Response Time (min)',
        'Time Correlation: Survey vs SO'
    )

# ========== MAIN ==========

def main():
    df = pd.read_csv(SURVEY_FILE)
    so_topic = pd.read_csv('results/data/no_accepted_answers_step1.csv')
    so_middle = pd.read_csv('results/data/no_accepted_answers_step2.csv')
    so_high = pd.read_csv('results/data/no_accepted_answers_step3.csv')
    so_time = pd.read_csv('results/data/median_response_time_step3.csv')

    difficulty_analysis(df, so_topic, row_idx=0, so_col='topic_name', prefix='topic')
    difficulty_analysis(df, so_middle, row_idx=-2, so_col='middle_category', prefix='middle')
    difficulty_analysis(df, so_high, row_idx=-1, so_col='category', prefix='high')

    time_analysis(df, so_time)

if __name__ == "__main__":
    main()
