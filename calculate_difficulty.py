# import pandas as pd

# input_file = 'results/data/final_category.csv'
# data = pd.read_csv(input_file)

# no_answer_percentage = data.groupby('category').apply(lambda x: (x['AnswerCount'] == 0).mean() * 100).reset_index(name='no_answer_percentage')

# output_file = 'results/data/no_answer_percentage_step3.csv' 
# no_answer_percentage.to_csv(output_file, index=False)

# print(f"The percentage of questions with no answers per topic has been saved to {output_file}")


# import pandas as pd

# input_file = 'results/data/final_category.csv'
# data = pd.read_csv(input_file)

# result = data.groupby('category').apply(
#     lambda x: (x['accepted_answer_id'].isna().sum() / len(x)) * 100
# ).reset_index(name='percentage_without_acc_answer')

# output_file = 'results/data/no_accepted_answers_step3_2.csv' 
# result.to_csv(output_file, index=False)

# print(f"The percentage of questions with no answers per topic has been saved to {output_file}")


import pandas as pd

def calculate_median_response_time(data):
    data['CreationDate'] = pd.to_datetime(data['CreationDate'], errors='coerce')
    data['accepted_answer_creation_date'] = pd.to_datetime(data['accepted_answer_creation_date'], errors='coerce')
    data['response_time'] = (data['accepted_answer_creation_date'] - data['CreationDate']).dt.total_seconds() / 60
    response_times = data.dropna(subset=['accepted_answer_creation_date'])
    median_response_time = response_times.groupby('category')['response_time'].mean().reset_index()
    return median_response_time

input_file = 'results/data/final_category.csv'
data = pd.read_csv(input_file)
median_response_time = calculate_median_response_time(data)
output_file = 'results/data/median_response_time_step3.csv'
median_response_time.to_csv(output_file, index=False)

print(f"The median response time per topic has been saved to {output_file}")


# import pandas as pd

# input_file = 'results/data/final_dataset_standardized_dates.csv'
# df = pd.read_csv(input_file)
# df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce')
# cutoff_date = pd.to_datetime('2022-11-30')
# filtered_df = df[df['CreationDate'] <= cutoff_date]

# result1 = df.groupby('topic_name').apply(
#     lambda x: (x['accepted_answer_id'].isna().sum() / len(x)) * 100
# ).reset_index(name='percentage_without_acc_answer')

# result2 = filtered_df.groupby('topic_name').apply(
#     lambda x: (x['accepted_answer_id'].isna().sum() / len(x)) * 100
# ).reset_index(name='percentage_without_acc_answer_filtered')

# output_file = 'results/data/difficulty_test1.csv' 
# result1.to_csv(output_file, index=False)
# output_file = 'results/data/difficulty_test2.csv' 
# result2.to_csv(output_file, index=False)

# print(f"The percentage of questions with no answers per topic has been saved to {output_file}")




# import pandas as pd

# input_file = 'results/data/final_dataset_standardized_dates.csv'
# data = pd.read_csv(input_file)

# topic_to_group = {
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
#     'Performance Optimization in Rails': 'Performance Optimization'
# }

# data['group'] = data['topic_name'].map(topic_to_group)

# grouped_data = data.groupby('group').agg(
#     total_questions=pd.NamedAgg(column='accepted_answer_id', aggfunc='count'),
#     no_accepted_answers=pd.NamedAgg(column='accepted_answer_id', aggfunc=lambda x: x.isna().sum())
# ).reset_index()

# grouped_data['percentage_no_accepted_answers'] = (grouped_data['no_accepted_answers'] / grouped_data['total_questions']) * 100

# output_file = 'results/data/no_accepted_answers_step2.csv'
# grouped_data.to_csv(output_file, index=False)

# print(f"The percentage of questions without an accepted answer per combined topic has been saved to {output_file}")

# import pandas as pd

# input_file = 'results/data/no_accepted_answers_step2.csv'
# data = pd.read_csv(input_file)

# topic_to_group = {
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
#     'Software Design Patterns': 'Software Architecture and Performance',
#     'Performance Optimization': 'Software Architecture and Performance',
# }

# data['topic_name'] = data['topic_name'].map(topic_to_group)

# grouped_data = data.groupby('topic_name')['without_accepted_answer'].mean().reset_index()

# output_file = 'results/data/no_accepted_answers_step3.csv'
# grouped_data.to_csv(output_file, index=False)

# print(f"The percentage of questions without an accepted answer per combined topic has been saved to {output_file}")
