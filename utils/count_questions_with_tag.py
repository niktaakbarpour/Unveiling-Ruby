from utils.common import logger

def main():
    import csv
    import re

    def extract_tags(tag_str):
    # Extract individual tags from the angle-bracket format
        return re.findall(r'<(.*?)>', tag_str)

    def count_questions_for_tags(csv_data, tags):
        return sum(1 for row in csv_data if any(tag in extract_tags(row['Tags']) for tag in tags))

    def main():
        csv_filename = 'new_csvs\concatenated_data.csv'  # Replace with your actual CSV file path
        tags_filename = 'tags/tags.txt'  # Replace with your actual tags file path
        output_csv_filename = 'new_csvs/output_counts.csv'  # Replace with your desired output CSV file path

        # Read CSV file data into a list of dictionaries
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            csv_data = list(csv.DictReader(csvfile))

        with open(tags_filename, 'r') as tags_file, open(output_csv_filename, 'w', newline='', encoding='utf-8') as output_csv:
            fieldnames = ['Tag', 'NoQ_in_F']
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()

            for tag in tags_file:
                tag = tag.strip()  # Remove leading/trailing whitespaces
                count = count_questions_for_tags(csv_data, [tag])
                
                writer.writerow({'Tag': tag, 'NoQ_in_F': count})
                logger.info(f"Processed tag: {tag}, NoQ_in_F: {count}")

        logger.info(f"Results written to {output_csv_filename}")

    if __name__ == "__main__":
        main()

if __name__ == '__main__':
    main()