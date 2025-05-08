from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

# sentence_to_number = {
#     'less than 15 minutes': 1,
#     'between 15 to 30 minutes': 2,
#     'between 30 to 60 minutes': 3,
#     'between 1 and 2 hours': 4,
#     'more than 2 hours': 5
# }

columns_time = ['Q12_{}'.format(i) for i in range(1, 36)]
descriptions_time = df.iloc[0, 72:107].tolist()

# cleaned_descriptions_time = []
for desc in descriptions_time:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions_time.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions_time.append('')

# data_time = []

for idx, col in enumerate(columns_time):
#     mapped_col = df[col].map(sentence_to_number)
#     filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     count_1_2 = count_1 + count_2
#     count_4_5 = count_4 + count_5

#     total = count_1_2 + count_3 + count_4_5
percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

#     data_time.append({
#         'column': col,
#         'description': cleaned_descriptions_time[idx],
#         'count_1': count_1,
#         'count_2': count_2,
#         'count_3': count_3,
#         'count_4': count_4,
#         'count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

columns_difficulty = ['Q9_{}'.format(i) for i in range(1, 36)]
descriptions_difficulty = df.iloc[0, 26:61].tolist()

cleaned_descriptions_difficulty = []
for desc in descriptions_difficulty:
if isinstance(desc, str) and '-' in desc:
cleaned_descriptions_difficulty.append(desc.split('-')[-1].strip())
else:
cleaned_descriptions_difficulty.append('')

df[columns_difficulty] = df[columns_difficulty].apply(pd.to_numeric, errors='coerce')

data_difficulty = []

for idx, col in enumerate(columns_difficulty):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     count_1_2 = count_1 + count_2
#     count_4_5 = count_4 + count_5

#     total = count_1_2 + count_3 + count_4_5
percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

data_difficulty.append({
#         'column': col,
'description': cleaned_descriptions_difficulty[idx],
#         'count_1': count_1,
#         'count_2': count_2,
#         'count_3': count_3,
#         'count_4': count_4,
#         'count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')

combined_df = pd.DataFrame(data_time).merge(pd.DataFrame(data_difficulty), on='description')
combined_df = combined_df.merge(stackoverflow_df, left_on='description', right_on='topic_name')

# combined_df['avg_time'] = (
#     (combined_df['count_1_x'] * 1) +
#     (combined_df['count_2_x'] * 2) +
#     (combined_df['count_3_x'] * 3) +
#     (combined_df['count_4_x'] * 4) +
#     (combined_df['count_5_x'] * 5)
# ) / (
#     combined_df['count_1_x'] +
#     combined_df['count_2_x'] +
#     combined_df['count_3_x'] +
#     combined_df['count_4_x'] +
#     combined_df['count_5_x']
# )

combined_df['avg_difficulty'] = (
#     (combined_df['count_1_y'] * 1) +
#     (combined_df['count_2_y'] * 2) +
#     (combined_df['count_3_y'] * 3) +
#     (combined_df['count_4_y'] * 4) +
#     (combined_df['count_5_y'] * 5)
# ) / (
#     combined_df['count_1_y'] +
#     combined_df['count_2_y'] +
#     combined_df['count_3_y'] +
#     combined_df['count_4_y'] +
#     combined_df['count_5_y']
# )

min_difficulty = combined_df['without_accepted_answer'].min()
max_difficulty = combined_df['without_accepted_answer'].max()
# scaled_difficulty = (combined_df['without_accepted_answer'] - min_difficulty) / (max_difficulty - min_difficulty)
# combined_df['size'] = scaled_difficulty * 5000
# combined_df['size'] = combined_df['without_accepted_answer'] * 100


norm = plt.Normalize(vmin=min_difficulty, vmax=max_difficulty)
cmap = plt.get_cmap('Spectral')
# colors = cmap(norm(combined_df['without_accepted_answer']))

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
#     combined_df['avg_time'],
combined_df['avg_difficulty'],
#     s=combined_df['size'],
#     c=combined_df['without_accepted_answer'],
#     cmap='Spectral',
#     alpha=0.6,
#     edgecolor='k'
# )

cbar = plt.colorbar(scatter, label='Percentage of Questions Without Accepted Answer Based on SO')

# for i, row in combined_df.iterrows():
#     plt.annotate(
# #         row['description'],
#         (row['avg_time'], row['avg_difficulty']),
# #         fontsize=8,
# #         alpha=0.8,
# #         ha='center',
# #         va='center'
# #     )

plt.xlabel('Average Time to Resolve Based on Survey (minutes)')
plt.ylabel('Average Difficulty Rating Based on Survey (1-5)')
# plt.title('Challenges Faced by Ruby Developers (Bubble Size = Scaled StackOverflow Difficulty)')

plt.tight_layout()
plt.savefig('difficulty_bubble_chart_step1.pdf')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

# description_to_group = {
#     'Ruby Array and Hash Operations': 'Core Ruby Operations',
#     'Regular Expressions in Ruby': 'Core Ruby Operations',
#     'Algorithm Design in Ruby': 'Algorithm Design',
#     'Advanced Ruby Methods and Metaprogramming': 'Advanced Ruby Concepts',
#     'File Handling and External Integrations': 'Data Handling and Serialization',
#     'Spreadsheet and CSV Management in Ruby': 'Data Handling and Serialization',
#     'JSON and Data Serialization': 'Data Handling and Serialization',
#     'ActiveRecord Associations in Rails': 'Database and ActiveRecord',
#     'Database Management and Schema Design': 'Database and ActiveRecord',
#     'Data Query and Manipulation in Rails': 'Database and ActiveRecord',
#     'Ruby Gem Installation and Configuration Issues': 'Environment and Dependency Management',
#     'Ruby Environment and Dependency Management': 'Environment and Dependency Management',
#     'Automation with Chef': 'Deployment and Infrastructure Management',
#     'Rails Deployment and Server Configuration': 'Deployment and Infrastructure Management',
#     'Heroku Deployment and Configuration': 'Deployment and Infrastructure Management',
#     'System Integration and External Libraries in Ruby': 'System Integration',
#     'Job Scheduling and Background Processes': 'Background Processing',
#     'Ruby on Rails Web Interface and UX Customization': 'Frontend Development in Rails',
#     'Frontend Integration and User Interaction in Rails Applications': 'Frontend Development in Rails',
#     'jQuery and AJAX in Rails': 'Frontend Development in Rails',
#     'Email Delivery with Rails ActionMailer': 'External Services and API Integrations',
#     'Asset Management and Integration Issues': 'External Services and API Integrations',
#     'Search Engines Integration in Rails': 'External Services and API Integrations',
#     'Ruby Payment and Financial Integration': 'External Services and API Integrations',
#     'API Management': 'External Services and API Integrations',
#     'Rails Routing and URLs': 'Routing and URLs',
#     'Time Zone Management and Date Operations in Rails': 'Time and Date Management',
#     'User Authentication and Role Management': 'User Authentication',
#     'Rails Method and Parameter Errors': 'Error Handling and Validation',
#     'Validation and Error Handling in Ruby on Rails': 'Error Handling and Validation',
#     'Rails Mass Assignment & Parameter Protection Issues': 'Error Handling and Validation',
#     'Ruby Debugging and Error Handling': 'Error Handling and Validation',
#     'Automated Testing and Integration Testing in Ruby on Rails': 'Testing and Quality Assurance',
#     'Rails Design Patterns': 'Software Design Patterns',
'Performance Optimization in Rails': 'Performance Optimization'
# }

# sentence_to_number = {
#     'less than 15 minutes': 1,
#     'between 15 to 30 minutes': 2,
#     'between 30 to 60 minutes': 3,
#     'between 1 and 2 hours': 4,
#     'more than 2 hours': 5
# }

columns_time = ['Q12_{}'.format(i) for i in range(1, 36)]
descriptions_time = df.iloc[0, 72:107].tolist()

# cleaned_descriptions_time = []
for desc in descriptions_time:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions_time.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions_time.append('')

group_counts_time = {group: {str(i): 0 for i in range(1, 6)} for group in set(description_to_group.values())}
# logger.info(group_counts_time)
# data_time = []

for idx, description in enumerate(cleaned_descriptions_time):
#     group = description_to_group.get(description, None)
# logger.info(group)
if group:
#         col = columns_time[idx]
# logger.info(idx)
#         mapped_col = df[col].map(sentence_to_number)
#         filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
#         rating_counts = filtered_data.value_counts().sort_index()
# logger.info(group, col)
        
for rating in range(1, 6):
#             group_counts_time[group][str(rating)] += rating_counts.get(rating, 0)

# logger.info(group_counts_time)


for group, counts in group_counts_time.items():
#     total = sum(counts.values())

for idx, group in tqdm(enumerate(group_counts_time.keys()), total=len(group_counts_time.keys())):
#     counts = group_counts_time[group]
#     total = sum(counts.values())

#     count_1 = counts['1']
#     count_2 = counts['2']
#     count_3 = counts['3']
#     count_4 = counts['4']
#     count_5 = counts['5']
    
#     count_1_2 = count_1 + count_2
#     count_4_5 = count_4 + count_5
    
#     total = count_1_2 + count_3 + count_4_5
percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

#     data_time.append({
#         'column': group,
#         'description': cleaned_descriptions_time[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

columns_difficulty = ['Q9_{}'.format(i) for i in range(1, 36)]
descriptions_difficulty = df.iloc[0, 26:61].tolist()

cleaned_descriptions_difficulty = []
for desc in descriptions_difficulty:
if isinstance(desc, str) and '-' in desc:
cleaned_descriptions_difficulty.append(desc.split('-')[-1].strip())
else:
cleaned_descriptions_difficulty.append('')

group_counts_difficulty = {group: {str(i): 0 for i in range(1, 6)} for group in set(description_to_group.values())}
# group_percent_4_5 = {}

for idx, description in enumerate(cleaned_descriptions_difficulty):
#     group = description_to_group.get(description, None)
    
if group:
col = columns_difficulty[idx]
df[col] = pd.to_numeric(df[col], errors='coerce')
        
#         filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#         rating_counts = filtered_data.value_counts().sort_index()
        
for rating in range(1, 6):
group_counts_difficulty[group][str(rating)] += rating_counts.get(rating, 0)

for group, counts in group_counts_difficulty.items():
#     total = sum(counts.values())
if total > 0:
#         count_4_5 = counts['4'] + counts['5']
#         percent_4_5 = (count_4_5 / total) * 100
#         group_percent_4_5[group] = percent_4_5

# sorted_groups = sorted(group_percent_4_5.keys(), key=lambda x: group_percent_4_5[x], reverse=False)

data_difficulty = []

for idx, group in tqdm(enumerate(group_counts_difficulty.keys()), total=len(group_counts_difficulty.keys())):
counts = group_counts_difficulty[group]
#     total = sum(counts.values())

#     count_1 = counts['1']
#     count_2 = counts['2']
#     count_3 = counts['3']
#     count_4 = counts['4']
#     count_5 = counts['5']
    
#     count_1_2 = count_1 + count_2
#     count_4_5 = count_4 + count_5
    
#     total = count_1_2 + count_3 + count_4_5
percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

data_difficulty.append({
#         'column': group,
'description': cleaned_descriptions_difficulty[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step2.csv')



combined_df = pd.DataFrame(data_time).merge(pd.DataFrame(data_difficulty), on='description', suffixes=('_time', '_difficulty'))
combined_df = combined_df.merge(stackoverflow_df, left_on='column_time', right_on='middle_category')


# combined_df['avg_time'] = (
#     (combined_df['norm_count_1_time'] * 1) +
#     (combined_df['norm_count_2_time'] * 2) +
#     (combined_df['norm_count_3_time'] * 3) +
#     (combined_df['norm_count_4_time'] * 4) +
#     (combined_df['norm_count_5_time'] * 5)
# ) / (
#     combined_df['norm_count_1_time'] +
#     combined_df['norm_count_2_time'] +
#     combined_df['norm_count_3_time'] +
#     combined_df['norm_count_4_time'] +
#     combined_df['norm_count_5_time']
# )

combined_df['avg_difficulty'] = (
(combined_df['norm_count_1_difficulty'] * 1) +
(combined_df['norm_count_2_difficulty'] * 2) +
(combined_df['norm_count_3_difficulty'] * 3) +
(combined_df['norm_count_4_difficulty'] * 4) +
(combined_df['norm_count_5_difficulty'] * 5)
# ) / (
combined_df['norm_count_1_difficulty'] +
combined_df['norm_count_2_difficulty'] +
combined_df['norm_count_3_difficulty'] +
combined_df['norm_count_4_difficulty'] +
combined_df['norm_count_5_difficulty']
# )

min_difficulty = combined_df['without_accepted_answer'].min()
max_difficulty = combined_df['without_accepted_answer'].max()
# scaled_difficulty = (combined_df['without_accepted_answer'] - min_difficulty) / (max_difficulty - min_difficulty)
# combined_df['size'] = scaled_difficulty * 5000
# combined_df['size'] = combined_df['without_accepted_answer'] * 100


norm = plt.Normalize(vmin=min_difficulty, vmax=max_difficulty)
cmap = plt.get_cmap('Spectral')
# colors = cmap(norm(combined_df['without_accepted_answer']))

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
#     combined_df['avg_time'],
combined_df['avg_difficulty'],
#     s=combined_df['size'],
#     c=combined_df['without_accepted_answer'],
#     cmap='Spectral',
#     alpha=0.6,
#     edgecolor='k'
# )

cbar = plt.colorbar(scatter, label='Percentage of Questions Without Accepted Answer Based on SO')

# for i, row in combined_df.iterrows():
#     plt.annotate(
# #         row['description'],
#         (row['avg_time'], row['avg_difficulty']),
# #         fontsize=8,
# #         alpha=0.8,
# #         ha='center',
# #         va='center'
# #     )

plt.xlabel('Average Time to Resolve Based on Survey (minutes)')
plt.ylabel('Average Difficulty Rating Based on Survey (1-5)')
# plt.title('Challenges Faced by Ruby Developers (Bubble Size = Scaled StackOverflow Difficulty)')

plt.tight_layout()
plt.savefig('difficulty_bubble_chart_step2.pdf')
plt.show()

from matplotlib.colors import LinearSegmentedColormap
def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from tqdm import tqdm
    import seaborn as sns

    df = pd.read_csv('survey/survey_data.csv')
    stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step3.csv')
    stackoverflow_df2 = pd.read_csv('results/data/median_response_time_step3.csv')


    sentence_to_number = {
        'less than 15 minutes': 1,
        'between 15 to 30 minutes': 2,
        'between 30 to 60 minutes': 3,
        'between 1 and 2 hours': 4,
        'more than 2 hours': 5
    }

    category = df.iloc[-1, 26:61]

    columns_time = ['Q12_{}'.format(i) for i in range(1, 36)]

    data_time = []

    for idx, col in tqdm(enumerate(columns_time), total=len(columns_time)):
        col = columns_time[idx]
        mapped_col = df[col].map(sentence_to_number)
        filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
        rating_counts = filtered_data.value_counts().sort_index()

        count_1 = rating_counts.get(1, 0)
        count_2 = rating_counts.get(2, 0)
        count_3 = rating_counts.get(3, 0)
        count_4 = rating_counts.get(4, 0)
        count_5 = rating_counts.get(5, 0)


        data_time.append({
            'column': col,
            'description': category[idx],
            'norm_count_1_time': count_1,
            'norm_count_2_time': count_2,
            'norm_count_3_time': count_3,
            'norm_count_4_time': count_4,
            'norm_count_5_time': count_5,
        })

    df_data_time = pd.DataFrame(data_time)

    logger.info(df_data_time[''])

    df_grouped_time = df_data_time.groupby('description').agg({
        'norm_count_1_time': 'sum',
        'norm_count_2_time': 'sum',
        'norm_count_3_time': 'sum',
        'norm_count_4_time': 'sum',
        'norm_count_5_time': 'sum',
    }).reset_index()

    columns = ['Q9_{}'.format(i) for i in range(1, 36)]

    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

    data = []

    for idx, col in tqdm(enumerate(columns), total=len(columns)):
        filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
        rating_counts = filtered_data.value_counts().sort_index()

        count_1 = rating_counts.get(1, 0)
        count_2 = rating_counts.get(2, 0)
        count_3 = rating_counts.get(3, 0)
        count_4 = rating_counts.get(4, 0)
        count_5 = rating_counts.get(5, 0)

        data.append({
            'column': col,
            'description': category[idx],
            'norm_count_1': count_1,
            'norm_count_2': count_2,
            'norm_count_3': count_3,
            'norm_count_4': count_4,
            'norm_count_5': count_5
        })

    df_data = pd.DataFrame(data)

    df_grouped = df_data.groupby('description').agg({
        'norm_count_1': 'sum',
        'norm_count_2': 'sum',
        'norm_count_3': 'sum',
        'norm_count_4': 'sum',
        'norm_count_5': 'sum'
    }).reset_index()


    combined_df = pd.DataFrame(df_grouped).merge(df_grouped_time, on='description')
    combined_df = pd.DataFrame(combined_df).merge(stackoverflow_df, left_on='description', right_on='category')
    combined_df = pd.DataFrame(combined_df).merge(stackoverflow_df2, on='category')

    combined_df['avg_time'] = (
        (combined_df['norm_count_1_time'] * 7.5) +
        (combined_df['norm_count_2_time'] * 22.5) +
        (combined_df['norm_count_3_time'] * 45) +
        (combined_df['norm_count_4_time'] * 90) +
        (combined_df['norm_count_5_time'] * 120)
    ) / (
        combined_df['norm_count_1_time'] +
        combined_df['norm_count_2_time'] +
        combined_df['norm_count_3_time'] +
        combined_df['norm_count_4_time'] +
        combined_df['norm_count_5_time']
    )

    combined_df['avg_difficulty'] = ((
        (combined_df['norm_count_1'] * 1) +
        (combined_df['norm_count_2'] * 2) +
        (combined_df['norm_count_3'] * 3) +
        (combined_df['norm_count_4'] * 4) +
        (combined_df['norm_count_5'] * 5)
    ) / (
        combined_df['norm_count_1'] +
        combined_df['norm_count_2'] +
        combined_df['norm_count_3'] +
        combined_df['norm_count_4'] +
        combined_df['norm_count_5']
    ) - 1) * 25

    min_difficulty = combined_df['response_time'].min()
    max_difficulty = combined_df['response_time'].max()

    # combined_df['size'] = combined_df['response_time'] * 70

    logger.info(combined_df)

    norm = plt.Normalize(vmin=min_difficulty, vmax=max_difficulty)
    cmap = plt.get_cmap('Spectral')
    colors = [cmap(i / 10) for i in range(10)]
    logger.info(colors)

    # cmap2 = plt.get_cmap('tab20c')
    # colors2 = [cmap2(i / 20) for i in range(20)]

    plt.figure(figsize=(6, 4))

    sns.regplot(x='avg_time', y='avg_difficulty', data=combined_df, scatter=False, ci=None)

    # from scipy.stats import pearsonr

    # pearson_corr, p_value = pearsonr(combined_df['avg_time'], combined_df['avg_difficulty'])

    # logger.info(f"Pearson Correlation Coefficient: {pearson_corr}")
    # logger.info(f"P-value: {p_value}")

    # from scipy.stats import kendalltau

    # # Assuming average_popularity and average_difficulty are defined as before
    # # average_popularity = combined_df['avg_time']
    # average_difficulty = combined_df['avg_difficulty']

    # # # Calculate Kendall correlation coefficient and p-value
    # kendall_coefficient, kendall_p_value = kendalltau(average_popularity, average_difficulty)

    # # # Output the results
    # logger.info("Kendall Correlation Coefficient:", kendall_coefficient)
    # logger.info("P-value:", kendall_p_value)

    # category_mapping = {
    #     'Application Quality and Security': 0,
    #     'Core Ruby Concepts': 1,
    #     'Data Management and Processing': 2,
    #     'Development Environment and Infrastructure': 3,
    'Software Architecture and Performance': 4,
    #     'Web Application Development': 5
    # }

    scatter = plt.scatter(
    #     combined_df['avg_time'],
    combined_df['avg_difficulty'],
    #     s=1200,
    #     c=combined_df['category'].map(category_mapping),
    #     cmap=cmap,
    #     alpha=0.7,
    #     edgecolor='k'
    # )

    # cbar = plt.colorbar(scatter, label='Percentage of Questions Without Accepted Answer Based on SO')

    # def adjust_category(category):
    #     words = category.split()
    if len(category) > 18:
    #         return ' '.join(words[:2])
    else:
    #         return category

    for i, row in combined_df.iterrows():
    #     # Annotate the description at the bubble position
    if adjust_category(row['description']) == 'Software Architecture':
    plt.annotate(
    #         adjust_category(row['description']),
    (row['avg_time'], row['avg_difficulty']),
    #         fontsize=10,
    #         xytext=(-30, -40),
    #         textcoords='offset points',
    #         alpha=0.8,
    #         ha='center',
    #         va='center'
    #     )
    elif adjust_category(row['description']) == 'Web Application':
    plt.annotate(
    #             adjust_category(row['description']),
    (row['avg_time'], row['avg_difficulty']),
    #             fontsize=10,
    #             xytext=(60, 0),
    #             textcoords='offset points',
    #             alpha=0.8,
    #             ha='center',
    #             va='center'
    #         )
    elif adjust_category(row['description']) == 'Core Ruby Concepts':
    plt.annotate(
    #             adjust_category(row['description']),
    (row['avg_time'], row['avg_difficulty']),
    #             fontsize=10,
    #             xytext=(-30, 25),
    #             textcoords='offset points',
    #             alpha=0.8,
    #             ha='center',
    #             va='center'
    #         )
    else:
    plt.annotate(
    #             adjust_category(row['description']),
    (row['avg_time'], row['avg_difficulty']),
    #             fontsize=10,
    #             xytext=(5, 25),
    #             textcoords='offset points',
    #             alpha=0.8,
    #             ha='center',
    #             va='center'
    #         )

    #     # Draw vertical line to x-axis
    # plt.plot([row['avg_time'], row['avg_time']], [0, row['avg_difficulty']], color='gray', linestyle='--', linewidth=0.7)
        
    #     # Draw horizontal line to y-axis
    # plt.plot([0, row['avg_time']], [row['avg_difficulty'], row['avg_difficulty']], color='gray', linestyle='--', linewidth=0.7)

    # Add text labels for the lines
    # plt.text(row['avg_time'], 0, str(round(row['avg_time'], 2)), fontsize=8, ha='center', va='bottom')
    # plt.text(0, row['avg_difficulty'], str(round(row['avg_difficulty'], 2)), fontsize=8, ha='right', va='center')

    plt.xlim(left=combined_df['avg_time'].min() - 0.5, right=combined_df['avg_time'].max() + 0.5)  # Adjust as needed
    plt.ylim(bottom=combined_df['avg_difficulty'].min() - 0.5, top=combined_df['avg_difficulty'].max() + 0.5)  # Adjust as needed

    plt.xlabel('Average Time to Resolve Based on Survey (minutes)')
    plt.ylabel('Average Difficulty Rating Based on Survey (1-5)')

    plt.tight_layout()
    plt.savefig('new_color_difficulty_bubble_chart_step3.pdf')
    plt.show()

if __name__ == '__main__':
    main()