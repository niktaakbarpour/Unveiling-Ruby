import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from gensim.models.coherencemodel import CoherenceModel
import gensim.corpora as corpora
from utils.common import logger


def train_topic_model(documents, config):
    embedding_model = SentenceTransformer(config['model_name'])
    umap_model = UMAP(
        n_components=config['n_components'],
        metric=config['metric_distance'],
        random_state=config['random_state'],
        low_memory=config['low_memory']
    )
    hdbscan_model = HDBSCAN(
        min_cluster_size=config['min_cluster_size'],
        min_samples=1,
        prediction_data=config['calculate_probabilities']
    )
    vectorizer_model = CountVectorizer(
        ngram_range=(1, config['ngram_range']),
        stop_words='english'
    )
    ctfidf_model = ClassTfidfTransformer(
        reduce_frequent_words=config['reduce_frequent_words']
    )
    representation_model = KeyBERTInspired()

    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        representation_model=representation_model,
        calculate_probabilities=config['calculate_probabilities'],
        nr_topics="auto",
        verbose=False
    )
    topics, _ = topic_model.fit_transform(documents)
    return topic_model, topics


def evaluate_coherence(topic_model, topics, documents):
    docs_df = pd.DataFrame({
        "Document": documents,
        "Topic": topics
    })
    docs_per_topic = docs_df.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
    cleaned_docs = topic_model._preprocess_text(docs_per_topic.Document.values)
    analyzer = topic_model.vectorizer_model.build_analyzer()
    tokens = [analyzer(doc) for doc in cleaned_docs]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]

    topic_words = [[word for word, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics)) - 1)]
    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=tokens,
        corpus=corpus,
        dictionary=dictionary,
        coherence='c_v'
    )
    return coherence_model.get_coherence()


def main():
    config = {
        'model_name': 'sentence-transformers/all-mpnet-base-v2',
        'metric_distance': 'cosine',
        'calculate_probabilities': True,
        'reduce_frequent_words': True,
        'low_memory': False,
        'random_state': 42,
        'ngram_range': 2,
        'n_components': 5,
        'min_cluster_size': 150
    }

    df = pd.read_csv('data/topic0.csv')
    output_dir = 'data/topic_results'
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for topic_id in sorted(df['Topic_ID'].unique()):
        logger.info(f"Processing Topic_ID {topic_id}")
        subset = df[df['Topic_ID'] == topic_id]
        documents = subset['CombinedText'].astype(str).tolist()

        topic_model, topics = train_topic_model(documents, config)

        if not topics or all(t is None for t in topics):
            logger.warning(f"No topics found for Topic_ID {topic_id}, skipping.")
            continue

        coherence = evaluate_coherence(topic_model, topics, documents)
        logger.info(f"Coherence for Topic_ID {topic_id}: {coherence:.4f}")

        topic_info = topic_model.get_topic_info()
        topic_info['Topic_ID'] = topic_id
        topic_info['Coherence'] = coherence

        # Save model and info
        topic_model.save(os.path.join(output_dir, f'model_topic_{topic_id}'), serialization='safetensors', save_ctfidf=True)
        topic_info.to_csv(os.path.join(output_dir, f'topic_info_{topic_id}.csv'), index=False)
        results.append({'Topic_ID': topic_id, 'Num_Topics': len(topic_info) - 1, 'Coherence': coherence})

    pd.DataFrame(results).to_csv(os.path.join(output_dir, 'coherence_summary.csv'), index=False)
    logger.info("All topics processed and results saved.")


if __name__ == '__main__':
    main()
