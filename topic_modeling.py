from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from umap import UMAP
import pandas as pd

print("after import")

path_dataset = 'data/deduplicated_data2.csv'
print("path_dataset")
df = pd.read_csv(path_dataset)
print("dataset loaded!!\n")
documents = df['CombinedText'].tolist()
print("dataset to list")
model_name = '/scratch/st-fhendija-1/nikta/unveiling-ruby/model'
print("model name")
embedding_model = SentenceTransformer(model_name)
print("model loaded\n")
umap_model = UMAP(n_components=5, n_neighbors=15, min_dist=0.0, metric='cosine')
print("after UMAP")
topic_model = BERTopic(embedding_model=embedding_model, umap_model=umap_model, hdbscan_model=HDBSCAN(min_cluster_size=1000), verbose=True)
print("topic model")
topics, _ = topic_model.fit_transform(documents)
print("after fit transform")
topic_info = topic_model.get_topic_info()
print("getting info")
topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])

output_file = 'data/topic_info.csv'
topic_df.to_csv(output_file, index=False)

print("finished")