import os
import re
import string
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from bertopic import BERTopic
from bertopic.dimensionality import BaseDimensionalityReduction
from cuml import KMeans
from sklearn.feature_extraction.text import CountVectorizer
# from spellchecker import SpellChecker  # Optional, comment out unless needed
from utils.common import logger  # You must have a logger setup

def preprocess_text(
    text,
    stop_words=None,
    lowercase=True,
    remove_usernames=True,
    remove_URLs=True,
    remove_domains_path=True,
    remove_punctuations=True,
    remove_digits=True,
    reduce_consecutive_characters=True,
    reduce_immediate_duplicate_words=True,
    spell_check=False,
    remove_stop_words=True
):
    """Clean and normalize a single text entry."""
    if lowercase:
        text = text.lower()
    if remove_usernames:
        text = re.sub(r'@\w+', '', text)
    if remove_URLs:
        text = re.sub(r'\S*http\S+|\S*www\.\S+|\S*/\S+', '', text)
    if remove_domains_path:
        text = re.sub(r'\S+\.\S+|\S*\\\S+', '', text)
    if reduce_consecutive_characters:
        text = re.sub(r'(.)\1{2,}', r'\1', text)
    if reduce_immediate_duplicate_words:
        text = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', text)
    # if spell_check:
    #     spell = SpellChecker()
    #     text = ' '.join([spell.correction(w) or w for w in text.split()])
    if remove_punctuations:
        text = text.translate(str.maketrans('', '', string.punctuation))
    if remove_digits:
        text = re.sub(r'\d+', '', text)
    if remove_stop_words and stop_words:
        text = ' '.join([word for word in text.split() if word not in stop_words])
    return re.sub(r'\s+', ' ', text).strip()

def run_bertopic_grid_search(embeddings, texts, stopwords, save_dir='Bertopic Models', k_range=(10, 51)):
    """
    Run BERTopic model for a range of cluster sizes and save models.

    Args:
        embeddings (np.ndarray): Precomputed embeddings.
        texts (List[str]): List of cleaned text documents.
        stopwords (Set[str]): Set of stopwords.
        save_dir (str): Directory to save models.
        k_range (tuple): Range of cluster numbers to train.
    """
    os.makedirs(save_dir, exist_ok=True)
    logger.info(f"🔍 Searching over k={k_range[0]} to k={k_range[1]-1}")

    for k in tqdm(range(*k_range), desc="BERTopic clustering"):
        model_path = os.path.join(save_dir, f'k_{k}')
        if os.path.isdir(model_path):
            continue
        logger.info(f"Training BERTopic with k={k}")

        vectorizer_model = CountVectorizer(ngram_range=(1, 2), max_df=0.4)
        kmeans = KMeans(n_clusters=k, random_state=0)
        topic_model = BERTopic(
            umap_model=BaseDimensionalityReduction(),
            hdbscan_model=kmeans,
            top_n_words=10,
            vectorizer_model=vectorizer_model,
            verbose=False
        )
        topics, _ = topic_model.fit_transform(texts, embeddings)
        topic_model.save(model_path, serialization="safetensors", save_ctfidf=True)
        logger.info(f"✅ Model saved to {model_path}")

def main():
    # Load stopwords
    with open('stopwords.pkl', 'rb') as file:  # TODO: replace path as needed
        stopwords = pickle.load(file)

    # Load embeddings
    embeddings_path = 'stack_overflow_embeddings.npy'  # TODO: replace
    embeddings = np.load(embeddings_path)

    # Load text data
    posts_path = 'preprocessed_data.csv'  # TODO: replace
    posts = pd.read_csv(posts_path)
    posts['CombinedText'] = posts['CombinedText'].astype(str)
    raw_messages = posts['CombinedText'].tolist()

    # Preprocess text
    cleaned_messages = [
        preprocess_text(msg, stop_words=stopwords, lowercase=False,
                        remove_usernames=False, remove_URLs=False,
                        remove_domains_path=False, spell_check=False)
        for msg in tqdm(raw_messages, desc="Preprocessing")
    ]

    # Run BERTopic model training
    run_bertopic_grid_search(embeddings, cleaned_messages, stopwords)

if __name__ == "__main__":
    main()
