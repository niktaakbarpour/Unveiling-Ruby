from utils.common import logger

def main():
    import pandas as pd
    import os

    from sklearn.feature_extraction.text import CountVectorizer
    from bertopic.vectorizers import ClassTfidfTransformer
    from sentence_transformers import SentenceTransformer
    from umap import UMAP
    from hdbscan import HDBSCAN
    from bertopic.representation import KeyBERTInspired
    from bertopic import BERTopic
    from gensim.models.coherencemodel import CoherenceModel
    import gensim.corpora as corpora

    logger.info("after import")

    path_dataset = 'data/topic0.csv'
    path_model = 'data/model'

    logger.info("after dataset")

    config_defaults = {
        'model_name': '/scratch/st-fhendija-1/nikta/unveiling-ruby/model',
        'metric_distane': 'cosine',
        'calculate_probabilities': True,
        'reduce_frequent_words': True,
        'low_memory': False,
        'random_state': 42,
        'ngram_range': 2,
        'n_components': 5  # Set the best known value for n_components
    }

    logger.info("after defaults")

    class TopicModeling:
        logger.info("I am in class")
        def __init__(self, column, documents):
            self.top_models = []
            self.path_model = path_model

            self.column = column
            self.documents = documents

        logger.info("after init")

        def train(self, min_cluster_sizes):
            result_data = []
            for min_cluster_size in min_cluster_sizes:
                logger.info(f"Training with min_cluster_size: {min_cluster_size}")
                config_defaults['min_cluster_size'] = min_cluster_size
                embedding_model = SentenceTransformer(config_defaults['model_name'])
                umap_model = UMAP(n_components=config_defaults['n_components'],
                                  metric=config_defaults['metric_distane'],
                                  random_state=config_defaults['random_state'],
                                  low_memory=config_defaults['low_memory'])
                hdbscan_model = HDBSCAN(min_cluster_size=config_defaults['min_cluster_size'],
                                        min_samples=1,
                                        prediction_data=config_defaults['calculate_probabilities'])
                vectorizer_model = CountVectorizer(ngram_range=(1, config_defaults['ngram_range']), stop_words='english')
                ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=config_defaults['reduce_frequent_words'])
                representation_model = KeyBERTInspired()
                topic_model = BERTopic(embedding_model=embedding_model,
                                       umap_model=umap_model,
                                       hdbscan_model=hdbscan_model,
                                       vectorizer_model=vectorizer_model,
                                       ctfidf_model=ctfidf_model,
                                       representation_model=representation_model,
                                       n_gram_range=(1, config_defaults['ngram_range']),
                                       calculate_probabilities=config_defaults['calculate_probabilities'],
                                       nr_topics="auto")
                topics, _ = topic_model.fit_transform(self.documents)
                if not topics or not topics[0]:
                    logger.info("No topics found or topics list is empty.")
                    continue

                documents = pd.DataFrame({
                    "Document": self.documents,
                    "ID": range(len(self.documents)),
                    "Topic": topics
                })
                documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
                cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)
                vectorizer = topic_model.vectorizer_model
                analyzer = vectorizer.build_analyzer()
                tokens = [analyzer(doc) for doc in cleaned_docs]
                dictionary = corpora.Dictionary(tokens)
                corpus = [dictionary.doc2bow(token) for token in tokens]

                topic_words = [[words for words, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics))-1)]

                coherence_umass = CoherenceModel(
                        topics=topic_words,
                        texts=tokens,
                        corpus=corpus,
                        dictionary=dictionary,
                        coherence='u_mass'
                    )

                coherence_umass = coherence_umass.get_coherence()
                logger.info(f"Training completed with min_cluster_size: {min_cluster_size}, Number of Topics: {len(set(topics))-1}, Coherence Score: {coherence_umass}")  

                result_data.append({'min_cluster_size': min_cluster_size, 'num_topics': len(set(topics))-1, 'coherence_score': coherence_umass})

            # Saving the results to a CSV file
            result_df = pd.DataFrame(result_data)
            result_df.to_csv('data/plot.csv', index=False)

    if __name__ == "__main__":
        df = pd.read_csv(path_dataset)
        column = 'CombinedText'
        documents = df[column].tolist()

        filtered_df = df[df['Topic_ID'] == 0]
        filtered_documents = filtered_df[column].tolist()

        min_cluster_sizes = [150]
        tm = TopicModeling(column, filtered_documents)
        tm.train(min_cluster_sizes)                                        


    import pandas as pd
    import os

    from sklearn.feature_extraction.text import CountVectorizer
    from bertopic.vectorizers import ClassTfidfTransformer
    from sentence_transformers import SentenceTransformer
    from umap import UMAP
    from hdbscan import HDBSCAN
    from bertopic.representation import KeyBERTInspired
    from bertopic import BERTopic
    import gensim.corpora as corpora

    logger.info("after import")

    # path_dataset = 'data/deduplicated_data2.csv'
    # path_model = 'data/model'
    # output_file = 'data/rr8.csv'

    logger.info("after dataset")

    # config_defaults = {
    #     'model_name': '/scratch/st-fhendija-1/nikta/unveiling-ruby/model',
    #     'metric_distane': 'cosine',
    #     'calculate_probabilities': True,
    #     'reduce_frequent_words': True,
    #     'low_memory': False,
    #     'min_cluster_size': 650,
    #     'random_state': 42,
    #     'ngram_range': 2,  
    'n_components': 5  # Set the best known value for n_components
    # }

    logger.info("after defaults")

    # class TopicModeling:
    logger.info("I am in class")
    #     def __init__(self, column, df):
    #         self.top_models = []
    #         self.path_model = path_model

    #         self.column = column
    #         self.df = df

    logger.info("after init")

    #     def train(self):
    logger.info("in train")
    embedding_model = SentenceTransformer(config_defaults['model_name'])
    logger.info("embedding model")
    #         umap_model = UMAP(n_components=config_defaults['n_components'],
    #                           metric=config_defaults['metric_distane'],
    #                           random_state=config_defaults['random_state'],
    #                           low_memory=config_defaults['low_memory'])
    logger.info("umap model")
    #         hdbscan_model = HDBSCAN(min_cluster_size=config_defaults['min_cluster_size'],
    #                                 min_samples=1,
    #                                 prediction_data=config_defaults['calculate_probabilities'])
    logger.info("hdbscan model")

    #         vectorizer_model = CountVectorizer(ngram_range=(1, config_defaults['ngram_range']), stop_words='english')
    logger.info("after vectorizer model")

    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=config_defaults['reduce_frequent_words'])
    logger.info("after ctfidf")
    #         representation_model = KeyBERTInspired()
    logger.info("keybert inspired")
    #         topic_model = BERTopic(embedding_model=embedding_model,
    #                                umap_model=umap_model,
    #                                hdbscan_model=hdbscan_model,
    #                                vectorizer_model=vectorizer_model,
    #                                ctfidf_model=ctfidf_model,
    #                                representation_model=representation_model,
    #                                n_gram_range=(1, config_defaults['ngram_range']),
    #                                calculate_probabilities=config_defaults['calculate_probabilities'],
    #                                nr_topics="auto")
    logger.info("topic model")
    #         documents = self.df[self.column].tolist()  # Extract the document column from the DataFrame
    topics, _ = topic_model.fit_transform(documents)
    logger.info("fit transform")
    if not topics or not topics[0]:  # Check if the topics list is empty or the first element is empty
    logger.info("No topics found or topics list is empty.")
    #             return

    # Get document information
    #         document_info = topic_model.get_document_info(documents)
    logger.info("Document info:")
    logger.info(document_info)
    logger.info("Type of document_info:", type(document_info))

    #         # Create a DataFrame to hold the results
    result_df = pd.DataFrame(columns=['ID', 'Title', 'Body', 'Topic_ID', 'Topic_Name', 'Probability', 'Top_n_words'])

    # Iterate over each row in document_info to extract information
    for index, row in document_info.iterrows():
    #             document_id = index  # Use the index as the document ID
    #             topic_id = row['Topic']
    #             topic_name = row['Name']
    #             probability = row['Probability']
    #             top_n_words = row['Top_n_words']

    #             # Find the corresponding document in the input DataFrame
    document_row = self.df.iloc[index]

    #             # Extract ID, Title, and Body from the document_row
    #             document_id = document_row['Id']
    #             title = document_row['Title']
    #             body = document_row['Body']

    # Append the information to result_df
    result_df = pd.concat([result_df, pd.DataFrame({'ID': [document_id], 'Title': [title], 'Body': [body],
    #                                           'Topic_ID': [topic_id], 'Topic_Name': [topic_name],
    #                                           'Probability': [probability], 'Top_n_words': [top_n_words]})], ignore_index=True)

    #         # Sort the DataFrame by Topic_ID and Probability
    result_df = result_df.sort_values(by=['Topic_ID', 'Probability'], ascending=[True, False])

    #         # Save the output to a CSV file
    result_df.to_csv(output_file, index=False)
    logger.info("Output saved to:", output_file)

    if __name__ == "__main__":
    df = pd.read_csv(path_dataset)

    #     tm = TopicModeling('CombinedText', df)
    #     tm.train()


    import pandas as pd
    import os

    from sklearn.feature_extraction.text import CountVectorizer
    from bertopic.vectorizers import ClassTfidfTransformer
    from sentence_transformers import SentenceTransformer
    from umap import UMAP
    from hdbscan import HDBSCAN
    from bertopic.representation import KeyBERTInspired
    from bertopic import BERTopic
    from gensim.models.coherencemodel import CoherenceModel
    import gensim.corpora as corpora

    logger.info("after import")

    # path_dataset = 'data/deduplicated_data2.csv'
    # path_model = 'data/model'

    logger.info("after dataset")

    # config_defaults = {
    #     'model_name': '/scratch/st-fhendija-1/nikta/unveiling-ruby/model',
    #     'metric_distane': 'cosine',
    #     'calculate_probabilities': True,
    #     'reduce_frequent_words': True,
    #     'low_memory': False,
    #     'min_cluster_size': 500,
    #     'random_state': 42,
    #     'ngram_range': 2,
    'n_components': 5  # Set the best known value for n_components
    # }

    logger.info("after defaults")

    # class TopicModeling:
    logger.info("I am in class")
    #     def __init__(self, column, documents):
    #         self.top_models = []
    #         self.path_model = path_model

    #         self.column = column
    #         self.documents = documents

    logger.info("after init")

    #     def train(self):
    logger.info("in train")
    embedding_model = SentenceTransformer(config_defaults['model_name'])
    logger.info("embedding model")
    #         umap_model = UMAP(n_components=config_defaults['n_components'],
    #                           metric=config_defaults['metric_distane'],
    #                           random_state=config_defaults['random_state'],
    #                           low_memory=config_defaults['low_memory'])
    logger.info("umap model")
    #         hdbscan_model = HDBSCAN(min_cluster_size=config_defaults['min_cluster_size'],
    #                                 min_samples=1,
    #                                 prediction_data=config_defaults['calculate_probabilities'])
    logger.info("hdbscan model")

    #         vectorizer_model = CountVectorizer(ngram_range=(1, config_defaults['ngram_range']), stop_words='english')
    logger.info("after vectorizer model")

    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=config_defaults['reduce_frequent_words'])
    logger.info("after ctfidf")
    #         representation_model = KeyBERTInspired()
    logger.info("keybert inspired")
    #         topic_model = BERTopic(embedding_model=embedding_model,
    #                                umap_model=umap_model,
    #                                hdbscan_model=hdbscan_model,
    #                                vectorizer_model=vectorizer_model,
    #                                ctfidf_model=ctfidf_model,
    #                                representation_model=representation_model,
    #                                n_gram_range=(1, config_defaults['ngram_range']),
    #                                calculate_probabilities=config_defaults['calculate_probabilities'],
    #                                nr_topics="auto")
    logger.info("topic model")
    topics, _ = topic_model.fit_transform(self.documents)
    logger.info("fit transform")
    if not topics or not topics[0]:  # Check if the topics list is empty or the first element is empty
    logger.info("No topics found or topics list is empty.")
    #             return

    documents = pd.DataFrame({
    #             "Document": self.documents,
    #             "ID": range(len(self.documents)),
    #             "Topic": topics
    #         })
    logger.info("documents")
    #         documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
    logger.info("documents per topic")
    #         cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)
    logger.info("cleaned docs")
    #         vectorizer = topic_model.vectorizer_model
    logger.info("vectorizer")
    #         analyzer = vectorizer.build_analyzer()
    logger.info("analyzer")
    tokens = [analyzer(doc) for doc in cleaned_docs]
    #         dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
    logger.info("step 4")
    topic_words = [[words for words, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics))-1)]
    logger.info("step 5")
    #         coherence_umass = CoherenceModel(
    #                 topics=topic_words,
    #                 texts=tokens,
    #                 corpus=corpus,
    #                 dictionary=dictionary,
    #                 coherence='u_mass'
    #             )
    logger.info("coherence")

    #         coherence_umass = coherence_umass.get_coherence()
    logger.info("get coherence")
    #         topic_info = topic_model.get_topic_info()
    logger.info("getting info")
    topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])
    #         topic_df['Coherence'] = coherence_umass
    logger.info("topic df")
    #         output_file = 'data/topic_info1.csv'
    topic_df.to_csv(output_file, index=False)
    logger.info("finished")

    #         model_name = f'{self.column}'
    topic_model.save(os.path.join(self.path_model, model_name), serialization='safetensors', save_ctfidf=True)
    logger.info("saving")

    if __name__ == "__main__":
    df = pd.read_csv(path_dataset)
    #     column = 'CombinedText'
    #     documents = df[column].tolist()
        
    #     tm = TopicModeling(column, documents)
    #     tm.train()


    import pandas as pd
    import os

    from sklearn.feature_extraction.text import CountVectorizer
    from bertopic.vectorizers import ClassTfidfTransformer
    from sentence_transformers import SentenceTransformer
    from umap import UMAP
    from hdbscan import HDBSCAN
    from bertopic.representation import KeyBERTInspired
    from bertopic import BERTopic
    from gensim.models.coherencemodel import CoherenceModel
    import gensim.corpora as corpora

    # path_dataset = 'data/deduplicated_data2.csv'  # Path to your CSV file
    # path_model = 'data/model'  # Define the model path

    # Set default configuration for hyperparameters
    # config_defaults = {
    #     'model_name': '/scratch/st-fhendija-1/nikta/unveiling-ruby/model',
    #     'metric_distane': 'cosine',
    #     'calculate_probabilities': True,
    #     'reduce_frequent_words': True,
    #     'low_memory': False,
    #     'min_cluster_size': 500,
    #     'random_state': 42,
    #     'ngram_range': 2,
    'n_components': 5  # Set the best known value for n_components
    # }

    # class TopicModeling:
    #     def __init__(self, column, documents):
    #         self.top_models = []
    #         self.path_model = path_model

    #         self.column = column
    #         self.documents = documents

    #     def train(self):
    embedding_model = SentenceTransformer(config_defaults['model_name'])
    logger.info("embedding model")
    #         umap_model = UMAP(n_components=config_defaults['n_components'],
    #                           metric=config_defaults['metric_distane'],
    #                           random_state=config_defaults['random_state'],
    #                           low_memory=config_defaults['low_memory'])
    logger.info("umap model")
    #         hdbscan_model = HDBSCAN(min_cluster_size=config_defaults['min_cluster_size'],
    #                                 min_samples=1,
    #                                 prediction_data=config_defaults['calculate_probabilities'])
    logger.info("hdbscan model")

    #         vectorizer_model = CountVectorizer(ngram_range=(1, config_defaults['ngram_range']), stop_words='english')

    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=config_defaults['reduce_frequent_words'])
    #         representation_model = KeyBERTInspired()
    logger.info("keybert inspired")
    #         topic_model = BERTopic(embedding_model=embedding_model,
    #                                umap_model=umap_model,
    #                                hdbscan_model=hdbscan_model,
    #                                vectorizer_model=vectorizer_model,
    #                                ctfidf_model=ctfidf_model,
    #                                representation_model=representation_model,
    #                                n_gram_range=(1, config_defaults['ngram_range']),
    #                                calculate_probabilities=config_defaults['calculate_probabilities'],
    #                                nr_topics="auto")
    logger.info("topic model")
    topics, _ = topic_model.fit_transform(self.documents)
    logger.info("fit transform")
    if not topics or not topics[0]:  # Check if the topics list is empty or the first element is empty
    logger.info("No topics found or topics list is empty.")
    #             return

    documents = pd.DataFrame({
    #             "Document": self.documents,
    #             "ID": range(len(self.documents)),
    #             "Topic": topics
    #         })
    logger.info("documents")
    #         documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
    logger.info("documents per topic")
    #         cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)
    logger.info("cleaned docs")
    #         vectorizer = topic_model.vectorizer_model
    logger.info("vectorizer")
    #         analyzer = vectorizer.build_analyzer()
    logger.info("analyzer")
    #         # Step 4 - Tokenize topics
    tokens = [analyzer(doc) for doc in cleaned_docs]
    #         dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
    logger.info("step 4")
    #         # Step 5 - Create topic representation
    topic_words = [[words for words, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics))-1)]
    logger.info("step 5")
    #         coherence_cv = CoherenceModel(
    #             topics=topic_words,
    #             texts=tokens,
    #             corpus=corpus,
    #             dictionary=dictionary,
    #             coherence='c_v'
    #         )
    logger.info("coherence")

    #         coherence_cv = coherence_cv.get_coherence()
    # logger.info(topic_model.get_topic_info())
    # logger.info("Coherence CV:", coherence_cv)
    # logger.info("Topic Number:", topic_model.get_topic_info().shape[0] - 1)
    # logger.info("Uncategorized Post Number:", topic_model.get_topic_info().at[0, 'Count'])
    logger.info("get coherence")
    #         topic_info = topic_model.get_topic_info()
    logger.info("getting info")
    topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])
    #         topic_df['Coherence'] = coherence_cv
    logger.info("topic df")
    #         output_file = 'data/topic_info1.csv'
    topic_df.to_csv(output_file, index=False)
    logger.info("finished")

    #         model_name = f'{self.column}'
    topic_model.save(os.path.join(self.path_model, model_name), serialization='safetensors', save_ctfidf=True)
    logger.info("saving")

    import pandas as pd
    import os
    from sentence_transformers import SentenceTransformer
    from umap import UMAP
    from hdbscan import HDBSCAN
    from bertopic.representation import KeyBERTInspired
    from bertopic import BERTopic
    from gensim.models.coherencemodel import CoherenceModel
    import gensim.corpora as corpora

    # path_dataset = './results/data/test.csv'  # Path to your CSV file
    # path_model = './results/model'  # Define the model path

    # Set default configuration for hyperparameters
    # config_defaults = {
    'model_name': 'sentence-transformers/all-mpnet-base-v2',
    #     'metric_distane': 'cosine',
    #     'calculate_probabilities': True,
    #     'low_memory': False,
    #     'min_cluster_size': 20,
    #     'random_state': 42,
    #     'ngram_range': 2,
    'n_components': 5  # Set the best known value for n_components
    # }

    # class TopicModeling:
    #     def __init__(self, column, documents):
    #         self.top_models = []
    #         self.path_model = path_model
            
    #         self.column = column
    #         self.documents = documents
            
    #     def train(self):
    embedding_model = SentenceTransformer(config_defaults['model_name'])
    #         umap_model = UMAP(n_components=config_defaults['n_components'],
    #                           metric=config_defaults['metric_distane'],
    #                           random_state=config_defaults['random_state'],
    #                           low_memory=config_defaults['low_memory'])
    #         hdbscan_model = HDBSCAN(min_cluster_size=config_defaults['min_cluster_size'],
    #                                 min_samples=1,
    #                                 prediction_data=config_defaults['calculate_probabilities'])
    #         representation_model = KeyBERTInspired()

    #         topic_model = BERTopic(embedding_model=embedding_model,
    #                                umap_model=umap_model,
    #                                hdbscan_model=hdbscan_model,
    #                                representation_model=representation_model,
    #                                n_gram_range=(1, config_defaults['ngram_range']),
    #                                calculate_probabilities=config_defaults['calculate_probabilities'],
    #                                nr_topics=5)

    topics, _ = topic_model.fit_transform(self.documents)

    if not topics or not topics[0]:  # Check if the topics list is empty or the first element is empty
    logger.info("No topics found or topics list is empty.")
    #             return

    documents = pd.DataFrame({
    #             "Document": self.documents,
    #             "ID": range(len(self.documents)),
    #             "Topic": topics
    #         })
    #         documents_per_topic = documents.groupby(['Topic'], as_index=False).agg({'Document': ' '.join})
    #         cleaned_docs = topic_model._preprocess_text(documents_per_topic.Document.values)

    #         vectorizer = topic_model.vectorizer_model
    #         analyzer = vectorizer.build_analyzer()

    #         # Step 4 - Tokenize topics
    tokens = [analyzer(doc) for doc in cleaned_docs]
    #         dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
            
    #         # Step 5 - Create topic representation
    topic_words = [[words for words, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics))-1)]

    #         coherence_cv = CoherenceModel(
    #             topics=topic_words,
    #             texts=tokens,
    #             corpus=corpus,
    #             dictionary=dictionary,
    #             coherence='c_v'
    #         )

    #         coherence_cv = coherence_cv.get_coherence()
    # logger.info(topic_model.get_topic_info())
    # logger.info("Coherence CV:", coherence_cv)
    # logger.info("Topic Number:", topic_model.get_topic_info().shape[0] - 1)
    # logger.info("Uncategorized Post Number:", topic_model.get_topic_info().at[0, 'Count'])

    #         topic_info = topic_model.get_topic_info()
    logger.info("getting info")
    topic_df = pd.DataFrame(topic_info, columns=['Topic', 'Count', 'Name', 'Representation', 'Representative_Docs'])
    #         topic_df['Coherence'] = coherence_cv

    #         output_file = './results/data/topic_info2.csv'
    topic_df.to_csv(output_file, index=False)

    logger.info("finished")
            
    #         model_name = f'{self.column}'
    topic_model.save(os.path.join(self.path_model, model_name), serialization='safetensors', save_ctfidf=True)

    Load data from CSV and perform topic modeling
    if __name__ == "__main__":
    df = pd.read_csv(path_dataset)
    column = 'CombinedText'  # Define the column name for topic modeling
    #     documents = df[column].tolist()
        
    #     tm = TopicModeling(column, documents)
    #     tm.train()

if __name__ == '__main__':
    main()