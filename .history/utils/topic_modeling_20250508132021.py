from utils.common import logger
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from umap import UMAP

def main():
    import pandas as pd

    # Paths
    input_path = 'data/deduplicated_data2.csv'
    output_path = 'data/topic_info.csv'
    model_name = '/scratch/st-fhendija-1/nikta/unveiling-ruby/model'

    logger.info("Loading dataset...")
    df = pd.read_csv(input_path)
    documents = df['CombinedText'].astype(str).tolist()
    logger.info(f"Loaded {len(documents)} documents.")

    logger.info("Loading embedding model...")
    embedding_model = SentenceTransformer(model_name)

    logger.info("Setting up UMAP and HDBSCAN...")
    umap_model = UMAP(n_components=5, n_neighbors=15, min_dist=0.0, metric='cosine')
    hdbscan_model = HDBSCAN(min_cluster_size=1000)

    logger.info("Initializing BERTopic...")
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        verbose=True
    )

    logger.info("Fitting topic model...")
    topics, _ = topic_model.fit_transform(documents)

    logger.info("Extracting topic information...")
    topic_info = topic_model.get_topic_info()
    topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])

    topic_df.to_csv(output_path, index=False)
    logger.info(f"Saved topic info to {output_path}")

if __name__ == '__main__':
    main()
