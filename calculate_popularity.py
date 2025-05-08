import pandas as pd


input_file = 'results/data/final_category.csv'
data = pd.read_csv(input_file)

numeric_mask = pd.to_numeric(data['Score'], errors='coerce').notna()
filtered_data = data[numeric_mask].copy()
filtered_data['Score'] = pd.to_numeric(filtered_data['Score'])
average_views = filtered_data.groupby('category')['Score'].mean().reset_index()


output_file = 'results/data/average_score_step3.csv'
average_views.to_csv(output_file, index=False)

print(f"The average number of views per topic has been saved to {output_file}")


# import pandas as pd


# input_file = 'results/data/final_category.csv'
# data = pd.read_csv(input_file)


# average_views = data['ViewCount'].mean()


# print(f"The average number of views per topic has been saved to {average_views}")