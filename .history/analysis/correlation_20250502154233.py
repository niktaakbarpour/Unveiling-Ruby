from utils.common import logger

import pandas as pd
from scipy.stats import pearsonr
import numpy as np

df1 = pd.read_csv('results/data/no_answer_percentage_step1.csv', usecols=[0, 1])
df2 = pd.read_csv('results/data/no_accepted_answers_step1.csv', usecols=[0, 1])
df3 = pd.read_csv('results/data/median_response_time_step1.csv', usecols=[0, 1])

merged_df_1_2 = pd.merge(df1, df2, on='topic_name', suffixes=('_1', '_2'))
merged_df_1_3 = pd.merge(df1, df3, on='topic_name', suffixes=('_1', '_3'))
merged_df_2_3 = pd.merge(df2, df3, on='topic_name', suffixes=('_2', '_3'))

# # Define a function to calculate correlation with NaN and inf handling
# def calculate_correlation(df, col_a, col_b):
# Select the two columns for correlation
data = df[[col_a, col_b]].replace([np.inf, -np.inf], np.nan).dropna()
# Calculate and return correlation if there is data remaining
if len(data) > 1:  # Pearson correlation needs at least two data points
#         return pearsonr(data[col_a], data[col_b])[0]
else:
logger.info(f"Not enough valid data in columns {col_a} and {col_b} after removing NaN/inf.")
#         return None

# # Use actual column names based on each merged DataFrame
# corr_1_2 = calculate_correlation(merged_df_1_2, 'no_answer_percentage', 'without_accepted_answer')
# corr_1_3 = calculate_correlation(merged_df_1_3, 'no_answer_percentage', 'response_time')
# corr_2_3 = calculate_correlation(merged_df_2_3, 'without_accepted_answer', 'response_time')

# # Print the results
logger.info(f"Correlation between file1 and file2: {corr_1_2}")
logger.info(f"Correlation between file1 and file3: {corr_1_3}")
logger.info(f"Correlation between file2 and file3: {corr_2_3}")




import pandas as pd

# def calculate_response_time(data):
data['CreationDate'] = pd.to_datetime(data['CreationDate'], errors='coerce')
data['accepted_answer_creation_date'] = pd.to_datetime(data['accepted_answer_creation_date'], errors='coerce')
    
#     data['response_time'] = (data['accepted_answer_creation_date'] - data['CreationDate']).dt.total_seconds() / 60
  
#     response_times = data.dropna(subset=['accepted_answer_creation_date'])
    
#     def categorize_response_time(minutes):
if minutes < 15:
#             return 1
elif 15 <= minutes < 30:
#             return 2
elif 30 <= minutes < 60:
#             return 3
elif 60 <= minutes < 120:
#             return 4
else:
#             return 5
    
#     response_times['response_time_category'] = response_times['response_time'].apply(categorize_response_time)
    
#     return response_times

# input_file = 'results/data/final_category.csv'
data = pd.read_csv(input_file)

# response_time = calculate_response_time(data)

# output_file = 'results/data/response_time.csv'
# response_time.to_csv(output_file, index=False)

logger.info(f"The response time per row, including categories, has been saved to {output_file}")

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    from collections import defaultdict

    # Load the original data
    input_file = 'results/data/final_category.csv'
    data = pd.read_csv(input_file)

    # Calculate response time
    def calculate_response_time(data):
        data['CreationDate'] = pd.to_datetime(data['CreationDate'], errors='coerce')
        data['accepted_answer_creation_date'] = pd.to_datetime(data['accepted_answer_creation_date'], errors='coerce')
        data['response_time'] = (data['accepted_answer_creation_date'] - data['CreationDate']).dt.total_seconds() / 60

    # Classify the response time into categories
        conditions = [
            (data['response_time'] < 15),
            (data['response_time'] >= 15) & (data['response_time'] < 30),
            (data['response_time'] >= 30) & (data['response_time'] < 60),
            (data['response_time'] >= 60) & (data['response_time'] < 120),
            (data['response_time'] >= 120)
        ]
        choices = [1, 2, 3, 4, 5]
        
        data['response_time_category'] = pd.cut(data['response_time'], bins=[-1, 15, 30, 60, 120, float('inf')], labels=choices)
        return data

    # Calculate response time and assign categories
    data = calculate_response_time(data)

    # Filter out rows with missing category or response_time_category
    data = data.dropna(subset=['category', 'response_time_category'])

    # Define a dictionary to store counts of each response time category within each category
    category_counts = defaultdict(lambda: {str(i): 0 for i in range(1, 6)})

    # Count occurrences of each response time category (1-5) within each category
    for _, row in data.iterrows():
        category = row['category']
        response_time_category = str(int(row['response_time_category']))
        category_counts[category][response_time_category] += 1

    logger.info(category_counts)

    Normalize counts for a 100-point bar chart length
    max_length = 100
    data_to_plot = []
    for category, counts in category_counts.items():
        total = sum(counts.values())
        
        # Normalize counts based on total and max_length
        norm_counts = {k: (v / total) * max_length for k, v in counts.items()}
        
        data_to_plot.append({
            'category': category,
            **norm_counts
        })

    Sort the data by category name for a consistent order in the bar chart
    data_to_plot = sorted(data_to_plot, key=lambda x: x['4'] + x['5'])

    Set colors for each response time category
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]

    # Plot the stacked bar chart
    plt.figure(figsize=(12, 3))

    for idx, item in enumerate(data_to_plot):
        # Get the normalized counts
        norm_count_1 = item['1']
        norm_count_2 = item['2']
        norm_count_3 = item['3']
        norm_count_4 = item['4']
        norm_count_5 = item['5']
        norm_percent_4_5 = item['4'] + item['5']
        norm_percent_1_2 = item['1'] + item['2']

        total_norm_count = norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5
        
    # Stack each bar segment for the response time categories
        plt.barh(item['category'], norm_count_1, color=colors[0], label='less than 15 minutes' if idx == 0 else "")
        plt.barh(item['category'], norm_count_2, left=norm_count_1, color=colors[1], label='15 to 30 minutes' if idx == 0 else "")
        plt.barh(item['category'], norm_count_3, left=norm_count_1 + norm_count_2, color=colors[18], label='30 to 60 minutes' if idx == 0 else "")
        plt.barh(item['category'], norm_count_4, left=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='1 to 2 hours' if idx == 0 else "")
        plt.barh(item['category'], norm_count_5, left=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='more than 2 hours' if idx == 0 else "")
        
        label_fontsize = 16

        plt.text(norm_count_1 / 2, idx - 0.25, f'{(norm_count_1 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 / 1.1, idx - 0.25, f'{(norm_count_2 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 / 1.1, idx - 0.25, f'{(norm_count_3 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, idx - 0.25, f'{(norm_count_4 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5, idx - 0.25, f'{(norm_count_5 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)

        plt.text(0, idx, f'{norm_percent_1_2:.1f}%', va='center', ha='right', color='black', fontsize=15)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 + 0.5, idx, f'{norm_percent_4_5:.1f}%', va='center', ha='left', color='black', fontsize=15)

        words = item['category'].split()

        if item['category'] == "Development Environment and Infrastructure":
            display_category = "Dev. Env."
        elif item['category'] == "Software Architecture and Performance":
            display_category = "Arch."
        elif item['category'] == "Web Application Development":
            display_category = "App. Dev."
        elif item['category'] == "Application Quality and Security":
            display_category = "App. Quality"
        elif item['category'] == "Core Ruby Concepts":
            display_category = "Core"
        elif item['category'] == "Data Management and Processing":
            display_category = "Data"

        plt.text(-7.5, idx, f'{display_category}', va='center', ha='right', rotation=0, fontsize=14)

    # Set up legend and labels
    plt.xlim(0, max_length)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.xlabel('')
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1), title='Response Time')
    plt.box(False)
    plt.tight_layout()
    plt.savefig('receive_accepted_answer_step3333333.pdf')

    # Show plot
    plt.show()

if __name__ == '__main__':
    main()