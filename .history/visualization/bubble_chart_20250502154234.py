from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

csv1 = pd.read_csv('results/data/average_view_step1.csv')
csv2 = pd.read_csv('results/data/no_accepted_answers_step1.csv')
csv3 = pd.read_csv('results/data/count_of_each_topic_step1.csv')

merged_df = pd.merge(csv1[['topic_name', 'view_count']], csv2[['topic_name', 'without_accepted_answer']], on='topic_name')
merged_df = pd.merge(merged_df, csv3[['topic_name', 'count']], on='topic_name')

# bubble_size = (merged_df['count'] / merged_df['count'].max()) * 8000  

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')
columns = ['Q9_{}'.format(i) for i in range(1, 36)]

descriptions = df.iloc[0, 26:61].tolist()
cleaned_descriptions = [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions]
df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# percent_4_5_dict = {}
for idx, col in enumerate(columns):
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
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0
#     percent_4_5_dict[cleaned_descriptions[idx]] = percent_4_5

# merged_df['percent_4_5'] = merged_df['topic_name'].map(percent_4_5_dict)

# norm = Normalize(vmin=23.5, vmax=46.9)
# cmap = get_cmap('Spectral')

plt.figure(figsize=(14, 10))
scatter = plt.scatter(merged_df['without_accepted_answer'], merged_df['view_count'],
#                       s=bubble_size, c=merged_df['percent_4_5'], cmap=cmap, norm=norm, alpha=0.7, edgecolors="w", linewidth=0.5)

cbar = plt.colorbar(scatter, ax=plt.gca(), pad=0.07)
# cbar.set_label('Survey Responses (%)')

# avg_view_count = merged_df['view_count'].mean()
# avg_without_accepted_answer = merged_df['without_accepted_answer'].mean()
plt.axhline(y=avg_view_count, color='red', linestyle='--', linewidth=1)
plt.axvline(x=avg_without_accepted_answer, color='red', linestyle='--', linewidth=1)

xlim = plt.xlim()
ylim = plt.ylim()
plt.text(xlim[1] + (xlim[1] - xlim[0]) * 0.01, avg_view_count, 'Average', color='red',
#          verticalalignment='center', horizontalalignment='left', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))
plt.text(avg_without_accepted_answer, ylim[1] + (ylim[1] - ylim[0]) * 0.01, 'Average', color='red',
#          verticalalignment='bottom', horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))

plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel('Difficulty')
plt.ylabel('Popularity')

plt.show()

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import Normalize
    from matplotlib.cm import get_cmap
    from matplotlib.colors import LinearSegmentedColormap
    import seaborn as sns

    csv1 = pd.read_csv('results/data/average_view_step3.csv')
    csv2 = pd.read_csv('results/data/no_accepted_answers_step3.csv')
    csv3 = pd.read_csv('results/data/count_of_each_topic_step3.csv')

    merged_df = pd.merge(csv1[['category', 'view_count']], csv2[['category', 'without_accepted_answer']], on='category')
    merged_df = pd.merge(merged_df, csv3[['category', 'count']], on='category')

    bubble_size = (merged_df['count'] / merged_df['count'].max()) * 8000  

    cmap = get_cmap('RdYlGn')
    colors = cmap(np.linspace(0.2, 1, 256))
    custom_cmap = LinearSegmentedColormap.from_list('custom_oranges', colors)

    cmap2 = plt.get_cmap('tab20c')
    colors2 = [cmap2(i / 20) for i in range(20)]

    plt.figure(figsize=(10, 5.5))

    sns.regplot(x='view_count', y='without_accepted_answer', data=merged_df, scatter=False, color=colors2[0], ci=None)

    scatter = plt.scatter(merged_df['without_accepted_answer'], merged_df['view_count'], 
                          s=bubble_size, c=bubble_size, cmap=custom_cmap, alpha=0.8, edgecolors="w", linewidth=0.5)
    plt.tick_params(axis='both', labelsize=14)

    from scipy.stats import pearsonr

    # average_popularity = merged_df['without_accepted_answer']
    average_difficulty = merged_df['view_count']

    correlation_coefficient, p_value = pearsonr(average_popularity, average_difficulty)

    logger.info("Pearson Correlation Coefficient:", correlation_coefficient)
    logger.info("P-value:", p_value)

    from scipy.stats import shapiro

    stat_so, p_so = shapiro(merged_df['view_count'])
    stat_survey, p_survey = shapiro(merged_df['without_accepted_answer'])

    logger.info(f"Shapiro-Wilk Test for SO Data: Statistic = {stat_so}, p-value = {p_so}")
    logger.info(f"Shapiro-Wilk Test for Survey Data: Statistic = {stat_survey}, p-value = {p_survey}")

    alpha = 0.05

    if p_so > alpha:
        logger.info("SO data average looks normally distributed.")
    else:
        logger.info("SO data average does not look normally distributed.")

    if p_survey > alpha:
        logger.info("Survey data average looks normally distributed.")
    else:
        logger.info("Survey data average does not look normally distributed.")

    from scipy.stats import kendalltau

    Assuming average_popularity and average_difficulty are defined as before
    average_popularity = merged_df['without_accepted_answer']
    average_difficulty = merged_df['view_count']

    # Calculate Kendall correlation coefficient and p-value
    kendall_coefficient, kendall_p_value = kendalltau(average_popularity, average_difficulty)

    # Output the results
    logger.info("Kendall Correlation Coefficient:", kendall_coefficient)
    logger.info("P-value:", kendall_p_value)


    avg_view_count = merged_df['view_count'].mean()
    avg_without_accepted_answer = merged_df['without_accepted_answer'].mean()
    plt.axhline(y=avg_view_count, color='#003f5c', linestyle='--', linewidth=1)
    plt.axvline(x=avg_without_accepted_answer, color='#003f5c', linestyle='--', linewidth=1)

    cbar = plt.colorbar(scatter, ax=plt.gca(), pad=0.05)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label(label='Questions in Each Category (#)', fontsize=14)

    for i, row in merged_df.iterrows():
        if row['category'] == 'Core Ruby Concepts':
            plt.annotate(
            "Core Ruby Concepts",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(50,-40),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )
        elif row['category'] == 'Application Quality and Security':
            plt.annotate(
            "App. Quality and Security",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(50,60),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )
        elif row['category'] == 'Data Management and Processing':
            plt.annotate(
            "Data Management and Processing",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(-70,70),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )
        elif row['category'] == 'Development Environment and Infrastructure':
            plt.annotate(
            "Development Environment",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(-100,70),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )
        elif row['category'] == 'Software Architecture and Performance':
            plt.annotate(
            "Software Architecture and Performance",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(-130,10),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )
        else:
            plt.annotate(
            "Web App. Development",
            (row['without_accepted_answer'], row['view_count']),
            textcoords="offset points",
            xytext=(-20,-50),
            ha='center',
            fontsize=14,
            color='black',
            bbox=dict(facecolor='#e3c3bc', edgecolor='none', pad=1),
            arrowprops=dict(arrowstyle='-', color='gray', lw=1) 
        )

    xlim = plt.xlim()
    ylim = plt.ylim()
    plt.text(xlim[1] + (xlim[1] - xlim[0]) * 0.01, avg_view_count, 'Avg.', color='#003f5c', 
             verticalalignment='center', horizontalalignment='left', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))
    plt.text(avg_without_accepted_answer, ylim[1] + (ylim[1] - ylim[0]) * 0.01, 'Avg.', color='#003f5c', 
             verticalalignment='bottom', horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))

    plt.xlabel(xlabel='Difficulty (%)', fontsize=14)
    plt.ylabel(ylabel='Popularity (#)', fontsize=14)
    plt.savefig('final_bubble_chart_step33.pdf')
    plt.show()



    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import Normalize
    from matplotlib.cm import get_cmap

    csv1 = pd.read_csv('results/data/average_view_step2.csv')
    csv2 = pd.read_csv('results/data/no_accepted_answers_step2.csv')
    csv3 = pd.read_csv('results/data/count_of_each_topic_step2.csv')
    survey_data = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

    merged_df = pd.merge(csv1[['middle_category', 'view_count']], csv2[['middle_category', 'without_accepted_answer']], on='middle_category')
    merged_df = pd.merge(merged_df, csv3[['middle_category', 'count']], on='middle_category')

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

    columns = ['Q9_{}'.format(i) for i in range(1, 36)]

    # descriptions = survey_data.iloc[0, 26:61].tolist()
    cleaned_descriptions = [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions]

    group_counts = {group: {str(i): 0 for i in range(1, 6)} for group in set(description_to_group.values())}

    for idx, description in enumerate(cleaned_descriptions):
    #     group = description_to_group.get(description, None)
    if group:
    #         col = columns[idx]
    survey_data[col] = pd.to_numeric(survey_data[col], errors='coerce')
    #         filtered_data = survey_data[col][(survey_data[col] >= 1) & (survey_data[col] <= 5)]
    #         rating_counts = filtered_data.value_counts().sort_index()

    for rating in range(1, 6):
    #             group_counts[group][str(rating)] += rating_counts.get(rating, 0)

    # percent_4_5 = {}
    for group, counts in group_counts.items():
    #     total = sum(counts.values())
    if total > 0:
    #         percent_4_5[group] = ((counts['4'] + counts['5']) / total) * 100
    else:
    #         percent_4_5[group] = 0

    # cmap = get_cmap('Spectral')
    # norm = Normalize(vmin=23.7, vmax=46.9)
    # merged_df['color'] = merged_df['middle_category'].map(percent_4_5)

    # bubble_size = (merged_df['count'] / merged_df['count'].max()) * 8000  

    # avg_view_count = merged_df['view_count'].mean()
    # avg_without_accepted_answer = merged_df['without_accepted_answer'].mean()

    plt.figure(figsize=(14, 10))
    scatter = plt.scatter(merged_df['without_accepted_answer'], merged_df['view_count'],
    #             s=bubble_size, alpha=0.5, c=merged_df['color'], cmap=cmap, norm=norm, edgecolors="w", linewidth=0.5)

    cbar = plt.colorbar(scatter, ax=plt.gca(), pad=0.07)
    # cbar.set_label('Survey Responses (%)')


    plt.axhline(y=avg_view_count, color='red', linestyle='--', linewidth=1, label='Avg. popularity')
    plt.axvline(x=avg_without_accepted_answer, color='red', linestyle='--', linewidth=1, label='Avg. difficulty')

    xlim = plt.xlim()
    ylim = plt.ylim()

    plt.text(xlim[1] + (xlim[1] - xlim[0]) * 0.01, avg_view_count, 'Average', color='red',
    #          verticalalignment='center', horizontalalignment='left', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))
    plt.text(avg_without_accepted_answer, ylim[1] + (ylim[1] - ylim[0]) * 0.01, 'Average', color='red',
    #          verticalalignment='bottom', horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('Difficulty')
    plt.ylabel('Popularity')
    plt.show()



    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import Normalize
    from matplotlib.cm import get_cmap

    csv1 = pd.read_csv('results/data/average_view_step3.csv')
    csv2 = pd.read_csv('results/data/no_accepted_answers_step3.csv')
    csv3 = pd.read_csv('results/data/count_of_each_topic_step3.csv')
    survey_data = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

    merged_df = pd.merge(csv1[['category', 'view_count']], csv2[['category', 'without_accepted_answer']], on='category')
    merged_df = pd.merge(merged_df, csv3[['category', 'count']], on='category')

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

    # group_to_category = {
    #     'Core Ruby Operations': 'Core Ruby Concepts',
    #     'Algorithm Design': 'Core Ruby Concepts',
    #     'Advanced Ruby Concepts': 'Core Ruby Concepts',
    #     'Data Handling and Serialization': 'Data Management and Processing',
    #     'Database and ActiveRecord': 'Data Management and Processing',
    #     'Environment and Dependency Management': 'Development Environment and Infrastructure',
    #     'Deployment and Infrastructure Management': 'Development Environment and Infrastructure',
    #     'System Integration': 'Development Environment and Infrastructure',
    #     'Background Processing': 'Development Environment and Infrastructure',
    #     'Frontend Development in Rails': 'Web Application Development',
    #     'External Services and API Integrations': 'Web Application Development',
    #     'Routing and URLs': 'Web Application Development',
    #     'Time and Date Management': 'Web Application Development',
    #     'User Authentication': 'Web Application Development',
    #     'Error Handling and Validation': 'Application Quality and Security',
    #     'Testing and Quality Assurance': 'Application Quality and Security',
    'Software Design Patterns': 'Software Architecture and Performance',
    'Performance Optimization': 'Software Architecture and Performance'
    # }

    columns = ['Q9_{}'.format(i) for i in range(1, 36)]

    # descriptions = survey_data.iloc[0, 26:61].tolist()
    cleaned_descriptions = [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions]

    category_counts = {category: {str(i): 0 for i in range(1, 6)} for category in set(group_to_category.values())}

    for idx, description in enumerate(cleaned_descriptions):
    #     group = description_to_group.get(description, None)
    if group:
    #         category = group_to_category.get(group, None)
    if category:
    #             col = columns[idx]
    survey_data[col] = pd.to_numeric(survey_data[col], errors='coerce')
    #             filtered_data = survey_data[col][(survey_data[col] >= 1) & (survey_data[col] <= 5)]
    #             rating_counts = filtered_data.value_counts().sort_index()

    for rating in range(1, 6):
    #             category_counts[category][str(rating)] += rating_counts.get(rating, 0)

    # percent_4_5 = {}
    for category, counts in category_counts.items():
    #     total = sum(counts.values())
    if total > 0:
    #         percent_4_5[category] = ((counts['4'] + counts['5']) / total) * 100
    else:
    #         percent_4_5[category] = 0

    # cmap = get_cmap('Spectral')
    # norm = Normalize(vmin=26.5, vmax=31.6)
    # merged_df['color'] = merged_df['category'].map(percent_4_5)

    # bubble_size = (merged_df['count'] / merged_df['count'].max()) * 8000  

    # avg_view_count = merged_df['view_count'].mean()
    # avg_without_accepted_answer = merged_df['without_accepted_answer'].mean()

    plt.figure(figsize=(14, 10))
    scatter = plt.scatter(merged_df['without_accepted_answer'], merged_df['view_count'],
    #             s=bubble_size, alpha=0.5, c=merged_df['color'], cmap=cmap, norm=norm, edgecolors="w", linewidth=0.5)

    cbar = plt.colorbar(scatter, ax=plt.gca(), pad=0.07)
    # cbar.set_label('Survey Responses (%)')


    plt.axhline(y=avg_view_count, color='red', linestyle='--', linewidth=1, label='Avg. popularity')
    plt.axvline(x=avg_without_accepted_answer, color='red', linestyle='--', linewidth=1, label='Avg. difficulty')

    xlim = plt.xlim()
    ylim = plt.ylim()

    plt.text(xlim[1] + (xlim[1] - xlim[0]) * 0.01, avg_view_count, 'Average', color='red',
    #          verticalalignment='center', horizontalalignment='left', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))
    plt.text(avg_without_accepted_answer, ylim[1] + (ylim[1] - ylim[0]) * 0.01, 'Average', color='red',
    #          verticalalignment='bottom', horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', pad=2))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('Difficulty')
    plt.ylabel('Popularity')
    plt.show()

if __name__ == '__main__':
    main()