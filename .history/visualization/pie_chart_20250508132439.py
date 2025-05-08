from utils.common import logger
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_cluster_plot_data(file_path):
    df = pd.read_csv(file_path)
    return df['min_cluster_size'], df['coherence_score']

def plot_coherence_score(min_cluster_size, coherence_score, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(min_cluster_size, coherence_score, marker='o', linestyle='-', color='b')
    plt.title('Coherence Score vs. Min Cluster Size')
    plt.xlabel('Min Cluster Size')
    plt.ylabel('Coherence Score')
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()
    logger.info(f"Coherence plot saved to {output_file}")

def get_pie_chart_data():
    labels = [
        ['Ruby Array and Hash Operations', 'Regular Expressions in Ruby', 'Algorithm Design in Ruby', 'Advanced Ruby Methods and Metaprogramming', 
         'File Handling and External Integrations', 'Spreadsheet and CSV Management', 'JSON and Data Serialization', 
         'ActiveRecord Associations', 'Database Management and Schema Design', 'Data Query and Manipulation', 
         'Ruby Gem Installation and Configuration Issues', 'Environment and Dependency Management', 
         'Automation with Chef', 'Deployment and Server Configuration', 'Heroku Deployment and Configuration', 
         'System Integration and External Libraries', 'Job Scheduling and Background Processes', 'Web Interface and UX Customization', 
         'Frontend Integration and User Interaction', 'jQuery and AJAX', 'Email Delivery with Rails ActionMailer', 
         'Asset Management and Integration Issues', 'Search Engines Integration', 'Payment and Financial Integration', 
         'API Management', 'Routing and URLs', 'Time Zone Management and Date Operations', 
         'User Authentication and Role Management', 'Rails Method and Parameter Errors', 'Validation and Error Handling', 
         'Mass Assignment & Parameter Protection Issues', 'Debugging and Error Handling', 'Automated Testing and Integration Testing', 
         'Design Patterns', 'Performance Optimization'],
        
        ['Core Ruby Operations', 'Algorithm Design', 'Advanced Ruby Concepts', 'Data Handling and Serialization', 
         'Database and ActiveRecord', 'Environment and Dependency Management', 'Deployment and Infrastructure Management', 
         'System Integration', 'Background Processing', 'Frontend Development in Rails', 'External Services and API Integrations', 
         'Routing and URLs', 'Time and Date Management', 'User Authentication', 'Error Handling and Validation', 
         'Testing and Quality Assurance', 'Software Design Patterns', 'Performance Optimization'],
        
        ['Core Ruby Concepts', 'Data Management and Processing', 'Development Environment and Infrastructure', 
         'Web Application Development', 'Application Quality and Security', 'Software Architecture and Performance']
    ]

    sizes = [
        [3.54, 1.03, 2.38, 4.23, 2.09, 1.13, 2.14, 5.83, 4.62, 3.84, 2.93, 4.81, 0.29, 1.54, 1.63, 
         3.29, 1.38, 5.91, 3.15, 4.74, 1.07, 1.87, 0.71, 0.48, 3.58, 2.34, 0.89, 2.72, 5.66, 2.12, 
         6.33, 3.16, 5.96, 1.65, 0.94],
        
        [4.58, 2.39, 4.24, 5.38, 14.32, 7.76, 3.18, 3.29, 1.38, 13.84,
         7.73, 2.35, 0.89, 2.73, 17.31, 5.97, 1.65, 0.94],
        
        [11.22, 19.71, 15.62, 27.55, 23.28, 2.59]
    ]
    return labels, sizes

def get_colors(sizes):
    norm = plt.Normalize(vmin=min(sizes), vmax=max(sizes))
    cmap = plt.get_cmap('GnBu')
    return [cmap(norm(size)) for size in sizes]

def plot_nested_pie_chart(labels, sizes, output_file):
    outer_colors = get_colors(sizes[0])
    middle_colors = get_colors(sizes[1])
    inner_colors = get_colors(sizes[2])

    fig, ax = plt.subplots(figsize=(12, 12))
    radius_levels = [1.3, 1.0, 0.7]
    widths = 0.3

    # Outer
    wedges, _ = ax.pie(sizes[0], labels=['']*len(labels[0]), radius=radius_levels[0], colors=outer_colors,
                       wedgeprops=dict(width=widths, edgecolor='w'))
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2.0
        x, y = radius_levels[0] * np.cos(np.radians(angle)), radius_levels[0] * np.sin(np.radians(angle))
        line_x, line_y = 1.5 * np.cos(np.radians(angle)), 1.5 * np.sin(np.radians(angle))
        ha = 'left' if x > 0 else 'right'
        ax.plot([x, line_x], [y, line_y], color='black', linewidth=0.8)
        ax.text(line_x, line_y, f"{labels[0][i]} ({sizes[0][i]}%)", ha=ha, va='center', fontsize=7)

    # Middle
    wedges_middle, _ = ax.pie(sizes[1], labels=['']*len(labels[1]), radius=radius_levels[1], colors=middle_colors,
                              wedgeprops=dict(width=widths, edgecolor='w'))
    for i, wedge in enumerate(wedges_middle):
        angle = (wedge.theta2 + wedge.theta1) / 2.0
        x, y = 0.85 * np.cos(np.radians(angle)), 0.85 * np.sin(np.radians(angle))
        label = f"{labels[1][i]}\n({sizes[1][i]}%)"
        ax.text(x, y, label, ha='center', va='center', fontsize=7, rotation=angle if -90 < angle < 90 else angle + 180)

    # Inner
    wedges_inner, _ = ax.pie(sizes[2], labels=['']*len(labels[2]), radius=radius_levels[2], colors=inner_colors,
                             wedgeprops=dict(width=widths, edgecolor='w'))
    for i, wedge in enumerate(wedges_inner):
        angle = (wedge.theta2 + wedge.theta1) / 2.0
        x, y = 0.54 * np.cos(np.radians(angle)), 0.54 * np.sin(np.radians(angle))
        label = f"{labels[2][i]}\n({sizes[2][i]}%)"
        ax.text(x, y, label, ha='center', va='center', fontsize=7, rotation=angle if -90 < angle < 90 else angle + 180)

    ax.set(aspect='equal')
    plt.savefig(output_file)
    plt.close()
    logger.info(f"Pie chart saved to {output_file}")

def main():
    # Part 1: Plot coherence score
    min_cluster_size, coherence_score = load_cluster_plot_data('data/plot.csv')
    plot_coherence_score(min_cluster_size, coherence_score, 'coherence_score_vs_min_cluster_size.png')

    # Part 2: Plot nested pie chart
    labels, sizes = get_pie_chart_data()
    plot_nested_pie_chart(labels, sizes, 'pie_chart_without_labels.pdf')

if __name__ == '__main__':
    main()
