from utils.common import logger
import pandas as pd

def get_unique_tags(csv_file):
    """
    Extracts unique tags from the 'Tags' column of a CSV file.
    Assumes tags are in Stack Overflow-style format: <tag1><tag2>...
    """
    df = pd.read_csv(csv_file)

    # Parse tags from Stack Overflow format
    all_tags_list = df['Tags'].astype(str).apply(
        lambda x: x.replace('><', ',').replace('<', '').replace('>', '').split(',')
    ).tolist()

    # Flatten and deduplicate
    flattened_tags = [tag.strip() for sublist in all_tags_list for tag in sublist]
    unique_tags = sorted(set(flattened_tags))

    logger.info(f"Found {len(unique_tags)} unique tags.")
    return unique_tags

def save_tags_to_txt(tags_list, output_file):
    """
    Saves a list of tags to a text file, one per line.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for tag in tags_list:
            f.write(f"{tag}\n")
    logger.info(f"Tags saved to {output_file}")

def main():
    csv_file_path = 'new_csvs/concatenated_data.csv'
    output_txt_file = 'tags/tags.txt'

    tags = get_unique_tags(csv_file_path)
    save_tags_to_txt(tags, output_txt_file)

if __name__ == '__main__':
    main()
