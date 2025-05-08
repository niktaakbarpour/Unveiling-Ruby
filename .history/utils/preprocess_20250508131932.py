from utils.common import logger

def add_combined_text_column(input_file_path, output_file_path):
    import pandas as pd
    df = pd.read_csv(input_file_path)
    df['CombinedText'] = df['Title'] + '\n' + df['Body']
    df.to_csv(output_file_path, index=False)
    logger.info("CombinedText column added and saved.")


def remove_escape_characters(s):
    import re
    return re.sub(r'\\.', ' ', s)


def clean_html_tags(text):
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text().encode('ascii', 'ignore').decode('ascii')
    except:
        return text


def extract_links(text):
    import re
    text = re.sub(r"\!?\[.*?\]\((.*?)\)", '', text)
    text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F]{2}))+", '', text)
    return text


def clean_code_blocks(text):
    import re
    return re.sub(r'<code>.*?</code>', '', text, flags=re.DOTALL)


def preprocess_text_column(df):
    import re
    from gensim.parsing.preprocessing import strip_numeric

    df['CombinedText'] = df['CombinedText'].astype(str)
    df['CombinedText'] = df['CombinedText'].str.lower()
    df['CombinedText'] = df['CombinedText'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['CombinedText'] = df['CombinedText'].apply(clean_code_blocks)
    df['CombinedText'] = df['CombinedText'].apply(extract_links)
    df['CombinedText'] = df['CombinedText'].apply(clean_html_tags)
    df['CombinedText'] = df['CombinedText'].apply(strip_numeric)
    return df


def handle_missing_values(df):
    df_cleaned = df.dropna(subset=['CombinedText'])
    df_cleaned.reset_index(drop=True, inplace=True)
    return df_cleaned


def main():
    import pandas as pd
    import csv

    input_file_path = './results/data/deduplicated_data.csv'
    output_file_path = './results/data/preprocessed_data.csv'

    # Step 1: Add CombinedText
    add_combined_text_column(input_file_path, output_file_path)

    # Step 2: Load, preprocess and save
    df = pd.read_csv(output_file_path)
    df = preprocess_text_column(df)
    logger.info("Preprocessing complete.")

    df.to_csv(output_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
    logger.info(f"Final cleaned data saved to {output_file_path}")


if __name__ == '__main__':
    main()
