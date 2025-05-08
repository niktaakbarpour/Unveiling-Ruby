# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv('data/plot.csv')

# min_cluster_size = df['min_cluster_size']
# coherence_score = df['coherence_score']

# plt.figure(figsize=(10, 6))
# plt.plot(min_cluster_size, coherence_score, marker='o', linestyle='-', color='b')

# plt.title('Coherence Score vs. Min Cluster Size')
# plt.xlabel('Min Cluster Size')
# plt.ylabel('Coherence Score')

# plt.grid(True)

# plt.savefig('coherence_score_vs_min_cluster_size.png')

import matplotlib.pyplot as plt
import numpy as np

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

def get_colors(sizes):
    norm = plt.Normalize(vmin=min(sizes), vmax=max(sizes))
    cmap = plt.get_cmap('GnBu')
    return [cmap(norm(size)) for size in sizes]

outer_colors = get_colors(sizes[0])
middle_colors = get_colors(sizes[1])
inner_colors = get_colors(sizes[2])

fig, ax = plt.subplots(figsize=(12, 12))

wedges, _ = ax.pie(sizes[0], labels=[''] * len(labels[0]), radius=1.3, colors=outer_colors,
                   wedgeprops=dict(width=0.3, edgecolor='w'))

for i, wedge in enumerate(wedges):
    angle = (wedge.theta2 + wedge.theta1) / 2.0
    x = 1.3 * np.cos(np.radians(angle))
    y = 1.3 * np.sin(np.radians(angle))
    
    line_x = 1.5 * np.cos(np.radians(angle))
    line_y = 1.5 * np.sin(np.radians(angle))
    
    ha = 'left' if x > 0 else 'right'
    
    ax.plot([x, line_x], [y, line_y], color='black', linestyle='-', linewidth=0.8)
    
    label = f"{labels[0][i]} ({sizes[0][i]}%)" 
    ax.text(line_x, line_y, label, ha=ha, va='center', fontsize=7)

wedges_middle, _ = ax.pie(sizes[1], labels=[''] * len(labels[1]), radius=1.0, colors=middle_colors,
                          wedgeprops=dict(width=0.3, edgecolor='w'))

for i, wedge in enumerate(wedges_middle):
    angle = (wedge.theta2 + wedge.theta1) / 2.0
    x = 0.85 * np.cos(np.radians(angle))
    y = 0.85 * np.sin(np.radians(angle))
    
    rotation = angle if -90 < angle < 90 else angle + 180
    
    label = f"{labels[1][i]}\n({sizes[1][i]}%)"
    if len(label) > 30:  
        if label.count(' ') >= 2:  
            label = label.replace(' ', '\n', 2)
            label = label.replace('\n', ' ', 1) 
    ax.text(x, y, label, ha='center', va='center', fontsize=7, rotation=rotation)

wedges_inner, _ = ax.pie(sizes[2], labels=[''] * len(labels[2]), radius=0.7, colors=inner_colors,
                         wedgeprops=dict(width=0.3, edgecolor='w'))

for i, wedge in enumerate(wedges_inner):
    angle = (wedge.theta2 + wedge.theta1) / 2.0
    x = 0.54 * np.cos(np.radians(angle))
    y = 0.54 * np.sin(np.radians(angle))

    rotation = angle if -90 < angle < 90 else angle + 180

    print(angle)
    
    label = f"{labels[2][i]}\n({sizes[2][i]}%)"
    print(label, rotation)
    if len(label) > 30:  
        if label.count(' ') >= 2:  
            label = label.replace(' ', '\n', 2)
            label = label.replace('\n', ' ', 1)
  
    ax.text(x, y, label, ha='center', va='center', fontsize=7, rotation=rotation)

ax.set(aspect="equal")

# plt.savefig('pie_chart_without_labels.pdf')
plt.show()