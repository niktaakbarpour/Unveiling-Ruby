from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

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
# logger.info(col, count_1, count_2, count_3, count_4, count_5)
    
#     count_1_2 = count_1 + count_2
#     count_4_5 = count_4 + count_5
    
#     total = count_1_2 + count_3 + count_4_5
percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

#     norm_count_1 = (count_1 / max(count_1 + count_2 + count_3 + count_4 + count_5, 1)) * max_length
#     norm_count_2 = (count_2 / max(count_1 + count_2 + count_3 + count_4 + count_5, 1)) * max_length
#     norm_count_3 = (count_3 / max(count_1 + count_2 + count_3 + count_4 + count_5, 1)) * max_length
#     norm_count_4 = (count_4 / max(count_1 + count_2 + count_3 + count_4 + count_5, 1)) * max_length
#     norm_count_5 = (count_5 / max(count_1 + count_2 + count_3 + count_4 + count_5, 1)) * max_length
#     all = (count_1 + (count_2*2) + (count_3*3) + (count_4*4) + (count_5*5))/total
logger.info(all)

#     data.append({
#         'column': col,
#         'description': cleaned_descriptions[idx],
#         'norm_count_1': norm_count_1,
#         'norm_count_2': norm_count_2,
#         'norm_count_3': norm_count_3,
#         'norm_count_4': norm_count_4,
#         'norm_count_5': norm_count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

# sorted_data = sorted(data, key=lambda x: x['percent_4_5'], reverse=False)

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(14, 10))

for idx, item in enumerate(sorted_data):
#     norm_count_1 = item['norm_count_1']
#     norm_count_2 = item['norm_count_2']
#     norm_count_3 = item['norm_count_3']
#     norm_count_4 = item['norm_count_4']
#     norm_count_5 = item['norm_count_5']
    
#     total_norm_count = norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5


plt.barh(item['column'], norm_count_1, color=colors[0], label='1' if idx == 0 else "")
plt.barh(item['column'], norm_count_2, left=norm_count_1, color=colors[1], label='2' if idx == 0 else "")
plt.barh(item['column'], norm_count_3, left=norm_count_1 + norm_count_2, color=colors[18], label='3' if idx == 0 else "")
plt.barh(item['column'], norm_count_4, left=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='4' if idx == 0 else "")
plt.barh(item['column'], norm_count_5, left=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='5' if idx == 0 else "")

plt.text(-10, idx, f'{item["description"]}', va='center', ha='right', color='black', fontsize=8)
plt.text(norm_count_1 / 2, idx, f'{(norm_count_1 / total_norm_count) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 / 2, idx, f'{(norm_count_2 / total_norm_count) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 / 2, idx, f'{(norm_count_3 / total_norm_count) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 2, idx, f'{(norm_count_4 / total_norm_count) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 / 2, idx, f'{(norm_count_5 / total_norm_count) * 100:.1f}%', va='center', color='black', fontsize=8)

plt.text(-5, idx, f'{item["percent_1_2"]:.1f}%', va='center', ha='right', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 + 5, idx, f'{item["percent_4_5"]:.1f}%', va='center', ha='left', color='black', fontsize=8)

plt.xlim(0, max_length)
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.xlabel('')
# plt.title('Stacked Bar Chart for Q9_1 to Q9_35')
plt.legend()
plt.tight_layout()
plt.savefig('survey_part1_step1.pdf')
plt.show()



import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

columns = ['Q9_{}'.format(i) for i in range(1, 36)]
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

descriptions = df.iloc[0, 26:61].tolist()
cleaned_descriptions = [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions]

group_counts = {group: {str(i): 0 for i in range(1, 6)} for group in set(description_to_group.values())}
# group_percent_4_5 = {}

for idx, description in enumerate(cleaned_descriptions):
#     group = description_to_group.get(description, None)
    
if group:
#         col = columns[idx]
df[col] = pd.to_numeric(df[col], errors='coerce')
        
#         filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#         rating_counts = filtered_data.value_counts().sort_index()
        
for rating in range(1, 6):
#             group_counts[group][str(rating)] += rating_counts.get(rating, 0)

for group, counts in group_counts.items():
#     total = sum(counts.values())
if total > 0:
#         count_4_5 = counts['4'] + counts['5']
#         percent_4_5 = (count_4_5 / total) * 100
#         group_percent_4_5[group] = percent_4_5

# sorted_groups = sorted(group_percent_4_5.keys(), key=lambda x: group_percent_4_5[x], reverse=False)

# max_length = 100
cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]
plt.figure(figsize=(14, 10))

for idx, group in enumerate(sorted_groups):
#     counts = group_counts[group]
#     total = sum(counts.values())
    
if total == 0:
#         continue

#     count_1_2 = counts['1'] + counts['2']
#     count_4_5 = counts['4'] + counts['5']

percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0
    
#     norm_count_1 = (counts['1'] / total) * max_length
#     norm_count_2 = (counts['2'] / total) * max_length
#     norm_count_3 = (counts['3'] / total) * max_length
#     norm_count_4 = (counts['4'] / total) * max_length
#     norm_count_5 = (counts['5'] / total) * max_length
    
plt.barh(group, norm_count_1, color=colors[0], label='1' if idx == 0 else "")
plt.barh(group, norm_count_2, left=norm_count_1, color=colors[1], label='2' if idx == 0 else "")
plt.barh(group, norm_count_3, left=norm_count_1 + norm_count_2, color=colors[18], label='3' if idx == 0 else "")
plt.barh(group, norm_count_4, left=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='4' if idx == 0 else "")
plt.barh(group, norm_count_5, left=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='5' if idx == 0 else "")
    
plt.text(-10, idx, f'{group}', va='center', ha='right', color='black', fontsize=8)
plt.text(norm_count_1 / 2, idx, f'{(counts["1"] / total) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 / 2, idx, f'{(counts["2"] / total) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 / 2, idx, f'{(counts["3"] / total) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 2, idx, f'{(counts["4"] / total) * 100:.1f}%', va='center', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 / 2, idx, f'{(counts["5"] / total) * 100:.1f}%', va='center', color='black', fontsize=8)

plt.text(-5, idx, f'{percent_1_2:.1f}%', va='center', ha='right', color='black', fontsize=8)
plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 + 5, idx, f'{percent_4_5:.1f}%', va='center', ha='left', color='black', fontsize=8)

plt.xlim(0, max_length)
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.xlabel('')
# plt.title('Stacked Bar Chart for Grouped Descriptions (Sorted by 4-5 Ratings)')
plt.legend()
plt.tight_layout()
plt.savefig('survey_part1_step2.pdf')
plt.show()


def main():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

    columns = ['Q9_{}'.format(i) for i in range(1, 36)]
    description_to_group = {
        'Ruby Array and Hash Operations': 'Core Ruby Operations',
        'Regular Expressions in Ruby': 'Core Ruby Operations',
        'Algorithm Design in Ruby': 'Algorithm Design',
        'Advanced Ruby Methods and Metaprogramming': 'Advanced Ruby Concepts',
        'File Handling and External Integrations': 'Data Handling and Serialization',
        'Spreadsheet and CSV Management in Ruby': 'Data Handling and Serialization',
        'JSON and Data Serialization': 'Data Handling and Serialization',
        'ActiveRecord Associations in Rails': 'Database and ActiveRecord',
        'Database Management and Schema Design': 'Database and ActiveRecord',
        'Data Query and Manipulation in Rails': 'Database and ActiveRecord',
        'Ruby Gem Installation and Configuration Issues': 'Environment and Dependency Management',
        'Ruby Environment and Dependency Management': 'Environment and Dependency Management',
        'Automation with Chef': 'Deployment and Infrastructure Management',
        'Rails Deployment and Server Configuration': 'Deployment and Infrastructure Management',
        'Heroku Deployment and Configuration': 'Deployment and Infrastructure Management',
        'System Integration and External Libraries in Ruby': 'System Integration',
        'Job Scheduling and Background Processes': 'Background Processing',
        'Ruby on Rails Web Interface and UX Customization': 'Frontend Development in Rails',
        'Frontend Integration and User Interaction in Rails Applications': 'Frontend Development in Rails',
        'jQuery and AJAX in Rails': 'Frontend Development in Rails',
        'Email Delivery with Rails ActionMailer': 'External Services and API Integrations',
        'Asset Management and Integration Issues': 'External Services and API Integrations',
        'Search Engines Integration in Rails': 'External Services and API Integrations',
        'Ruby Payment and Financial Integration': 'External Services and API Integrations',
        'API Management': 'External Services and API Integrations',
        'Rails Routing and URLs': 'Routing and URLs',
        'Time Zone Management and Date Operations in Rails': 'Time and Date Management',
        'User Authentication and Role Management': 'User Authentication',
        'Rails Method and Parameter Errors': 'Error Handling and Validation',
        'Validation and Error Handling in Ruby on Rails': 'Error Handling and Validation',
        'Rails Mass Assignment & Parameter Protection Issues': 'Error Handling and Validation',
        'Ruby Debugging and Error Handling': 'Error Handling and Validation',
        'Automated Testing and Integration Testing in Ruby on Rails': 'Testing and Quality Assurance',
        'Rails Design Patterns': 'Software Design Patterns',
        'Performance Optimization in Rails': 'Performance Optimization'
    }

    group_to_category = {
        'Core Ruby Operations': 'Core Ruby Concepts',
        'Algorithm Design': 'Core Ruby Concepts',
        'Advanced Ruby Concepts': 'Core Ruby Concepts',
        'Data Handling and Serialization': 'Data Management and Processing',
        'Database and ActiveRecord': 'Data Management and Processing',
        'Environment and Dependency Management': 'Development Environment and Infrastructure',
        'Deployment and Infrastructure Management': 'Development Environment and Infrastructure',
        'System Integration': 'Development Environment and Infrastructure',
        'Background Processing': 'Development Environment and Infrastructure',
        'Frontend Development in Rails': 'Web Application Development',
        'External Services and API Integrations': 'Web Application Development',
        'Routing and URLs': 'Web Application Development',
        'Time and Date Management': 'Web Application Development',
        'User Authentication': 'Web Application Development',
        'Error Handling and Validation': 'Application Quality and Security',
        'Testing and Quality Assurance': 'Application Quality and Security',
        'Software Design Patterns': 'Software Architecture and Performance',
        'Performance Optimization': 'Software Architecture and Performance'
    }

    descriptions = df.iloc[0, 26:61].tolist()
    cleaned_descriptions = [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions]

    category_counts = {category: {str(i): 0 for i in range(1, 6)} for category in set(group_to_category.values())}

    for idx, description in enumerate(cleaned_descriptions):
        group = description_to_group.get(description, None)
        
        if group:
            category = group_to_category.get(group, None)
            if category:
                col = columns[idx] 
                df[col] = pd.to_numeric(df[col], errors='coerce') 
                
                filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
                
                rating_counts = filtered_data.value_counts().sort_index()
                
                for rating in range(1, 6):
                    category_counts[category][str(rating)] += rating_counts.get(rating, 0)

    category_percent_4_5 = {}

    for category, counts in category_counts.items():
        total = sum(counts.values())
        if total > 0:
            count_4_5 = counts['4'] + counts['5']
            percent_4_5 = (count_4_5 / total) * 100
            category_percent_4_5[category] = percent_4_5

    sorted_categories = sorted(category_percent_4_5.keys(), key=lambda x: category_percent_4_5[x], reverse=False)

    max_length = 100
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]
    plt.figure(figsize=(14, 3))

    for idx, category in enumerate(sorted_categories):
        counts = category_counts[category]
        total = sum(counts.values())
        
        if total == 0:
            continue

        count_1_2 = counts['1'] + counts['2']
        count_4_5 = counts['4'] + counts['5']

        percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
        percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

        norm_count_1 = (counts['1'] / total) * max_length
        norm_count_2 = (counts['2'] / total) * max_length
        norm_count_3 = (counts['3'] / total) * max_length
        norm_count_4 = (counts['4'] / total) * max_length
        norm_count_5 = (counts['5'] / total) * max_length

        logger.info(colors[0], colors[1], colors[18], colors[5], colors[4])
        
        plt.barh(category, norm_count_1, color=colors[0], label='1' if idx == 0 else "", height=0.8)
        plt.barh(category, norm_count_2, left=norm_count_1, color=colors[1], label='2' if idx == 0 else "", height=0.8)
        plt.barh(category, norm_count_3, left=norm_count_1 + norm_count_2, color=colors[18], label='3' if idx == 0 else "", height=0.8)
        plt.barh(category, norm_count_4, left=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='4' if idx == 0 else "", height=0.8)
        plt.barh(category, norm_count_5, left=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='5' if idx == 0 else "", height=0.8)
        
        words = category.split()
        logger.info(category)
        if category == "Development Environment and Infrastructure":
            display_category = "Dev. Env."
        elif category == "Software Architecture and Performance":
            display_category = "Arch."
        elif category == "Web Application Development":
            display_category = "App. Dev."
        elif category == "Application Quality and Security":
            display_category = "App. Quality"
        elif category == "Core Ruby Concepts":
            display_category = "Core"
        elif category == "Data Management and Processing":
            display_category = "Data"
        elif len(category) > 15:
            display_category = ' '.join(words[:2])
        else:
            display_category = category

        plt.text(-6.5, idx, f'{display_category}', va='center', ha='right', color='black', fontsize=15)
        plt.text(norm_count_1 / 2, idx, f'{(counts["1"] / total) * 100:.1f}%', va='center', color='black', fontsize=16)
        plt.text(norm_count_1 + norm_count_2 / 2, idx, f'{(counts["2"] / total) * 100:.1f}%', va='center', color='black', fontsize=16)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 / 2, idx, f'{(counts["3"] / total) * 100:.1f}%', va='center', color='black', fontsize=16)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 2, idx, f'{(counts["4"] / total) * 100:.1f}%', va='center', color='black', fontsize=16)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 / 2, idx, f'{(counts["5"] / total) * 100:.1f}%', va='center', color='black', fontsize=14)

        plt.text(-0.5, idx, f'{percent_1_2:.1f}%', va='center', ha='right', color='black', fontsize=14)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 + 0.5, idx, f'{percent_4_5:.1f}%', va='center', ha='left', color='black', fontsize=14)

    plt.xlim(0, max_length)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.xlabel('')
    plt.box(False)
    plt.subplots_adjust(left=0.3, right=0.85, top=0.9, bottom=0.1)
    plt.title('Stacked Bar Chart for Grouped Categories (Sorted by Satisfaction)')
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust
    plt.savefig('survey_part1_step333333333333.pdf')
    plt.show()

if __name__ == '__main__':
    main()