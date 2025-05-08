from utils.common import logger

def main():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Load your data
    df = pd.read_csv('survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv')

    # Mapping descriptions to groups
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
        'Time Zone Management and Date Operations in Rails': 'Web Application Development',
        'User Authentication and Role Management': 'Web Application Development',
        'Rails Method and Parameter Errors': 'Error Handling and Validation',
        'Validation and Error Handling in Ruby on Rails': 'Error Handling and Validation',
        'Rails Mass Assignment & Parameter Protection Issues': 'Error Handling and Validation',
        'Ruby Debugging and Error Handling': 'Error Handling and Validation',
        'Automated Testing and Integration Testing in Ruby on Rails': 'Testing and Quality Assurance',
        'Rails Design Patterns': 'Software Design Patterns',
        'Performance Optimization in Rails': 'Performance Optimization'
    }

    # Group to category mapping
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

    # Define response mapping
    sentence_to_number = {
        'less than 15 minutes': 1,
        'between 15 to 30 minutes': 2,
        'between 30 to 60 minutes': 3,
        'between 1 and 2 hours': 4,
        'more than 2 hours': 5
    }

    # Define the columns of interest and descriptions
    columns = ['Q12_{}'.format(i) for i in range(1, 36)]
    descriptions = df.iloc[0, 72:107].tolist()

    # Prepare data for the violin plot
    violin_data = []

    # Clean and gather response data
    cleaned_descriptions = []
    for desc in descriptions:
        if isinstance(desc, str) and '-' in desc:
            cleaned_descriptions.append(desc.split('-')[-1].strip())
        else:
            cleaned_descriptions.append('')

    for idx, description in enumerate(cleaned_descriptions):
        group = description_to_group.get(description, None)
        
        if group:
            category = group_to_category.get(group, None)
            col = columns[idx]
            mapped_col = df[col].map(sentence_to_number)
            
            # Only keep valid responses
            valid_responses = mapped_col[(mapped_col >= 1) & (mapped_col <= 5)]
            if category:  # Check if category exists
                for response in valid_responses:
                    violin_data.append({
                        'Category': category,
                        'Response': response
                    })

    violin_df = pd.DataFrame(violin_data)

    response_counts = violin_df.groupby(['Category', 'Response']).size().unstack(fill_value=0)


    melted_response_counts = response_counts.stack().reset_index()
    melted_response_counts.columns = ['Category', 'Response', 'Count']
    logger.info(melted_response_counts)

    plt.figure(figsize=(12, 6))

    cmap = plt.get_cmap('Paired')
    colors = [cmap(i / 12) for i in range(12)]

    sns.violinplot(
        x='Category', 
        y='Response', 
        data=violin_df, 
        inner=None, 
        scale='area', 
        palette=colors
    )

    plt.ylabel('Response Time (1-5)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('violin_chart_step3.pdf')
    plt.show()

if __name__ == '__main__':
    main()