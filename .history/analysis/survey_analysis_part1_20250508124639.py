import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')  # Prevents GUI backend issues for PDF saving

# ============================ CONFIGURATION ============================

SURVEY_PATH = 'survey/Understanding Challenges of Ruby Developers_September 12, 2024_17.02.csv'
COLUMNS = [f'Q9_{i}' for i in range(1, 36)]
MAX_LENGTH = 100

# ============================ HELPER FUNCTIONS ============================

def clean_descriptions(raw_descriptions):
    """Extracts cleaned description from the format 'Q9_1 - Description'"""
    return [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in raw_descriptions]

def normalize_counts(counts, total, max_length=MAX_LENGTH):
    """Normalizes count values for visualization."""
    return {f'norm_count_{i}': (counts.get(i, 0) / total) * max_length if total else 0 for i in range(1, 6)}

def compute_percentage_and_weighted_average(counts, total):
    """Computes 1–2%, 4–5% and weighted average for satisfaction"""
    count_1_2 = counts.get(1, 0) + counts.get(2, 0)
    count_4_5 = counts.get(4, 0) + counts.get(5, 0)
    percent_1_2 = (count_1_2 / total) * 100 if total else 0
    percent_4_5 = (count_4_5 / total) * 100 if total else 0
    weighted_avg = sum(i * counts.get(i, 0) for i in range(1, 6)) / total if total else 0
    return percent_1_2, percent_4_5, weighted_avg

def draw_stacked_bar_chart(items, label_key, filename, title):
    """Draws and saves a stacked horizontal bar chart."""
    cmap = plt.get_cmap('tab20c')
    colors = [cmap(i / 20) for i in range(20)]
    plt.figure(figsize=(14, len(items) * 0.5))

    for idx, item in enumerate(items):
        left = 0
        for i in range(1, 6):
            width = item[f'norm_count_{i}']
            plt.barh(item[label_key], width, left=left, color=colors[i - 1], label=str(i) if idx == 0 else "")
            plt.text(left + width / 2, idx, f"{(width / MAX_LENGTH) * 100:.1f}%", va='center', fontsize=8, color='black')
            left += width

        # Label descriptions or group names
        plt.text(-5, idx, f"{item.get('description', item[label_key])}", va='center', ha='right', fontsize=8)
        plt.text(left + 2, idx, f"{item['percent_4_5']:.1f}%", va='center', ha='left', fontsize=8)

    plt.xlim(0, MAX_LENGTH)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# ============================ ANALYSIS FUNCTIONS ============================

def analyze_individual_questions(df):
    """Analyzes each individual question and generates a bar chart."""
    raw_descriptions = df.iloc[0, 26:61].tolist()
    cleaned_descriptions = clean_descriptions(raw_descriptions)
    df[COLUMNS] = df[COLUMNS].apply(pd.to_numeric, errors='coerce')

    data = []
    for idx, col in tqdm(enumerate(COLUMNS), total=len(COLUMNS)):
        filtered = df[col][(df[col] >= 1) & (df[col] <= 5)]
        counts = filtered.value_counts().sort_index()
        total = sum(counts.values())
        norm_counts = normalize_counts(counts, total)
        percent_1_2, percent_4_5, weighted_avg = compute_percentage_and_weighted_average(counts, total)

        data.append({
            'column': col,
            'description': cleaned_descriptions[idx],
            **norm_counts,
            'percent_1_2': percent_1_2,
            'percent_4_5': percent_4_5
        })

    sorted_data = sorted(data, key=lambda x: x['percent_4_5'])
    draw_stacked_bar_chart(sorted_data, 'column', 'survey_part1_step1.pdf', 'Q9 Survey Ratings per Question')

def analyze_grouped_descriptions(df, description_to_group):
    """Analyzes questions grouped by their functional area."""
    raw_descriptions = df.iloc[0, 26:61].tolist()
    cleaned_descriptions = clean_descriptions(raw_descriptions)
    df[COLUMNS] = df[COLUMNS].apply(pd.to_numeric, errors='coerce')

    group_data = {}
    for idx, description in enumerate(cleaned_descriptions):
        group = description_to_group.get(description)
        if not group:
            continue

        col = COLUMNS[idx]
        counts = df[col][(df[col] >= 1) & (df[col] <= 5)].value_counts().sort_index()
        if group not in group_data:
            group_data[group] = {i: 0 for i in range(1, 6)}
        for i in range(1, 6):
            group_data[group][i] += counts.get(i, 0)

    items = []
    for group, counts in group_data.items():
        total = sum(counts.values())
        norm_counts = normalize_counts(counts, total)
        percent_1_2, percent_4_5, _ = compute_percentage_and_weighted_average(counts, total)
        items.append({
            'group': group,
            **norm_counts,
            'percent_1_2': percent_1_2,
            'percent_4_5': percent_4_5
        })

    sorted_items = sorted(items, key=lambda x: x['percent_4_5'])
    draw_stacked_bar_chart(sorted_items, 'group', 'survey_part1_step2.pdf', 'Q9 Survey Ratings by Group')

def analyze_categories(df, description_to_group, group_to_category):
    """Aggregates data into high-level categories and visualizes."""
    raw_descriptions = df.iloc[0, 26:61].tolist()
    cleaned_descriptions = clean_descriptions(raw_descriptions)
    df[COLUMNS] = df[COLUMNS].apply(pd.to_numeric, errors='coerce')

    category_data = {}
    for idx, desc in enumerate(cleaned_descriptions):
        group = description_to_group.get(desc)
        if not group:
            continue
        category = group_to_category.get(group)
        if not category:
            continue

        col = COLUMNS[idx]
        counts = df[col][(df[col] >= 1) & (df[col] <= 5)].value_counts().sort_index()
        if category not in category_data:
            category_data[category] = {i: 0 for i in range(1, 6)}
        for i in range(1, 6):
            category_data[category][i] += counts.get(i, 0)

    items = []
    for cat, counts in category_data.items():
        total = sum(counts.values())
        norm_counts = normalize_counts(counts, total)
        percent_1_2, percent_4_5, _ = compute_percentage_and_weighted_average(counts, total)
        items.append({
            'category': cat,
            **norm_counts,
            'percent_1_2': percent_1_2,
            'percent_4_5': percent_4_5
        })

    sorted_items = sorted(items, key=lambda x: x['percent_4_5'])
    draw_stacked_bar_chart(sorted_items, 'category', 'survey_part1_step3.pdf', 'Q9 Survey Ratings by Category')

# ============================ MAPPING DICTIONARIES ============================

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

# ============================ MAIN EXECUTION ============================

def main():
    df = pd.read_csv(SURVEY_PATH, low_memory=False)
    analyze_individual_questions(df)
    analyze_grouped_descriptions(df, DESCRIPTION_TO_GROUP)
    analyze_categories(df, DESCRIPTION_TO_GROUP, GROUP_TO_CATEGORY)

if __name__ == '__main__':
    main()
