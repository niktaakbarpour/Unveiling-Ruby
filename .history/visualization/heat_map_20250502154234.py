from utils.common import logger

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import pandas as pd
import numpy as np

# save_directory = 'heatmaps'
# figure_size = (9, 0.2)

# generate some random data for the heatmap:
random_data = {f"day{i}": np.random.randint(0, 11, size=5) for i in range(20)}
logger.info(random_data)
heatmap_df = pd.DataFrame(data = random_data, index = [f'topic{i}' for i in range(5)])
logger.info(heatmap_df)

# # A color map from complete white to an orange like color:
# # cmap = LinearSegmentedColormap.from_list('custom', [colors['white'], colors[2][1]])

# milestones = {'Coding Starts': 3, 'Mid-term Evaluation': 9}


# Iterating the heatmap_df to generate one heatmap for each topic
for topic in heatmap_df.index:
logger.info(topic)
# plt.figure(figsize=figure_size)
# ax = sns.heatmap((heatmap_df).loc[[topic]], annot=False, fmt=".1f", cmap=cmap, cbar=False, xticklabels=False, yticklabels=False)
    

#     # week_index = milestones['Coding Starts']
#     # rect = Rectangle((week_index, 0), 1, 1, fill=False, color=colors[4][2], lw=2)
#     # ax.add_patch(rect)

#     # week_index = milestones['Mid-term Evaluation'] 
#     # rect = Rectangle((week_index, 0), 1, 1, fill=False, color=colors[4][1], lw=2)
#     # ax.add_patch(rect)

#     # Set the path to save the heatmaps
# plt.savefig(f"{save_directory}/{topic}_heatmap.pdf", format='pdf', bbox_inches='tight', pad_inches=0)
# plt.show()
# plt.close()



import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import pandas as pd
import numpy as np
import os
df = pd.read_csv('results/data/final_category.csv', low_memory=False)
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year

# output_dir = 'results/heatmap_step1'
os.makedirs(output_dir, exist_ok=True)

# figure_size = (9, 0.2)

# cmap = LinearSegmentedColormap.from_list('custom', ['#ffffff', '#bc5090'])

pivot_table = df.pivot_table(index='topic_name', columns='Year', aggfunc='size', fill_value=0)

for topic in pivot_table.index:

plt.figure(figsize=figure_size)
ax = sns.heatmap((pivot_table).loc[[topic]], annot=False, fmt=".1f", cmap='Oranges', cbar=False, xticklabels=False, yticklabels=False)
plt.axis('off')

safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
plt.savefig(f'{output_dir}/{safe_topic_name}_heatmap_step1.pdf', bbox_inches='tight', pad_inches=0, transparent = True)
plt.close()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('results/data/final_category.csv', low_memory=False)
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year

pivot_table = df.pivot_table(index='topic_name', columns='Year', aggfunc='size', fill_value=0)
# pivot_table = pivot_table.sort_index()

plt.figure(figsize=(16, 12))
sns.heatmap(pivot_table, cmap='Oranges', annot=True, fmt='d', linewidths=.5)

plt.xlabel('Year')
plt.ylabel('Topic')

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig('heat_map.png')
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('results/data/final_category.csv', low_memory=False)
df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
df = df.dropna(subset=['CreationDate'])
# df['Year'] = df['CreationDate'].dt.year

pivot_table = df.pivot_table(index='middle_category', columns='Year', aggfunc='size', fill_value=0)
# pivot_table = pivot_table.sort_index()

plt.figure(figsize=(14, 9))
sns.heatmap(pivot_table, cmap='Oranges', annot=True, fmt='d', linewidths=.5, square=True)

plt.xlabel('Year')
plt.ylabel('Middle Category')

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig('heat_map_step2.png')
plt.show()


def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    df = pd.read_csv('results/data/final_category.csv', low_memory=False)

    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
    df = df.dropna(subset=['CreationDate'])
    df['Year'] = df['CreationDate'].dt.year

    pivot_table = df.pivot_table(index='category', columns='Year', aggfunc='size', fill_value=0)
    pivot_table = pivot_table.sort_index()

    fig, ax = plt.subplots(figsize=(14, 9))

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    heatmap = sns.heatmap(pivot_table, cmap='Oranges', annot=True, fmt='d', linewidths=.5, square=True, ax=ax, cbar_ax=cax)
    logger.info(pivot_table.sum())
    plt.xlabel('Year')
    plt.ylabel('Category')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()

    plt.savefig('heat_map_step3.png')
    plt.show()



if __name__ == '__main__':
    main()