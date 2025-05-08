from utils.common import logger

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable


def load_data(file_path='results/data/final_category.csv'):
    df = pd.read_csv(file_path, low_memory=False)
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], errors='coerce', infer_datetime_format=True)
    df = df.dropna(subset=['CreationDate'])
    df['Year'] = df['CreationDate'].dt.year
    return df


def generate_heatmap(df, index_column, output_file, figsize=(14, 9), title=None):
    pivot_table = df.pivot_table(index=index_column, columns='Year', aggfunc='size', fill_value=0)
    pivot_table = pivot_table.sort_index()

    fig, ax = plt.subplots(figsize=figsize)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    sns.heatmap(
        pivot_table,
        cmap='Oranges',
        annot=True,
        fmt='d',
        linewidths=.5,
        square=True,
        ax=ax,
        cbar_ax=cax
    )

    logger.info(f"Total per year for {index_column}:\n{pivot_table.sum()}")
    plt.xlabel('Year')
    plt.ylabel(index_column.replace('_', ' ').title())
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    if title:
        plt.title(title)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def generate_individual_topic_heatmaps(df, output_dir='results/heatmap_step1', figsize=(9, 0.2)):
    os.makedirs(output_dir, exist_ok=True)
    pivot_table = df.pivot_table(index='topic_name', columns='Year', aggfunc='size', fill_value=0)

    for topic in pivot_table.index:
        plt.figure(figsize=figsize)
        ax = sns.heatmap(
            pivot_table.loc[[topic]],
            annot=False,
            fmt="d",
            cmap='Oranges',
            cbar=False,
            xticklabels=False,
            yticklabels=False
        )
        plt.axis('off')
        safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic])
        plt.savefig(f'{output_dir}/{safe_topic_name}_heatmap_step1.pdf', bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()


def main():
    df = load_data()

    # Generate overall heatmaps
    generate_heatmap(df, index_column='topic_name', output_file='results/heat_map_step1.png')
    generate_heatmap(df, index_column='middle_category', output_file='results/heat_map_step2.png')
    generate_heatmap(df, index_column='category', output_file='results/heat_map_step3.png')

    # Generate individual heatmaps for each topic
    generate_individual_topic_heatmaps(df)


if __name__ == '__main__':
    main()
