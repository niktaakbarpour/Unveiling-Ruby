from utils.common import logger

from bertopic import BERTopic
from bertopic.dimensionality import BaseDimensionalityReduction
def main():
    import cuml
    import os
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from random import randint
    import re
    import string
    import pickle
    from tqdm import tqdm
    from sklearn.feature_extraction.text import CountVectorizer
    import seaborn as sns
    with open('stopwords.pkl', 'rb') as file:
        stopwords = pickle.load(file)

    def preprocess_text(
            text, stop_words = stopwords, lowercase = True, remove_usernames = True, remove_URLs = True, remove_domains_path = True,
            remove_punctuations = True, remove_digits = True, reduce_consecutive_characters = True,
            reduce_immediate_duplicate_words = True, spell_check = True, remove_stop_words = True):

        # Convert text to lowercase
        if(lowercase):
            text = text.lower()

        # Remove @usernames
        if(remove_usernames):
            text = re.sub(r'@\w+', '', text)

        # URL removal
        if(remove_URLs):
            text = re.sub(r'\S*http\S+', '', text)
            text = re.sub(r'\S*www.\S+', '', text)
            text = re.sub(r'\S*/\S+', '', text)

        # Domain/Path Removal
        if(remove_domains_path):
            text = re.sub(r'\S+\.\S+' , '', text)
            text = re.sub(r'\S*\\\S+' , '', text)

        #text = re.sub(r'\S*bot\S*', '', text)

        # Consecutive Character Reduction
        if(reduce_consecutive_characters):
            text = re.sub(r'(.)\1{2,}', r'\1', text)

        # Immediate Duplicate Word Removal
        if(reduce_immediate_duplicate_words):
            text = re.sub(r'\b(\w+)(\s+\1){1,}\b', r'\1', text)

        # Spell Checker
        if(spell_check):
            spell = SpellChecker()
            corrected_text = []
            for word in text.split():
                corrected_word = spell.correction(word)
                corrected_text.append(corrected_word if corrected_word else word)
            text = ' '.join(corrected_text)


        # Remove punctuations
        if(remove_punctuations):
            text = text.translate(str.maketrans('', '', string.punctuation))

        # Remove digits
        if(remove_digits):
            text = re.sub(r'\d+', '', text)

        # Remove stop words
        if(remove_stop_words and stop_words):
            text = ' '.join([word for word in text.split() if word not in stop_words])

        # Whitespace Normalization
        text = re.sub(r'\s+', ' ', text).strip()

        return text


    path = os.path.join('stack_overflow_embeddings.npy')
    embeddings = np.load(path)

    path = os.path.join('preprocessed_data.csv')
    posts = pd.read_csv(path, encoding='utf-8')
    posts['CombinedText'] = posts['CombinedText'].astype(str)
    messages = posts['CombinedText'].to_list()

    cleaned_messages = [preprocess_text(
            message, stop_words = stopwords, lowercase = False, remove_usernames = False, remove_URLs = False, remove_domains_path = False,
            remove_punctuations = True, remove_digits = False, reduce_consecutive_characters = False,
            reduce_immediate_duplicate_words = False, spell_check = False, remove_stop_words = True) for message in tqdm(messages, desc="preprocessing")]





    betopic_model_directory = 'Bertopic Models'
    betopic_model_directory = os.path.join(directory, 'Bertopic Models')
    if not os.path.isdir(betopic_model_directory):
        os.mkdir(betopic_model_directory)


    for k in tqdm(range(10, 51, 1)):
        path = os.path.join(betopic_model_directory, f'k_{k}')
        if os.path.isdir(path):
            continue
        empty_dimensionality_model = BaseDimensionalityReduction()
        vectorizer_model = CountVectorizer(ngram_range=(1, 2), max_df = 0.4)
        kmeans = cuml.KMeans(n_clusters=k, random_state=0) # this needs graphics card and cuda
        topic_model = BERTopic(umap_model=empty_dimensionality_model, hdbscan_model=kmeans, verbose=False, top_n_words=10, vectorizer_model = vectorizer_model)
        topics, _ = topic_model.fit_transform(cleaned_messages, embeddings)
        topic_model.save(path, serialization="safetensors", save_ctfidf=True)

if __name__ == '__main__':
    main()