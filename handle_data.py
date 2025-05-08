import pandas as pd

path_dataset = './results/data/deduplicated_data2.csv'
df = pd.read_csv(path_dataset)

nan_indices = df[df['CombinedText'].isna()].index
non_string_indices = df[~df['CombinedText'].apply(lambda x: isinstance(x, str))].index

print("Indices of rows with NaN values in 'CombinedText' column:", nan_indices)
print("Indices of rows with non-string values in 'CombinedText' column:", non_string_indices)
