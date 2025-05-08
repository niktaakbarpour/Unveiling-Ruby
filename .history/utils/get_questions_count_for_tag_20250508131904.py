from utils.common import logger

def get_questions_count_for_tag(api_key, tag):
    """Query StackOverflow API to get question count for a given tag."""
    import requests
    from urllib.parse import quote

    api_url = f"https://api.stackexchange.com/2.3/tags/{quote(tag)}/info"
    params = {'site': 'stackoverflow', 'key': api_key}

    logger.info(f"Processing tag: {tag}")
    response = requests.get(api_url, params=params)

    if response.status_code // 100 != 2:
        logger.info(f"Error: HTTP {response.status_code} for tag: {tag}")
        with open('tags/unsuccessful_tags.txt', 'a') as fail_log:
            fail_log.write(f"{tag}\n")
        return None

    try:
        data = response.json()
    except Exception as e:
        logger.info(f"JSON decode error for tag: {tag}: {e}")
        return None

    if 'items' in data and data['items']:
        return data['items'][0]['count']
    return None


def get_tags_from_file(file_path, start_line=1):
    """Read tag list starting from a specific line in a file."""
    import itertools
    with open(file_path, 'r') as file:
        return [tag.strip() for tag in itertools.islice(file, start_line - 1, None)]


def write_tag_counts(api_key, input_path, output_path, start_line=1):
    tags = get_tags_from_file(input_path, start_line)
    processed = 0

    with open(output_path, 'a', encoding='utf-8') as outfile:
        for tag in tags:
            count = get_questions_count_for_tag(api_key, tag)
            if count is not None:
                outfile.write(f"{tag}: {count}\n")
                logger.info(f"✅ {tag}: {count}")
            else:
                logger.info(f"❌ Failed: {tag}")
            processed += 1
            logger.info(f"[{processed}/{len(tags)}] Processed")

    logger.info(f"✅ All results written to {output_path}")


def main():
    api_key = 'UKCVof68)r15kpNYG0uMyg(('  # Replace with your real API key
    input_file = 'tags/unsuccessful_tags.txt'
    output_file = 'tags/unsuccessful_tags_counts.txt'
    start_from_line = 1  # Adjust if resuming

    write_tag_counts(api_key, input_file, output_file, start_from_line)


if __name__ == '__main__':
    main()
