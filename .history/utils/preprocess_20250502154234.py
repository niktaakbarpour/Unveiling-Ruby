from utils.common import logger

import pandas as pd
import re
from gensim.parsing.preprocessing import strip_numeric, strip_punctuation, remove_stopwords
from bs4 import BeautifulSoup
import html

# def add_combined_text_column(input_file_path, output_file_path):
df = pd.read_csv(input_file_path)
#     df['CombinedText'] = df['Title'] + '\n' + df['Body']
df.to_csv(output_file_path, index=False)

# def remove_escape_characters(s):
#     return re.sub(r'\\.', ' ', s)

# def clean_html_tags(text):
soup = BeautifulSoup(text, 'html.parser')
#     return soup.get_text(separator=' ')


# def clean_code_blocks(content):
#     code_patterns = [r'```.*?```', r'``.*?``', r'`.*?`']
#     clean_text = content
for code_pattern in code_patterns:
#         clean_text = re.sub(code_pattern, '', clean_text, flags=re.DOTALL)
#     clean_text = html.unescape(clean_text)
#     return clean_text


# def extract_links(text):
#     link_pattern1 = r"\!?\[.*?\]\((.*?)\)"
#     clean_text = re.sub(link_pattern1, '', text)
#     link_pattern2 = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
#     clean_text = re.sub(link_pattern2, '', clean_text)
#     return clean_text

# def handle_missing_values(df):
df_cleaned = df.dropna(subset=['CombinedText'])
#     df_cleaned.reset_index(drop=True, inplace=True)
#     return df_cleaned

# def preprocess_text(df):
#     df['CombinedText'] = df['CombinedText'].str.lower()
logger.info("lower")
#     df['CombinedText'] = df['CombinedText'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
logger.info("ascii")
#     df['CombinedText'] = df['CombinedText'].apply(remove_escape_characters)
logger.info("remove_escape_characters")
#     df['CombinedText'] = df['CombinedText'].apply(extract_links)
logger.info("extract_links")
#     df['CombinedText'] = df['CombinedText'].apply(clean_html_tags)
logger.info("clean_html_tags")
#     df['CombinedText'] = df['CombinedText'].apply(clean_code_blocks)
logger.info("clean_code_blocks")
#     # df['CombinedText'] = df['CombinedText'].apply(strip_punctuation)
# logger.info("strip_punctuation")
#     df['CombinedText'] = df['CombinedText'].apply(strip_numeric)
logger.info("strip_numeric")
#     # df['CombinedText'] = df['CombinedText'].apply(remove_stopwords)
# logger.info("remove_stopwords")
#     return df

if __name__ == "__main__":
#     input_file_path = './results/data/deduplicated_data.csv'
#     output_file_path = './results/data/preprocessed_data.csv'
    
#     add_combined_text_column(input_file_path, output_file_path)
    
df = pd.read_csv(output_file_path)
#     # df = preprocess_text(df)
#     df = handle_missing_values(df)
logger.info("handle_missing_values")
    
df.to_csv(output_file_path, index=False)



def main():
    import pandas as pd
    import re
    from gensim.parsing.preprocessing import strip_numeric, strip_punctuation, remove_stopwords
    from bs4 import BeautifulSoup
    import html
    import csv

    def add_combined_text_column(input_file_path, output_file_path):
        df = pd.read_csv(input_file_path)
        df['CombinedText'] = df['Title'] + '\n' + df['Body']
        df.to_csv(output_file_path, index=False)

    def remove_escape_characters(s):
        return re.sub(r'\\.', ' ', s)

    def clean_html_tags(text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return soup.get_text().encode('ascii', 'ignore').decode('ascii')
            #return soup.get_text(separator=' ')
        except:
            return text

    #def clean_code_blocks(content):
    #    code_patterns = [r'```.*?```', r'``.*?``', r'`.*?`']
    #    clean_text = content
    for code_pattern in code_patterns:
    #        clean_text = re.sub(code_pattern, '', clean_text, flags=re.DOTALL)
    #    clean_text = html.unescape(clean_text)
    #    return clean_text

    def extract_links(text):
        link_pattern1 = r"\!?\[.*?\]\((.*?)\)"
        clean_text = re.sub(link_pattern1, '', text)
        link_pattern2 = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        clean_text = re.sub(link_pattern2, '', clean_text)
        return clean_text

    def handle_missing_values(df):
        df_cleaned = df.dropna(subset=['CombinedText'])
        df_cleaned.reset_index(drop=True, inplace=True)
        return df_cleaned

    def clean_code_blocks(text):
        # This regular expression matches anything between <code> and </code> including the tags themselves.
        pattern = re.compile(r'<code>.*?</code>', re.DOTALL)
        # Replace all occurrences with an empty string.
        return re.sub(pattern, '', text)

    def preprocess_text(df):
        df['CombinedText'] = df['CombinedText'].astype(str)
        #df['CombinedText'] = df['CombinedText'].lower()
        df['CombinedText'] = df['CombinedText'].apply(lambda x: x.lower())
        df['CombinedText'] = df['CombinedText'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
        df['CombinedText'] = df['CombinedText'].apply(clean_code_blocks)
        # df['CombinedText'] = df['CombinedText'].apply(remove_escape_characters)

        df['CombinedText'] = df['CombinedText'].apply(extract_links)

        df['CombinedText'] = df['CombinedText'].apply(clean_html_tags)
        
        df['CombinedText'] = df['CombinedText'].apply(strip_numeric)
        return df

    if __name__ == "__main__":
        input_file_path = './results/data/deduplicated_data.csv'
        output_file_path = './results/data/preprocessed_data.csv'
        
        # Add the CombinedText column to the DataFrame and save it
        add_combined_text_column(input_file_path, output_file_path)
        
        # Load the new DataFrame with the CombinedText column
        
        df = pd.read_csv(output_file_path)
        
        # Preprocess the text in the CombinedText column
        df = preprocess_text(df)
        logger.info("Preprocessing complete")
        
        # Handle missing values
        #df = handle_missing_values(df)
    #logger.info("Handling missing values complete")
        
        # Save the preprocessed DataFrame to the output file
        df.to_csv(output_file_path, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        

if __name__ == '__main__':
    main()