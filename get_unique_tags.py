import pandas as pd

def get_unique_tags(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the 'Tags' column
    tags_column = df['Tags']

    # Split each tag string into a list of tags
    all_tags_list = [tag.replace('><', ',').replace('<', '').replace('>', '').split(',') for tag in tags_column]

    # Flatten the list of lists into a single list
    flattened_tags_list = [tag for sublist in all_tags_list for tag in sublist]

    # Get unique tags
    unique_tags = list(set(flattened_tags_list))

    return unique_tags

def save_tags_to_txt(tags_list, output_file):
    # Write each unique tag to a text file
    with open(output_file, 'w') as txt_file:
        for tag in tags_list:
            txt_file.write(f"{tag}\n")

# Example usage
csv_file_path = 'new_csvs\concatenated_data.csv'
output_txt_file = 'tags/tags.txt'

unique_tags_list = get_unique_tags(csv_file_path)
save_tags_to_txt(unique_tags_list, output_txt_file)
