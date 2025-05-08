from utils.common import logger
import csv
import re

def extract_tags(tag_str):
    """
    Extracts individual tags from a Stack Overflow-style angle-bracket tag string.
    Example: '<ruby><arrays>' → ['ruby', 'arrays']
    """
    return re.findall(r'<(.*?)>', tag_str)

def count_questions_for_tags(csv_data, tags):
    """
    Counts the number of questions that include at least one of the specified tags.
    """
    return sum(1 for row in csv_data if any(tag in extract_tags(row['Tags']) for tag in tags))

def count_tag_frequencies(csv_filename, tags_filename, output_csv_filename):
    """
    Reads a dataset of posts and a list of tags, counts the number of questions
    associated with each tag, and writes the results to a CSV file.
    """
    # Load CSV post data
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        csv_data = list(csv.DictReader(csvfile))

    # Open tags list and output CSV
    with open(tags_filename, 'r') as tags_file, open(output_csv_filename, 'w', newline='', encoding='utf-8') as output_csv:
        fieldnames = ['Tag', 'NoQ_in_F']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        for tag in tags_file:
            tag = tag.strip()
            count = count_questions_for_tags(csv_data, [tag])
            writer.writerow({'Tag': tag, 'NoQ_in_F': count})
            logger.info(f"Processed tag: {tag}, NoQ_in_F: {count}")

    logger.info(f"✅ Results written to {output_csv_filename}")

def main():
    csv_filename = 'new_csvs/concatenated_data.csv'
    tags_filename = 'tags/tags.txt'
    output_csv_filename = 'new_csvs/output_counts.csv'
    count_tag_frequencies(csv_filename, tags_filename, output_csv_filename)

if __name__ == '__main__':
    main()
