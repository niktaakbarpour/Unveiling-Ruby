import pandas as pd
import os

# ========== MAPPINGS ==========
TOPIC_NUMBER_MAPPING = {
    "Rails Mass Assignment & Parameter Protection Issues": 0,
    "Ruby on Rails Web Interface and UX Customization": 1,
    "Rails Method and Parameter Errors": 2,
    "jQuery and AJAX in Rails": 3,
    "Advanced Ruby Methods and Metaprogramming": 4,
    "Data Query and Manipulation in Rails": 5,
    "API Management": 6,
    "Ruby Array and Hash Operations": 7,
    "System Integration and External Libraries in Ruby": 8,
    "Ruby Debugging and Error Handling": 9,
    "Frontend Integration and User Interaction in Rails Applications": 10,
    "Ruby Gem Installation and Configuration Issues": 11,
    "User Authentication and Role Management": 12,
    "Algorithm Design in Ruby": 13,
    "Rails Routing and URLs": 14,
    "Ruby Environment and Dependency Management": 15,
    "JSON and Data Serialization": 16,
    "Validation and Error Handling in Ruby on Rails": 17,
    "File Handling and External Integrations": 18,
    "Asset Management and Integration Issues": 19,
    "Automated Testing and Integration Testing in Ruby on Rails": 20,
    "ActiveRecord Associations in Rails": 21,
    "Database Management and Schema Design": 22,
    "Rails Design Patterns": 23,
    "Heroku Deployment and Configuration": 24,
    "Rails Deployment and Server Configuration": 25,
    "Job Scheduling and Background Processes": 26,
    "Spreadsheet and CSV Management in Ruby": 27,
    "Email Delivery with Rails ActionMailer": 28,
    "Regular Expressions in Ruby": 29,
    "Performance Optimization in Rails": 30,
    "Time Zone Management and Date Operations in Rails": 31,
    "Search Engines Integration in Rails": 32,
    "Ruby Payment and Financial Integration": 33,
    "Automation with Chef in DevOps": 34
}

MIDDLE_CATEGORY_MAPPING = {
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

FINAL_CATEGORY_MAPPING = {
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


# ========== FUNCTIONS ==========
def apply_topic_number_mapping(input_file, output_file):
    df = pd.read_csv(input_file)
    df['topic'] = df['topic_name'].map(TOPIC_NUMBER_MAPPING)
    df_sorted = df.sort_values(by='topic')
    df_sorted.to_csv(output_file, index=False)
    print(f"Saved topic numbers to {output_file}")


def apply_middle_category_mapping(input_file, output_file):
    df = pd.read_csv(input_file)
    df['middle_category'] = df['topic_name'].map(MIDDLE_CATEGORY_MAPPING)
    df_sorted = df.sort_values(by='middle_category')
    df_sorted.to_csv(output_file, index=False)
    print(f"Saved middle categories to {output_file}")


def apply_final_category_mapping(input_file, output_file):
    df = pd.read_csv(input_file)
    df['category'] = df['middle_category'].map(FINAL_CATEGORY_MAPPING)
    df_sorted = df.sort_values(by='category')
    df_sorted.to_csv(output_file, index=False)
    print(f"Saved final categories to {output_file}")


def augment_survey_with_mapped_rows(input_file, output_file):
    df = pd.read_csv(input_file)
    columns = ['Q9_{}'.format(i) for i in range(1, 36)]
    descriptions = df.iloc[0, 26:61].tolist()

    cleaned_descriptions = []
    for desc in descriptions:
        if isinstance(desc, str) and '-' in desc:
            cleaned_descriptions.append(desc.split('-')[-1].strip())
        else:
            cleaned_descriptions.append('')

    middle_categories = [MIDDLE_CATEGORY_MAPPING.get(desc, '') for desc in cleaned_descriptions]

    new_row_df = pd.DataFrame([{col: cleaned_descriptions[i] for i, col in enumerate(columns)}])
    middle_row_df = pd.DataFrame([{col: middle_categories[i] for i, col in enumerate(columns)}])

    df_updated = pd.concat([df, new_row_df, middle_row_df], ignore_index=True)
    df_updated.to_csv(output_file, index=False)
    print(f"Survey updated with middle categories at {output_file}")


def append_final_categories(input_file, output_file):
    df = pd.read_csv(input_file)
    columns = ['Q9_{}'.format(i) for i in range(1, 36)]

    last_row = df.iloc[-1, 26:61]
    mapped_last_row = last_row.map(FINAL_CATEGORY_MAPPING).fillna('')
    new_row_df = pd.DataFrame([{col: mapped_last_row[i] for i, col in enumerate(columns)}])

    df_updated = pd.concat([df, new_row_df], ignore_index=True)
    df_updated.to_csv(output_file, index=False)
    print(f"Survey updated with final categories at {output_file}")


# ========== EXAMPLE USAGE ==========
if __name__ == "__main__":
    apply_topic_number_mapping(
        'results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet.csv',
        'results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet_corrected_topic_number.csv'
    )

    apply_middle_category_mapping(
        'results/data/final_dataset_standardized_dates.csv',
        'results/data/middle_category.csv'
    )

    apply_final_category_mapping(
        'results/data/middle_category.csv',
        'results/data/final_category.csv'
    )

    augment_survey_with_mapped_rows(
        'survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv',
        'survey/data.csv'
    )

    append_final_categories(
        'survey/data.csv',
        'survey/data2.csv'
    )
