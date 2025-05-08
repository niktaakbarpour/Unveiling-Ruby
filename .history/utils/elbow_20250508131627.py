from utils.common import logger
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle
import gc
import cuml


def load_embeddings(path):
    """
    Loads precomputed embedding vectors from a .npy file.
    """
    embeddings = np.load(path)
    logger.info(f"✅ Loaded {len(embeddings)} embeddings from '{path}'")
    return embeddings


def train_kmeans_models(embeddings, ks):
    """
    Trains KMeans models using cuML for each k in ks.
    """
    models = []
    for k in tqdm(ks, desc="Training KMeans models"):
        gc.collect()
        model = cuml.KMeans(n_clusters=k, random_state=0)
        model.fit(embeddings)
        models.append(model)
        logger.info(f"Trained KMeans for k={k}")
    return models


def save_models(models, output_path):
    """
    Saves a list of models to a pickle file.
    """
    with open(output_path, 'wb') as f:
        pickle.dump(models, f)
    logger.info(f"✅ Saved {len(models)} models to '{output_path}'")


def main():
    # === Config ===
    embedding_path = '../stack_overflow_embeddings.npy'
    output_path = 'elbow_models_1_to_150_2.pkl'
    k_range = list(range(1, 151))  # 1 to 150 inclusive

    # === Load data ===
    embeddings = load_embeddings(embedding_path)

    # === Train models ===
    models = train_kmeans_models(embeddings, ks=k_range)

    # === Save results ===
    save_models(models, output_path)


if __name__ == '__main__':
    main()
