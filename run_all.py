"""
Minimal Runner Script for Unveiling Ruby
Reproduces main analysis and figures as used in the EASE 2025 paper.
"""

import os

def run(script):
    print(f"Running: {script}")
    os.system(f"python {script}")

# Data Preprocessing
run("data_preprocessing/gather_dataset.py")
run("data_preprocessing/handle_data.py")

# Topic Modeling and Tag Counting
run("utils/topic_modeling.py")
run("utils/count_topics.py")

# Statistical Analysis
run("analysis/calculate_difficulty.py")
run("analysis/calculate_popularity.py")
run("analysis/survey_vs_so.py")

# Visualizations
run("visualization/heat_map.py")
run("visualization/violin_plot.py")
run("visualization/line_chart.py")

print("\n✅ Minimal pipeline completed. Output files and figures should be available in the respective folders.")
