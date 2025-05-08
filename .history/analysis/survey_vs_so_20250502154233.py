from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')

columns = ['Q9_{}'.format(i) for i in range(1, 36)]

descriptions = df.iloc[0, 26:61].tolist()

# cleaned_descriptions = []
for desc in descriptions:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions.append('')

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []
# max_length = 100

for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'column': col,
#         'description': cleaned_descriptions[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,
#     })

combined_df = pd.DataFrame(data).merge(stackoverflow_df, left_on='description', right_on='topic_name')

logger.info(combined_df)

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(12, 8))

plt.scatter(combined_df['average'], np.arange(len(combined_df)), label='Survey Difficulty', color=colors[0], zorder=5, marker='o')

plt.scatter(combined_df['without_accepted_answer'], np.arange(len(combined_df)), label='StackOverflow Difficulty', color=colors[4], zorder=5, marker='x')

for i in range(len(combined_df)):
plt.plot(
#         [combined_df['average'].iloc[i], combined_df['without_accepted_answer'].iloc[i]],
#         [i, i],
#         color='gray', linestyle='--', alpha=0.7
#     )

plt.grid(True, linestyle='--', alpha=0.7)

plt.yticks(np.arange(len(combined_df)), combined_df['topic_name'], fontsize=8)
plt.xlabel('Difficulty Level')
# plt.title('Comparison of Survey Difficulty and StackOverflow Difficulty')

plt.legend()

plt.tight_layout()
# plt.savefig('dot_chart_step1.pdf')
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step2.csv')

middle_category = df.iloc[-2, 26:61]

columns = ['Q9_{}'.format(i) for i in range(1, 36)]

# for i, desc in enumerate(middle_category):
#     logger.info(len(desc))

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []

for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'column': col,
#         'description': middle_category[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,
#     })

df_data = pd.DataFrame(data)

# df_grouped = df_data.groupby('description').agg({
#     'norm_count_1': 'sum',
#     'norm_count_2': 'sum',
#     'norm_count_3': 'sum',
#     'norm_count_4': 'sum',
#     'norm_count_5': 'sum',
#     'average': 'mean'
# }).reset_index()

combined_df = pd.DataFrame(df_grouped).merge(stackoverflow_df, left_on='description', right_on='middle_category')

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(12, 8))

plt.scatter(combined_df['average'], np.arange(len(combined_df)), label='Survey Difficulty', color=colors[0], zorder=5, marker='o')

plt.scatter(stackoverflow_df['without_accepted_answer'], np.arange(len(stackoverflow_df)), label='StackOverflow Difficulty', color=colors[4], zorder=5, marker='x')

for i in range(len(combined_df)):
plt.plot(
#         [combined_df['average'].iloc[i], combined_df['without_accepted_answer'].iloc[i]],
#         [i, i],
#         color='gray', linestyle='--', alpha=0.7
#     )

plt.grid(True, linestyle='--', alpha=0.7)

plt.yticks(np.arange(len(combined_df)), combined_df['middle_category'], fontsize=8)
plt.xlabel('Difficulty Level')
plt.title('Comparison of Survey Difficulty and StackOverflow Difficulty')

plt.legend()

plt.tight_layout()
# plt.savefig('difficulty_comparison_dot_chart.png')  # Save the plot as a PNG file
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step3.csv')

middle_category = df.iloc[-1, 26:61]

columns = ['Q9_{}'.format(i) for i in range(1, 36)]

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []

for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / (count_1 + count_2 + count_3 + count_4 + count_5)

#     data.append({
#         'column': col,
#         'description': middle_category[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,
#     })

df_data = pd.DataFrame(data)

# df_grouped = df_data.groupby('description').agg({
#     'norm_count_1': 'sum',
#     'norm_count_2': 'sum',
#     'norm_count_3': 'sum',
#     'norm_count_4': 'sum',
#     'norm_count_5': 'sum',
#     'average': 'mean'
# }).reset_index()

logger.info(df_grouped)

combined_df = pd.DataFrame(df_grouped).merge(stackoverflow_df, left_on='description', right_on='category')

# from scipy.stats import shapiro

# # stat_so, p_so = shapiro(combined_df['without_accepted_answer'])
# # stat_survey, p_survey = shapiro(combined_df['average'])

# logger.info(f"Shapiro-Wilk Test for SO Data: Statistic = {stat_so}, p-value = {p_so}")
# logger.info(f"Shapiro-Wilk Test for Survey Data: Statistic = {stat_survey}, p-value = {p_survey}")

# # alpha = 0.05

# if p_so > alpha:
#     logger.info("SO data average looks normally distributed.")
# else:
#     logger.info("SO data average does not look normally distributed.")

# if p_survey > alpha:
#     logger.info("Survey data average looks normally distributed.")
# else:
#     logger.info("Survey data average does not look normally distributed.")



# from scipy import stats


# # t_statistic, t_p_value = stats.ttest_rel(combined_df['average'], combined_df['without_accepted_answer'])
# logger.info("Paired Sample T-test Statistic:", t_statistic)
# logger.info("P-value for T-test:", t_p_value)


cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(7, 2))

plt.scatter(combined_df['average'], np.arange(len(combined_df)), label='Survey Difficulty', color=colors[0], zorder=7, marker='o')

plt.scatter(stackoverflow_df['without_accepted_answer'], np.arange(len(stackoverflow_df)), label='StackOverflow Difficulty', color=colors[4], zorder=7, marker='x')


for i in range(len(combined_df)):
plt.plot(
#         [combined_df['average'].iloc[i], combined_df['without_accepted_answer'].iloc[i]],
#         [i, i],
#         color='gray', linestyle='--', alpha=0.7
#     )

plt.grid(True, linestyle='--', alpha=0.7)
# logger.info(type(combined_df['category']))

# def adjust_category(category):
#     words = category.split()
if len(category) > 18:
#         return ' '.join(words[:2])
else:
#         return category
    
# logger.info(combined_df, stackoverflow_df)

plt.yticks(np.arange(len(combined_df)), combined_df['category'].apply(adjust_category), fontsize=10)
plt.xlabel('Difficulty Level (percentage)')
# plt.title('Comparison of Survey Difficulty and StackOverflow Difficulty')

plt.legend()

plt.tight_layout()
# plt.savefig('difficulty_comparison_dot_chart_step3.pdf')  # Save the plot as a PNG file
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/median_response_time_step3.csv')

# sentence_to_number = {
#     'less than 15 minutes': 1,
#     'between 15 to 30 minutes': 2,
#     'between 30 to 60 minutes': 3,
#     'between 1 and 2 hours': 4,
#     'more than 2 hours': 5
# }

category = df.iloc[-1, 26:61]

columns_time = ['Q12_{}'.format(i) for i in range(1, 36)]

# data_time = []

for idx, col in tqdm(enumerate(columns_time), total=len(columns_time)):
#     col = columns_time[idx]
#     mapped_col = df[col].map(sentence_to_number)
#     filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)


#     data_time.append({
#         'column': col,
#         'description': category[idx],
#         'norm_count_1_time': count_1,
#         'norm_count_2_time': count_2,
#         'norm_count_3_time': count_3,
#         'norm_count_4_time': count_4,
#         'norm_count_5_time': count_5,
#     })

df_data_time = pd.DataFrame(data_time)


# df_grouped_time = df_data_time.groupby('description').agg({
#     'norm_count_1_time': 'sum',
#     'norm_count_2_time': 'sum',
#     'norm_count_3_time': 'sum',
#     'norm_count_4_time': 'sum',
#     'norm_count_5_time': 'sum',
# }).reset_index()

combined_df = pd.DataFrame(df_grouped_time).merge(stackoverflow_df, left_on='description', right_on='category')

# combined_df['avg_time'] = (
#     (combined_df['norm_count_1_time'] * 7.5) +
#     (combined_df['norm_count_2_time'] * 22.5) +
#     (combined_df['norm_count_3_time'] * 45) +
#     (combined_df['norm_count_4_time'] * 90) +
#     (combined_df['norm_count_5_time'] * 120)
# ) / (
#     combined_df['norm_count_1_time'] +
#     combined_df['norm_count_2_time'] +
#     combined_df['norm_count_3_time'] +
#     combined_df['norm_count_4_time'] +
#     combined_df['norm_count_5_time']
# )

# # cmap = plt.get_cmap('tab20c')
# # colors = [cmap(i / 20) for i in range(20)]

# # # def radar_chart(labels, values_survey, values_stackoverflow):
# # #     num_vars = len(labels)
# #     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
# # #     angles += angles[:1]

# # #     values_survey += values_survey[:1]
# # #     values_stackoverflow += values_stackoverflow[:1]

# #     fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
# #     ax.plot(angles, values_survey, color=colors[0], linewidth=2, label='Survey Difficulty')
# # #     ax.fill(angles, values_survey, color=colors[0], alpha=0.25)

# #     ax.plot(angles, values_stackoverflow, color=colors[4], linewidth=2, linestyle='--', label='StackOverflow Difficulty')
# # #     ax.fill(angles, values_stackoverflow, color=colors[4], alpha=0.25)

# # #     ax.set_yticklabels([])
# # #     ax.set_xticks(angles[:-1])
# # #     ax.set_xticklabels(labels, rotation=45, ha='right')

# #     # plt.title('Radar Chart Comparison of Survey and StackOverflow Difficulty')
# #     plt.legend(loc='upper right')
# #     # plt.savefig('radar_chart_step1.pdf')
# #     plt.show()

# # # labels = combined_df['description'].tolist()
# # # values_survey = combined_df['avg_time'].tolist()
# # # values_stackoverflow = combined_df['response_time'].tolist()

# # # radar_chart(labels, values_survey, values_stackoverflow)

# from scipy.stats import shapiro

# # stat_so, p_so = shapiro(combined_df['response_time'])
# # stat_survey, p_survey = shapiro(combined_df['avg_time'])

# logger.info(f"Shapiro-Wilk Test for SO Data: Statistic = {stat_so}, p-value = {p_so}")
# logger.info(f"Shapiro-Wilk Test for Survey Data: Statistic = {stat_survey}, p-value = {p_survey}")

# # alpha = 0.05

# if p_so > alpha:
#     logger.info("SO data average looks normally distributed.")
# else:
#     logger.info("SO data average does not look normally distributed.")

# if p_survey > alpha:
#     logger.info("Survey data average looks normally distributed.")
# else:
#     logger.info("Survey data average does not look normally distributed.")



from scipy import stats


# t_statistic, t_p_value = stats.ttest_rel(combined_df['avg_time'], combined_df['response_time'])
logger.info("Paired Sample T-test Statistic:", t_statistic)
logger.info("P-value for T-test:", t_p_value)
import seaborn as sns

logger.info(np.corrcoef(combined_df['avg_time'], combined_df['response_time'])[0,1])

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(7, 2))
plt.scatter(combined_df['avg_time'], combined_df['response_time'])
sns.regplot(x='avg_time', y='response_time', data=combined_df, scatter=False, color=colors[0], ci=None)


plt.scatter(combined_df['avg_time'], np.arange(len(combined_df)), label='Survey Time', color=colors[0], zorder=7, marker='o')

plt.scatter(stackoverflow_df['response_time'], np.arange(len(stackoverflow_df)), label='StackOverflow Time', color=colors[4], zorder=7, marker='x')


for i in range(len(combined_df)):
plt.plot(
#         [combined_df['avg_time'].iloc[i], combined_df['response_time'].iloc[i]],
#         [i, i],
#         color='gray', linestyle='--', alpha=0.7
#     )

plt.grid(True, linestyle='--', alpha=0.7)
# logger.info(type(combined_df['category']))

# def adjust_category(category):
#     words = category.split()
if len(category) > 18:
#         return ' '.join(words[:2])
else:
#         return category
    
# logger.info(combined_df, stackoverflow_df)

plt.yticks(np.arange(len(combined_df)), combined_df['category'].apply(adjust_category), fontsize=10)
plt.xlabel('Time (minutes)')
# plt.title('Comparison of Survey Difficulty and StackOverflow Difficulty')

plt.legend()

plt.tight_layout()
plt.savefig('time_comparison_dot_chart_step3.pdf')  # Save the plot as a PNG file
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')

columns = ['Q9_{}'.format(i) for i in range(1, 36)]
descriptions = df.iloc[0, 26:61].tolist()

# cleaned_descriptions = []
for desc in descriptions:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions.append('')

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []
for idx, col in enumerate(columns):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'description': cleaned_descriptions[idx],
#         'average': (average - 1) * 25,
#     })

combined_df = pd.DataFrame(data).merge(stackoverflow_df, left_on='description', right_on='topic_name')

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

# def radar_chart(labels, values_survey, values_stackoverflow):
#     num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#     angles += angles[:1]

#     values_survey += values_survey[:1]
#     values_stackoverflow += values_stackoverflow[:1]

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
ax.plot(angles, values_survey, color=colors[0], linewidth=2, label='Survey Difficulty')
#     ax.fill(angles, values_survey, color=colors[0], alpha=0.25)

ax.plot(angles, values_stackoverflow, color=colors[4], linewidth=2, linestyle='--', label='StackOverflow Difficulty')
#     ax.fill(angles, values_stackoverflow, color=colors[4], alpha=0.25)

#     ax.set_yticklabels([])
#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(labels, rotation=45, ha='right')

# plt.title('Radar Chart Comparison of Survey and StackOverflow Difficulty')
plt.legend(loc='upper right')
plt.savefig('radar_chart_step1.pdf')
plt.show()

# labels = combined_df['description'].tolist()
# values_survey = combined_df['average'].tolist()
# values_stackoverflow = combined_df['without_accepted_answer'].tolist()

# radar_chart(labels, values_survey, values_stackoverflow)

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step2.csv')

middle_category = df.iloc[-2, 26:61]

columns = ['Q9_{}'.format(i) for i in range(1, 36)]

# for i, desc in enumerate(middle_category):
#     logger.info(len(desc))

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []

for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'column': col,
#         'description': middle_category[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,
#     })

df_data = pd.DataFrame(data)

# df_grouped = df_data.groupby('description').agg({
#     'norm_count_1': 'sum',
#     'norm_count_2': 'sum',
#     'norm_count_3': 'sum',
#     'norm_count_4': 'sum',
#     'norm_count_5': 'sum',
#     'average': 'mean'
# }).reset_index()

combined_df = pd.DataFrame(df_grouped).merge(stackoverflow_df, left_on='description', right_on='middle_category')

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

# def radar_chart(labels, values_survey, values_stackoverflow):
#     num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#     angles += angles[:1]

#     values_survey += values_survey[:1]
#     values_stackoverflow += values_stackoverflow[:1]

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
ax.plot(angles, values_survey, color=colors[0], linewidth=2, label='Survey Difficulty')
#     ax.fill(angles, values_survey, color=colors[0], alpha=0.25)

ax.plot(angles, values_stackoverflow, color=colors[4], linewidth=2, linestyle='--', label='StackOverflow Difficulty')
#     ax.fill(angles, values_stackoverflow, color=colors[4], alpha=0.25)

#     ax.set_yticklabels([])
#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(labels, rotation=45, ha='right')

# plt.title('Radar Chart Comparison of Survey and StackOverflow Difficulty')
plt.legend(loc='upper right')

plt.show()

# labels = combined_df['description'].tolist()
# values_survey = combined_df['average'].tolist()
# values_stackoverflow = combined_df['without_accepted_answer'].tolist()

# radar_chart(labels, values_survey, values_stackoverflow)


import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step3.csv')

category = df.iloc[-1, 26:61]

columns = ['Q9_{}'.format(i) for i in range(1, 36)]

df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# data = []

for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'column': col,
#         'description': category[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,
#     })

df_data = pd.DataFrame(data)

# df_grouped = df_data.groupby('description').agg({
#     'norm_count_1': 'sum',
#     'norm_count_2': 'sum',
#     'norm_count_3': 'sum',
#     'norm_count_4': 'sum',
#     'norm_count_5': 'sum',
#     'average': 'mean'
# }).reset_index()

combined_df = pd.DataFrame(df_grouped).merge(stackoverflow_df, left_on='description', right_on='category')

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

# def radar_chart(labels, values_survey, values_stackoverflow):
#     num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#     angles += angles[:1]

#     values_survey += values_survey[:1]
#     values_stackoverflow += values_stackoverflow[:1]

fig, ax = plt.subplots(figsize=(5, 4.75), subplot_kw=dict(polar=True))
#     ax.plot(angles, values_survey, color=colors[0], linewidth=2, label='Survey')
#     ax.fill(angles, values_survey, color=colors[0], alpha=0.25)

#     ax.plot(angles, values_stackoverflow, color=colors[4], linewidth=2, linestyle='--', label='StackOverflow')
#     ax.fill(angles, values_stackoverflow, color=colors[4], alpha=0.25)

#     ax.set_yticklabels([])
#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels([])

plt.legend(loc='upper left', bbox_to_anchor=(0.3, 1.15))
plt.savefig('radar_chart_step3.pdf')
# plt.show()

# labels = combined_df['description'].tolist()
# values_survey = combined_df['average'].tolist()
# values_stackoverflow = combined_df['without_accepted_answer'].tolist()

# def adjust_category(category):
#     words = category.split()
if len(category) > 18:
#         return ' '.join(words[:2])
else:
#         return category

radar_chart([adjust_category(category) for category in labels], values_survey, values_stackoverflow)