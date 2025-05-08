from utils.common import logger

def main():
    import pandas as pd
    from tqdm import tqdm
    import matplotlib.pyplot as plt

    df = pd.read_csv('survey/survey_data.csv')

    # filter_values = ["Less than a year", "Between one and two years", "More than ten years", "Between six and ten years"]
    # filter_values = ["Less than a year", "Between one and two years"]
    # filter_values = ["More than ten years", "Between six and ten years"]
    # filter_values = ["More than ten years"]




    filtered_df = df[df.iloc[:, 25].isin(filter_values)]
    logger.info(len(filtered_df))

    filtered_df.to_csv('survey/expert.csv', index=False)
    df = pd.read_csv('survey/novice.csv')

    category = df.iloc[-1, 26:61]
    logger.info(category)

    columns = ['Q9_{}'.format(i) for i in range(1, 36)]

    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

    data = []

    for idx, col in tqdm(enumerate(columns), total=len(columns)):
        filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
        rating_counts = filtered_data.value_counts().sort_index()

        count_1 = rating_counts.get(1, 0)
        count_2 = rating_counts.get(2, 0)
        count_3 = rating_counts.get(3, 0)
        count_4 = rating_counts.get(4, 0)
        count_5 = rating_counts.get(5, 0)

        # average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

        data.append({
            'column': col,
            'description': category[idx],
            'norm_count_1': count_1,
            'norm_count_2': count_2,
            'norm_count_3': count_3,
            'norm_count_4': count_4,
            'norm_count_5': count_5,
            # 'average': (average - 1) * 25,
        })

    df_data = pd.DataFrame(data)

    logger.info(df_data)


    df_grouped = df_data.groupby('description').agg({
        'norm_count_1': 'sum',
        'norm_count_2': 'sum',
        'norm_count_3': 'sum',
        'norm_count_4': 'sum',
        'norm_count_5': 'sum',
        # 'average': 'mean'
    }).reset_index()

    logger.info(df_grouped)



if __name__ == '__main__':
    main()