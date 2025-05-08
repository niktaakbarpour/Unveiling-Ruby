from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt

# # Load the dataset
df = pd.read_csv('results/data/final_category.csv', low_memory=False)

# # Convert 'CreationDate' to datetime
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)

# # Drop rows with invalid 'CreationDate'
df = df.dropna(subset=['CreationDate'])

# # Create a 'Day' column from 'CreationDate'
# df['Day'] = df['CreationDate'].dt.date

# Create counts for different time frames
# time_frames = {
'After GPT': (pd.to_datetime('2022-11-30'), pd.to_datetime('2023-04-30')),
'Before GPT': (pd.to_datetime('2022-06-30'), pd.to_datetime('2022-11-30')),
'Before COVID': (pd.to_datetime('2019-10-11'), pd.to_datetime('2020-03-11')),
'After COVID': (pd.to_datetime('2020-03-11'), pd.to_datetime('2020-08-11')),
'After COVID': (pd.to_datetime('2020-08-11'), pd.to_datetime('2021-01-11')),
# 'During COVID': (pd.to_datetime('2020-03-11'), pd.to_datetime('2020-08-11')),  # New time frame
# 'After COVID': (pd.to_datetime('2023-05-05'), pd.to_datetime('2023-10-05'))
# }

# # Create a new DataFrame to hold the counts
counts = pd.DataFrame()

# Count occurrences for each time frame
for label, (start, end) in time_frames.items():
#     count = df[(df['CreationDate'] >= start) & (df['CreationDate'] <= end)]
#     count_per_day = count.groupby('Day').size().reset_index(name='Count')
#     count_per_day['TimeFrame'] = label
counts = pd.concat([counts, count_per_day], ignore_index=True)

# Calculate averages for each time frame
# # average_counts = {}
# for label in time_frames.keys():
# #     avg_count = counts[counts['TimeFrame'] == label]['Count'].mean()
# #     average_counts[label] = avg_count

# # Plotting
plt.figure(figsize=(12, 6))

# # Plot each time frame in the line chart
for label in counts['TimeFrame'].unique():
#     frame_data = counts[counts['TimeFrame'] == label]
plt.plot(frame_data['Day'], frame_data['Count'], marker='', linestyle='-', label=label)

# Add horizontal lines for specific dates
specific_dates = [
#     '2022-11-30', '2023-04-30', '2022-06-30', 
#     '2020-03-11', '2019-10-11', '2023-10-05', 
#     '2020-08-11'
# ]
for date in specific_dates:
plt.axvline(x=pd.to_datetime(date), color='#ffa600', linestyle='--')

# # Add average change lines between adjacent time frames
# time_frame_labels = list(time_frames.keys())
for i in range(len(time_frame_labels) - 1):
#     label1 = time_frame_labels[i]
#     label2 = time_frame_labels[i + 1]
    
#     # avg1 = average_counts[label1]
#     # avg2 = average_counts[label2]
    
# Calculate the midpoints for the x-axis
#     mid_x1 = time_frames[label1][1]  # End of the first time frame
#     mid_x2 = time_frames[label2][0]  # Start of the second time frame
    
#     # Draw a line connecting the averages
# plt.plot([mid_x1, mid_x2], [avg1, avg2], color='red', linewidth=2, marker='o', label=f'Avg Change: {label1} to {label2}')

# # Formatting the plot
plt.title('Counts Over Time by Specified Time Frames with Average Changes')
plt.xlabel('Date')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Time Frames', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid()
plt.show()









import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

df = pd.read_csv('results/data/final_category.csv', low_memory=False)

df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year
# df['Month'] = df['CreationDate'].dt.month

# output_dir = 'results/line_charts_step1-1'
os.makedirs(output_dir, exist_ok=True)

# unique_topics = df['topic_name'].unique()

for topic in tqdm(unique_topics):
#     filtered_df = df[df['topic_name'] == topic]

topic_questions_per_month = filtered_df.groupby(['Year', 'Month']).size()
#     topic_questions_per_month = topic_questions_per_month.reset_index(name='Count')
topic_questions_per_month['Date'] = pd.to_datetime(topic_questions_per_month[['Year', 'Month']].assign(DAY=1))
#     topic_questions_per_month = topic_questions_per_month.sort_values('Date')

plt.figure(figsize=(4, 1))
plt.plot(topic_questions_per_month['Date'], topic_questions_per_month['Count'], color='black')

plt.axis('off')
plt.gca().set_facecolor('none')
plt.gcf().set_facecolor('none')
plt.box(False)
plt.show()
safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
plt.savefig(f'{output_dir}/{safe_topic_name}_line_chart_step1-1.pdf', bbox_inches='tight', pad_inches=0, transparent = True)
plt.close()

import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

df = pd.read_csv('results/data/final_category.csv', low_memory=False)
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year

# output_dir = 'results/line_charts_step1'
os.makedirs(output_dir, exist_ok=True)

# unique_topics = df['topic_name'].unique()

for topic in tqdm(unique_topics):
#     filtered_df = df[df['topic_name'] == topic]

if filtered_df.empty:
logger.info(f"No data found for the topic_name: {topic}")
#         continue

total_questions_per_year = df.groupby('Year').size()
topic_questions_per_year = filtered_df.groupby('Year').size()
    
#     percentages_per_year = (topic_questions_per_year / total_questions_per_year).fillna(0) * 100

fig, ax1 = plt.subplots(figsize=(8, 4.5))

#     ax1.plot(topic_questions_per_year.index, topic_questions_per_year.values, marker='', linestyle='-', color='#003f5c', label='#')
#     ax1.tick_params(axis='y')

#     ax2 = ax1.twinx()
#     ax2.plot(percentages_per_year.index, percentages_per_year.values, marker='', linestyle='-', color='#ffa600', label='%')
#     ax2.tick_params(axis='y')

#     ax1.spines['top'].set_visible(False)
#     ax1.spines['bottom'].set_visible(False)
#     ax1.spines['right'].set_visible(False)
#     ax1.spines['left'].set_visible(False)

#     ax2.spines['top'].set_visible(False)
#     ax2.spines['bottom'].set_visible(False)
#     ax2.spines['right'].set_visible(False)
#     ax2.spines['left'].set_visible(False)

plt.grid(True)
plt.xticks([2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024])
    
safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
plt.tight_layout()
plt.savefig(f'{output_dir}/{safe_topic_name}_line_chart_step1.pdf')
plt.close(fig)

import pandas as pd
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

df = pd.read_csv('results/data/final_category.csv', low_memory=False)
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year

# output_dir = 'results/line_charts_step2'
os.makedirs(output_dir, exist_ok=True)

# unique_topics = df['middle_category'].unique()

for topic in tqdm(unique_topics):
#     filtered_df = df[df['middle_category'] == topic]

total_questions_per_year = df.groupby('Year').size()
topic_questions_per_year = filtered_df.groupby('Year').size()
    
#     percentages_per_year = (topic_questions_per_year / total_questions_per_year).fillna(0) * 100

fig, ax1 = plt.subplots(figsize=(8, 4.5))

#     ax1.plot(topic_questions_per_year.index, topic_questions_per_year.values, marker='', linestyle='-', color='#003f5c', label='#')
#     ax1.tick_params(axis='y')

#     ax2 = ax1.twinx()
#     ax2.plot(percentages_per_year.index, percentages_per_year.values, marker='', linestyle='-', color='#ffa600', label='%')
#     ax2.tick_params(axis='y')

#     ax1.spines['top'].set_visible(False)
#     ax1.spines['bottom'].set_visible(False)
#     ax1.spines['right'].set_visible(False)
#     ax1.spines['left'].set_visible(False)

#     ax2.spines['top'].set_visible(False)
#     ax2.spines['bottom'].set_visible(False)
#     ax2.spines['right'].set_visible(False)
#     ax2.spines['left'].set_visible(False)

plt.grid(True)
plt.xticks([2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024])
plt.show()
# safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
# plt.savefig(f'{output_dir}/{safe_topic_name}_line_chart_step2.pdf')
# plt.close(fig)

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    from tqdm import tqdm
    from matplotlib.ticker import FuncFormatter
    import os

    df = pd.read_csv('results/data/final_category.csv', low_memory=False)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
    df = df.dropna(subset=['CreationDate'])
    df['Year'] = df['CreationDate'].dt.year
    df['Month'] = df['CreationDate'].dt.month

    output_dir = 'results/line_charts_step3-3'
    os.makedirs(output_dir, exist_ok=True)

    unique_topics = df['category'].unique()

    for topic in tqdm(unique_topics):
        filtered_df = df[df['category'] == topic]

        total_questions_per_year = df.groupby('Year').size()
        topic_questions_per_year = filtered_df.groupby('Year').size()
        
        percentages_per_year = (topic_questions_per_year / total_questions_per_year).fillna(0) * 100

        fig, ax1 = plt.subplots(figsize=(8, 4.5))
        ax1.plot(topic_questions_per_year.index, topic_questions_per_year.values, marker='', linestyle='-', color='#003f5c', label='#')
        ax1.tick_params(axis='y', labelsize=15)

        ax2 = ax1.twinx()
        ax2.plot(percentages_per_year.index, percentages_per_year.values, marker='', linestyle='-', color='#ffa600', label='%')
        ax2.tick_params(axis='y', labelsize=15)

        ax1.set_xticks([2008, 2012, 2016, 2020, 2024])
        ax1.tick_params(axis='x', labelsize=15)
    # import pymannkendall as mk

        # mk_result_count = mk.original_test(topic_questions_per_month['Count'])
    # logger.info("Mann-Kendall Test for Count:")
    # logger.info("Trend: ", mk_result_count.trend)  # Increasing or Decreasing
    # logger.info("p-value: ", mk_result_count.p)  # p-value
    # logger.info("Z-value: ", mk_result_count.z)  # Z-value

        # mk_result_percentage = mk.original_test(merged_df['Percentage'])
    # logger.info(topic)
    # logger.info("\nMann-Kendall Test for Percentage:")
    # logger.info("Trend: ", mk_result_percentage.trend)  # Increasing or Decreasing
    # logger.info("p-value: ", mk_result_percentage.p)  # p-value
    # logger.info("Z-value: ", mk_result_percentage.z)  # Z-value

        # alpha = 0.05 
    # if mk_result_count.p < alpha:
    #     logger.info("The trend in Count is statistically significant.")
    # else:
    #     logger.info("The trend in Count is not statistically significant.")

    # if mk_result_percentage.p < alpha:
    #     logger.info("The trend in Percentage is statistically significant.")
    # else:
    #     logger.info("The trend in Percentage is not statistically significant.")


    # fig, ax1 = plt.subplots(figsize=(8, 4.5))

        # ax1.plot(topic_questions_per_month['Date'], topic_questions_per_month['Count'], marker='', linestyle='-', color='#003f5c', label='#')
        # ax1.tick_params(axis='y')

        # ax2 = ax1.twinx()
        # ax2.plot(merged_df['Date'], merged_df['Percentage'], marker='', linestyle='-', color='#ffa600', label='%')
        # ax2.tick_params(axis='y')

        ax1.spines['top'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_visible(False)

        ax2.spines['top'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        
        # Get y-axis vertical midpoints
        mid_y1 = (ax1.get_ylim()[0] + ax1.get_ylim()[1]) / 2
        mid_y2 = (ax2.get_ylim()[0] + ax2.get_ylim()[1]) / 2

        # Add '%' label on left, vertically centered
        ax1.text(ax1.get_xlim()[0] - 2.5, mid_y1, '%', color='#ffa600', fontsize=15,
                va='center', ha='center', rotation='vertical')

        # Add '#' label on right, vertically centered
        ax2.text(ax2.get_xlim()[1] + 2, mid_y2, '#', color='#003f5c', fontsize=15,
                va='center', ha='center', rotation='vertical')


        from matplotlib.ticker import MaxNLocator

        ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))  # 4 ticks max
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))  # 4 ticks max

    # plt.show()
        
    # safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
        plt.savefig(f'{output_dir}/{topic}_line_chart_step3-3-33333.pdf')
        plt.close(fig) 

if __name__ == '__main__':
    main()