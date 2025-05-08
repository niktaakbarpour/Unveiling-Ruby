from utils.common import logger

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

# sentence_to_number = {
#     'less than 15 minutes': 1,
#     'between 15 to 30 minutes': 2,
#     'between 30 to 60 minutes': 3,
#     'between 1 and 2 hours': 4,
#     'more than 2 hours': 5
# }

columns = ['Q12_{}'.format(i) for i in range(1, 36)]
descriptions = df.iloc[0, 72:107].tolist()

# cleaned_descriptions = []
for desc in descriptions:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions.append('')

# data = []

for idx, col in tqdm(enumerate(columns), total=len(columns)):
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

#     data.append({
#         'column': col,
#         'description': cleaned_descriptions[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

# sorted_data = sorted(data, key=lambda x: x['percent_4_5'], reverse=False)

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(18, 14))

for idx, item in enumerate(sorted_data):
#     norm_count_1 = item['norm_count_1']
#     norm_count_2 = item['norm_count_2']
#     norm_count_3 = item['norm_count_3']
#     norm_count_4 = item['norm_count_4']
#     norm_count_5 = item['norm_count_5']
    
#     total_norm_count = norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5

plt.bar(item['column'], norm_count_1, color=colors[0], label='less than 15 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_2, bottom=norm_count_1, color=colors[1], label='between 15 to 30 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_3, bottom=norm_count_1 + norm_count_2, color=colors[18], label='between 30 to 60 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_4, bottom=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='between 1 and 2 hours' if idx == 0 else "")
plt.bar(item['column'], norm_count_5, bottom=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='more than 2 hours' if idx == 0 else "")

plt.text(idx, norm_count_1 / 2, f'{(norm_count_1 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 / 2, f'{(norm_count_2 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 / 2, f'{(norm_count_3 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 2, f'{(norm_count_4 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 / 2, f'{(norm_count_5 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)

plt.text(idx, -1, item['description'], va='top', ha='center', rotation=90, fontsize=7)

plt.subplots_adjust(bottom=0.3)

plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.xlabel('')
plt.legend()
plt.tight_layout()
plt.savefig('survey_part2_step1.pdf')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
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

columns = ['Q12_{}'.format(i) for i in range(1, 36)]
descriptions = df.iloc[0, 72:107].tolist()

# cleaned_descriptions = []
for desc in descriptions:
if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions.append(desc.split('-')[-1].strip())
else:
#         cleaned_descriptions.append('')

group_counts = {group: {str(i): 0 for i in range(1, 6)} for group in set(description_to_group.values())}
# logger.info(group_counts)
# data = []


for idx, description in enumerate(cleaned_descriptions):
#     group = description_to_group.get(description, None)
logger.info(group)
if group:
#         col = columns[idx]
#         mapped_col = df[col].map(sentence_to_number)
#         filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
#         rating_counts = filtered_data.value_counts().sort_index()
        
for rating in range(1, 6):
#             group_counts[group][str(rating)] += rating_counts.get(rating, 0)
            

for group, counts in group_counts.items():
#     total = sum(counts.values())

for idx, group in tqdm(enumerate(group_counts.keys()), total=len(group_counts.keys())):
#     counts = group_counts[group]
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

#     data.append({
#         'column': group,
#         'description': cleaned_descriptions[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'percent_1_2': percent_1_2,
#         'percent_4_5': percent_4_5
#     })

# sorted_data = sorted(data, key=lambda x: x['percent_4_5'], reverse=False)

cmap = plt.get_cmap('tab20c')
colors = [cmap(i / 20) for i in range(20)]

plt.figure(figsize=(18, 14))

for idx, item in enumerate(sorted_data):
#     norm_count_1 = item['norm_count_1']
#     norm_count_2 = item['norm_count_2']
#     norm_count_3 = item['norm_count_3']
#     norm_count_4 = item['norm_count_4']
#     norm_count_5 = item['norm_count_5']
    
#     total_norm_count = norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5

plt.bar(item['column'], norm_count_1, color=colors[0], label='less than 15 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_2, bottom=norm_count_1, color=colors[1], label='between 15 to 30 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_3, bottom=norm_count_1 + norm_count_2, color=colors[18], label='between 30 to 60 minutes' if idx == 0 else "")
plt.bar(item['column'], norm_count_4, bottom=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='between 1 and 2 hours' if idx == 0 else "")
plt.bar(item['column'], norm_count_5, bottom=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='more than 2 hours' if idx == 0 else "")

plt.text(idx, norm_count_1 / 2, f'{(norm_count_1 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 / 2, f'{(norm_count_2 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 / 2, f'{(norm_count_3 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 2, f'{(norm_count_4 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)
plt.text(idx, norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 / 2, f'{(norm_count_5 / total_norm_count) * 100:.1f}%', ha='center', color='black', fontsize=8)

plt.text(idx, -1, item['column'], va='top', ha='center', rotation=90, fontsize=7)

plt.subplots_adjust(bottom=0.3)

plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)
plt.xlabel('')
plt.legend()
plt.tight_layout()
plt.savefig('survey_part2_step2.pdf')
plt.show()

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    from tqdm import tqdm

    df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

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

    sentence_to_number = {
        'less than 15 minutes': 1,
        'between 15 to 30 minutes': 2,
        'between 30 to 60 minutes': 3,
        'between 1 and 2 hours': 4,
        'more than 2 hours': 5
    }

    columns = ['Q12_{}'.format(i) for i in range(1, 36)]
    descriptions = df.iloc[0, 72:107].tolist()

    category_counts = {category: {str(i): 0 for i in range(1, 6)} for category in set(group_to_category.values())}

    cleaned_descriptions = []
    for desc in descriptions:
        if isinstance(desc, str) and '-' in desc:
            cleaned_descriptions.append(desc.split('-')[-1].strip())
        else:
            cleaned_descriptions.append('')

    data = []

    for idx, description in enumerate(cleaned_descriptions):
        group = description_to_group.get(description, None)
        
        if group:
            category = group_to_category.get(group, None)
            if category:
                col = columns[idx]
                mapped_col = df[col].map(sentence_to_number) 
                
                filtered_data = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
                
                rating_counts = filtered_data.value_counts().sort_index()
                
                for rating in range(1, 6):
                    category_counts[category][str(rating)] += rating_counts.get(rating, 0)

    logger.info(category_counts)

    for group, counts in category_counts.items():
        total = sum(counts.values())

    max_length = 100

    for idx, group in tqdm(enumerate(category_counts.keys()), total=len(category_counts.keys())):
        counts = category_counts[group]
        total = sum(counts.values())

        count_1 = counts['1']
        count_2 = counts['2']
        count_3 = counts['3']
        count_4 = counts['4']
        count_5 = counts['5']
        
        count_1_2 = count_1 + count_2
        count_4_5 = count_4 + count_5
        
        total = count_1_2 + count_3 + count_4_5
        percent_1_2 = (count_1_2 / total) * 100 if total != 0 else 0
        percent_4_5 = (count_4_5 / total) * 100 if total != 0 else 0

        norm_count_1 = (counts['1'] / total) * max_length
        norm_count_2 = (counts['2'] / total) * max_length
        norm_count_3 = (counts['3'] / total) * max_length
        norm_count_4 = (counts['4'] / total) * max_length
        norm_count_5 = (counts['5'] / total) * max_length
        norm_percent_1_2 = norm_count_1 + norm_count_2
        norm_percent_4_5 = norm_count_4 + norm_count_5

    # logger.info(group, norm_percent_1_2, norm_percent_4_5)


        data.append({
            'column': group,
            'description': cleaned_descriptions[idx],
            'norm_count_1': norm_count_1,
            'norm_count_2': norm_count_2,
            'norm_count_3': norm_count_3,
            'norm_count_4': norm_count_4,
            'norm_count_5': norm_count_5,
            'percent_1_2': norm_percent_1_2,
            'percent_4_5': norm_percent_4_5
        })

    sorted_data = sorted(data, key=lambda x: x['percent_4_5'], reverse=False)

    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]

    plt.figure(figsize=(12, 3))

    for idx, item in enumerate(sorted_data):
        norm_count_1 = item['norm_count_1']
        norm_count_2 = item['norm_count_2']
        norm_count_3 = item['norm_count_3']
        norm_count_4 = item['norm_count_4']
        norm_count_5 = item['norm_count_5']
        norm_percent_4_5 = item['percent_4_5']
        norm_percent_1_2 = item['percent_1_2']
        
        total_norm_count = norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5

        plt.barh(item['column'], norm_count_1, color=colors[0], label='less than 15 minutes' if idx == 0 else "")
        plt.barh(item['column'], norm_count_2, left=norm_count_1, color=colors[1], label='between 15 to 30 minutes' if idx == 0 else "")
        plt.barh(item['column'], norm_count_3, left=norm_count_1 + norm_count_2, color=colors[18], label='between 30 to 60 minutes' if idx == 0 else "")
        plt.barh(item['column'], norm_count_4, left=norm_count_1 + norm_count_2 + norm_count_3, color=colors[5], label='between 1 and 2 hours' if idx == 0 else "")
        plt.barh(item['column'], norm_count_5, left=norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4, color=colors[4], label='more than 2 hours' if idx == 0 else "")

    # label_fontsize = 12 if idx < len(sorted_data) - 1 else 8
        label_fontsize = 16


        plt.text(norm_count_1 / 1.2, idx-0.2, f'{(norm_count_1 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 / 2, idx-0.2, f'{(norm_count_2 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 / 2, idx-0.2, f'{(norm_count_3 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 / 1.6, idx-0.2, f'{(norm_count_4 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5, idx-0.2, f'{(norm_count_5 / total_norm_count) * 100:.1f}%', ha='right', color='black', fontsize=label_fontsize)

        plt.text(0, idx, f'{norm_percent_1_2:.1f}%', va='center', ha='right', color='black', fontsize=15)
        plt.text(norm_count_1 + norm_count_2 + norm_count_3 + norm_count_4 + norm_count_5 + 0.5, idx, f'{norm_percent_4_5:.1f}%', va='center', ha='left', color='black', fontsize=16)

        words = item['column'].split()
    # if len(item['column']) > 18:
        #     display_category = ' '.join(words[:2])
    # else:
        #     display_category = item['column']

        #     words = category.split()

        category = item['column']
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

        plt.text(-7.5, idx, f'{display_category}', va='center', ha='right', rotation=0, fontsize=16)


    plt.subplots_adjust(bottom=0.3)
    plt.xlim(0, max_length)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.xlabel('')
    plt.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95), fontsize=11)
    plt.box(False)
    plt.tight_layout()
    plt.savefig('normalized_bar_chart_step333333333333333333.pdf')
    plt.show()

if __name__ == '__main__':
    main()