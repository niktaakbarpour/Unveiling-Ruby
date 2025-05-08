import cuml
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle
import gc



path = os.path.join('../stack_overflow_embeddings.npy')
embeddings = np.load(path)

print(f"length of embeddings: {len(embeddings)}")



def elbow(embeddings, ks):
    models = []
    for k in tqdm(ks):
        gc.collect()
        model = cuml.KMeans(n_clusters=k, random_state=0)
        model.fit(embeddings)
        models.append(model)
    return models

start = 1
end = 150
step = 1
ks = list(range(start, end + 1, step))
#ks = [1] + ks
models = elbow(embeddings, ks=ks)

path = os.path.join('elbow_models_1_to_150_2.pkl')
with open(path, 'wb') as file:
    pickle.dump(models, file)
