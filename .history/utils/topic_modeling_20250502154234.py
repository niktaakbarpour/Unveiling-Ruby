from utils.common import logger

from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from umap import UMAP
def main():
    import pandas as pd

    logger.info("after import")

    path_dataset = 'data/deduplicated_data2.csv'
    logger.info("path_dataset")
    df = pd.read_csv(path_dataset)
    logger.info("dataset loaded!!\n")
    documents = df['CombinedText'].tolist()
    logger.info("dataset to list")
    model_name = '/scratch/st-fhendija-1/nikta/unveiling-ruby/model'
    logger.info("model name")
    embedding_model = SentenceTransformer(model_name)
    logger.info("model loaded\n")
    umap_model = UMAP(n_components=5, n_neighbors=15, min_dist=0.0, metric='cosine')
    logger.info("after UMAP")
    topic_model = BERTopic(embedding_model=embedding_model, umap_model=umap_model, hdbscan_model=HDBSCAN(min_cluster_size=1000), verbose=True)
    logger.info("topic model")
    topics, _ = topic_model.fit_transform(documents)
    logger.info("after fit transform")
    topic_info = topic_model.get_topic_info()
    logger.info("getting info")
    topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])

    output_file = 'data/topic_info.csv'
    topic_df.to_csv(output_file, index=False)

    logger.info("finished")

if __name__ == '__main__':
    main()