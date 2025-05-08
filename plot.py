import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file into a DataFrame
df = pd.read_csv('results/data/posts_more_meta_using_arc_corrected_name_corrected_sheet_corrected_topic_number.csv')

# Convert 'CreationDate' column to datetime format if not already
df['CreationDate'] = pd.to_datetime(df['CreationDate'])

# Extract year from 'CreationDate' column
df['Year'] = df['CreationDate'].dt.year

# Create a directory to save plots if it doesn't exist
output_dir = 'results/data/images'
os.makedirs(output_dir, exist_ok=True)

# Iterate over each unique topic
for topic in df['topic'].unique():
    # Filter the DataFrame for the current topic
    topic_data = df[df['topic'] == topic]
    
    # Count the number of questions for each year
    counts_per_year = topic_data['Year'].value_counts().sort_index()
    
    # Plotting the line chart
    plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
    plt.plot(counts_per_year.index, counts_per_year.values, marker='o', linestyle='-')
    
    # Customize the plot
    plt.title(f'Number of Questions Over Years for Topic: {topic}')
    plt.xlabel('Year')
    plt.ylabel('Number of Questions')
    
    # Save plot as an image file
    output_file = os.path.join(output_dir, f'topic_{topic}_by_year.png')
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()  # Close the plot to free memory

print(f'Plots saved in directory: {output_dir}')