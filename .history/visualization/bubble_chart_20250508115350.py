import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import logging

from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import pearsonr, shapiro, kendalltau

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv_files(file_paths):
    """
    Load multiple CSV files into a dictionary of DataFrames.

    Args:
        file_paths (dict): A dictionary mapping keys to file paths.

    Returns:
        dict: A dictionary mapping keys to loaded DataFrames.
    """
    return {key: pd.read_csv(path) for key, path in file_paths.items()}


def merge_dataframes(df1, df2, df3, key='category'):
    """
    Merge three DataFrames on a common key.

    Args:
        df1, df2, df3 (pd.DataFrame): DataFrames to be merged.
        key (str): Column to join on.

    Returns:
        pd.DataFrame: Merged DataFrame with selected columns.
    """
    merged = pd.merge(df1[[key, 'view_count']],
                      df2[[key, 'without_accepted_answer']], on=key)
    merged = pd.merge(merged, df3[[key, 'count']], on=key)
    return merged


def calculate_bubble_sizes(df, size_column='count', scale=8000):
    """
    Calculate bubble sizes scaled by a given factor.

    Args:
        df (pd.DataFrame): Data containing size values.
        size_column (str): Column name to scale.
        scale (float): Maximum size for scaling.

    Returns:
        pd.Series: Scaled sizes for bubble chart.
    """
    return (df[size_column] / df[size_column].max()) * scale


def draw_bubble_chart(df, x_col, y_col, size_col='count', color_col=None,
                      cmap_name='Spectral', norm=None, title=None, save_path=None):
    """
    Create a bubble chart with optional color mapping and saving.

    Args:
        df (pd.DataFrame): Data to plot.
        x_col, y_col (str): Columns for x and y axes.
        size_col (str): Column used to determine bubble size.
        color_col (str or None): Column used for color mapping.
        cmap_name (str): Name of matplotlib colormap.
        norm (Normalize or None): Normalization for color scale.
        title (str or None): Title for the plot.
        save_path (str or None): If set, saves the plot to this path.
    """
    plt.figure(figsize=(14, 10))
    sizes = calculate_bubble_sizes(df, size_col)

    scatter = plt.scatter(
        df[x_col], df[y_col],
        s=sizes,
        c=df[color_col] if color_col else sizes,
        cmap=cmap_name,
        norm=norm,
        alpha=0.7,
        edgecolors="w",
        linewidth=0.5
    )

    # Draw reference lines at average values
    avg_x = df[x_col].mean()
    avg_y = df[y_col].mean()
    plt.axhline(avg_y, color='red', linestyle='--', linewidth=1)
    plt.axvline(avg_x, color='red', linestyle='--', linewidth=1)

    # Annotate averages
    plt.text(plt.xlim()[1] * 0.99, avg_y, 'Average', color='red', va='center', ha='left', fontsize=10)
    plt.text(avg_x, plt.ylim()[1] * 0.99, 'Average', color='red', va='bottom', ha='center', fontsize=10)

    plt.xlabel('Difficulty')
    plt.ylabel('Popularity')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Add colorbar if color_col is provided
    cbar = plt.colorbar(scatter, ax=plt.gca(), pad=0.07)
    if color_col:
        cbar.set_label('Survey Responses (%)')

    if title:
        plt.title(title)

    if save_path:
        plt.savefig(save_path)

    plt.show()


def analyze_correlations(df, x_col, y_col):
    """
    Compute and log Pearson correlation, Shapiro-Wilk normality test,
    and Kendall tau rank correlation.

    Args:
        df (pd.DataFrame): Data for analysis.
        x_col, y_col (str): Columns to analyze.
    """
    # Pearson correlation
    r, p_r = pearsonr(df[x_col], df[y_col])
    logger.info(f"[Pearson] r = {r:.3f}, p = {p_r:.3f}")

    # Shapiro-Wilk test for normality
    stat_x, p_x = shapiro(df[x_col])
    stat_y, p_y = shapiro(df[y_col])
    logger.info(f"[Shapiro] {x_col}: stat = {stat_x:.3f}, p = {p_x:.3f}")
    logger.info(f"[Shapiro] {y_col}: stat = {stat_y:.3f}, p = {p_y:.3f}")

    # Kendall Tau correlation
    tau, p_tau = kendalltau(df[x_col], df[y_col])
    logger.info(f"[Kendall Tau] τ = {tau:.3f}, p = {p_tau:.3f}")


def main():
    """
    Main function that executes the full analysis pipeline:
    - Loads data
    - Merges data
    - Draws bubble chart
    - Logs statistical correlations
    """
    # File paths
    file_paths = {
        'csv1': 'results/data/average_view_step3.csv',
        'csv2': 'results/data/no_accepted_answers_step3.csv',
        'csv3': 'results/data/count_of_each_topic_step3.csv',
    }

    # Load and merge data
    data = load_csv_files(file_paths)
    merged_df = merge_dataframes(data['csv1'], data['csv2'], data['csv3'], key='category')

    # Optional normalization for color mapping
    norm = Normalize(vmin=26.5, vmax=46.9)

    # Generate bubble chart
    draw_bubble_chart(
        df=merged_df,
        x_col='without_accepted_answer',
        y_col='view_count',
        size_col='count',
        color_col=None,  # set to a column name for color mapping if desired
        cmap_name='Spectral',
        norm=norm,
        title='Ruby Topic Popularity vs Difficulty',
        save_path='bubble_chart_step3.pdf'
    )

    # Perform correlation analysis
    analyze_correlations(merged_df, 'without_accepted_answer', 'view_count')


if __name__ == '__main__':
    main()
