from utils.common import logger

import pandas as pd

# input_file = 'results/data/posts_using_arc_corrected_name_corrected_sheet.csv'
# output_file = 'results/data/count_of_each_topic.csv'

df = pd.read_csv(input_file)

# topic_counts = df['topic_name'].value_counts().reset_index()

# topic_counts.columns = ['topic_name', 'count']

# topic_counts.to_csv(output_file, index=False)

logger.info(f"Processed {len(df)} rows. Result saved to '{output_file}'")

import pandas as pd

# input_file = 'results/data/count_of_each_topic.csv' 
df = pd.read_csv(input_file)

# total_count = df['count'].sum()
# df['percentage'] = (df['count'] / total_count) * 100

# output_file = 'results/data/count_of_each_topic.csv' 
df.to_csv(output_file, index=False)

logger.info(f"Updated CSV file saved as {output_file}")

import pandas as pd

# input_file = 'results/data/count_of_each_topic.csv' 
df = pd.read_csv(input_file)

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
'Performance Optimization in Rails': 'Performance Optimization'
# }

# df['group'] = df['topic_name'].map(topic_to_group)

grouped_df = df.groupby('group', as_index=False).agg({
#     'count': 'sum'
# })

# total_count = grouped_df['count'].sum()

# grouped_df['percentage'] = (grouped_df['count'] / total_count) * 100

# output_file = 'results/data/count_of_each_topic_step2.csv'
grouped_df.to_csv(output_file, index=False)

logger.info(f"Grouped CSV file saved as {output_file}")


def main():
    import pandas as pd

    input_file = 'results/data/count_of_each_topic_step2.csv'
    df = pd.read_csv(input_file)

    topic_to_group = {
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
        'Performance Optimization': 'Software Architecture and Performance',
    }

    df['group'] = df['group'].map(topic_to_group)

    grouped_df = df.groupby('group', as_index=False).agg({
        'count': 'sum'
    })

    total_count = grouped_df['count'].sum()

    grouped_df['percentage'] = (grouped_df['count'] / total_count) * 100

    output_file = 'results/data/count_of_each_topic_step3.csv'
    grouped_df.to_csv(output_file, index=False)

    logger.info(f"Grouped CSV file saved as {output_file}")



if __name__ == '__main__':
    main()