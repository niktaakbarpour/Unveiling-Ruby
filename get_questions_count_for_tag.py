import requests
import itertools
from urllib.parse import quote

def get_questions_count_for_tag(api_key, tag):
    api_url = f"https://api.stackexchange.com/2.3/tags/{quote(tag)}/info"
    params = {
        'site': 'stackoverflow',
        'key': api_key,
    }

    print(f"Processing tag: {tag}")

    response = requests.get(api_url, params=params)

        # Check if the request was successful (status code in the range 200-299)
    if response.status_code // 100 != 2:
        print(f"Error: HTTP Status Code {response.status_code}")
        # Log unsuccessful tag to a file
        with open('tags/unsuccessful_tags.txt', 'a') as unsuccessful_tags_file:
            unsuccessful_tags_file.write(f"{tag}\n")
        return None

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['count']
    else:
        return None

def get_tags_from_file(file_path, start_line):
    with open(file_path, 'r') as file:
        # Use itertools.islice to start reading from a specific line
        return [tag.strip() for tag in itertools.islice(file, start_line-1, None)]

def main():
    api_key = 'UKCVof68)r15kpNYG0uMyg(('  # Replace with your actual API key
    input_file_path = 'tags/unsuccessful_tags.txt'  # Replace with your input file path
    output_file_path = 'tags/unsuccessful_tags_counts.txt'  # Replace with your desired output file path
    start_line = 1  # Specify the line number to start from

    tags = get_tags_from_file(input_file_path, start_line)
    processed_tags_count = 0

    # Write results to the txt file after processing each tag
    with open(output_file_path, 'a') as output_file:
        for tag in tags:
            question_count = get_questions_count_for_tag(api_key, tag)
            if question_count is not None:
                output_file.write(f'{tag}: {question_count}\n')
                print(f'Writing result for tag: {tag}, count: {question_count}')
            else:
                print(f'Failed to retrieve count for tag: {tag}')
            processed_tags_count += 1
            print(f"Processed {processed_tags_count} out of {len(tags)} tags")

    print(f"Results written to {output_file_path}")

if __name__ == "__main__":
    main()
