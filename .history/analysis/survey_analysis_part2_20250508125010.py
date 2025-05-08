import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# ===== Configuration =====

SURVEY_PATH = 'survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv'
COLUMNS = [f'Q12_{i}' for i in range(1, 36)]
MAX_LENGTH = 100

# Mapping sentence responses to numeric values
SENTENCE_TO_NUMBER = {
    'less than 15 minutes': 1,
    'between 15 to 30 minutes': 2,
    'between 30 to 60 minutes': 3,
    'between 1 and 2 hours': 4,
    'more than 2 hours': 5
}

# ===== Description Group Mappings =====

DESCRIPTION_TO_GROUP = {
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

GROUP_TO_CATEGORY = {
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

# ===== Helper Functions =====

def clean_descriptions(descriptions_raw):
    return [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in descriptions_raw]

def normalize_counts(counts, total):
    return {f'norm_count_{i}': (counts.get(i, 0) / total) * MAX_LENGTH if total else 0 for i in range(1, 6)}

def compute_percentages(counts, total):
    count_1_2 = counts.get(1, 0) + counts.get(2, 0)
    count_4_5 = counts.get(4, 0) + counts.get(5, 0)
    return (
        (count_1_2 / total) * 100 if total else 0,
        (count_4_5 / total) * 100 if total else 0
    )

def plot_stacked_bar(data, key, title, filename):
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]

    plt.figure(figsize=(14, len(data) * 0.4))

    for idx, item in enumerate(data):
        left = 0
        for i in range(1, 6):
            width = item[f'norm_count_{i}']
            plt.barh(item[key], width, left=left, color=colors[i-1], label=str(i) if idx == 0 else "")
            left += width
        plt.text(left + 1, idx, f"{item['percent_4_5']:.1f}%", va='center', fontsize=8)

    plt.xlim(0, MAX_LENGTH)
    plt.title(title)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# ===== Main Function =====

def main():
    df = pd.read_csv(SURVEY_PATH)
    raw_descriptions = df.iloc[0, 72:107].tolist()
    cleaned_descriptions = clean_descriptions(raw_descriptions)

    # ========== Question-level ==========
    question_data = []
    for idx, col in tqdm(enumerate(COLUMNS), total=len(COLUMNS)):
        mapped = df[col].map(SENTENCE_TO_NUMBER)
        filtered = mapped[(mapped >= 1) & (mapped <= 5)]
        counts = filtered.value_counts().sort_index()
        total = counts.sum()
        norm = normalize_counts(counts, total)
        p12, p45 = compute_percentages(counts, total)

        question_data.append({
            'column': col,
            'description': cleaned_descriptions[idx],
            **norm,
            'percent_1_2': p12,
            'percent_4_5': p45
        })

    question_data.sort(key=lambda x: x['percent_4_5'])
    plot_stacked_bar(question_data, 'column', 'Time to Resolve by Question', 'survey_part2_step1.pdf')

    # ========== Group-level ==========
    group_counts = {g: {i: 0 for i in range(1, 6)} for g in set(DESCRIPTION_TO_GROUP.values())}
    for idx, desc in enumerate(cleaned_descriptions):
        group = DESCRIPTION_TO_GROUP.get(desc)
        if not group:
            continue
        mapped = df[COLUMNS[idx]].map(SENTENCE_TO_NUMBER)
        filtered = mapped[(mapped >= 1) & (mapped <= 5)]
        counts = filtered.value_counts().sort_index()
        for i in range(1, 6):
            group_counts[group][i] += counts.get(i, 0)

    group_data = []
    for group, counts in group_counts.items():
        total = sum(counts.values())
        norm = normalize_counts(counts, total)
        p12, p45 = compute_percentages(counts, total)
        group_data.append({'group': group, **norm, 'percent_1_2': p12, 'percent_4_5': p45})

    group_data.sort(key=lambda x: x['percent_4_5'])
    plot_stacked_bar(group_data, 'group', 'Time to Resolve by Group', 'survey_part2_step2.pdf')

    # ========== Category-level ==========
    category_counts = {c: {i: 0 for i in range(1, 6)} for c in set(GROUP_TO_CATEGORY.values())}
    for idx, desc in enumerate(cleaned_descriptions):
        group = DESCRIPTION_TO_GROUP.get(desc)
        if not group:
            continue
        category = GROUP_TO_CATEGORY.get(group)
        if not category:
            continue
        mapped = df[COLUMNS[idx]].map(SENTENCE_TO_NUMBER)
        filtered = mapped[(mapped >= 1) & (mapped <= 5)]
        counts = filtered.value_counts().sort_index()
        for i in range(1, 6):
            category_counts[category][i] += counts.get(i, 0)

    category_data = []
    for category, counts in category_counts.items():
        total = sum(counts.values())
        norm = normalize_counts(counts, total)
        p12, p45 = compute_percentages(counts, total)
        category_data.append({'category': category, **norm, 'percent_1_2': p12, 'percent_4_5': p45})

    category_data.sort(key=lambda x: x['percent_4_5'])
    plot_stacked_bar(category_data, 'category', 'Time to Resolve by Category', 'survey_part2_step3.pdf')

if __name__ == '__main__':
    main()
