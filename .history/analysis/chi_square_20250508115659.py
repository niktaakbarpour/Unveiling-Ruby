import numpy as np
from scipy.stats import chisquare
from utils.common import logger

# Placeholder for data file (if later extended to read from file)
INPUT_FILE = 'path/to/your/input.csv'  # TODO: Replace with actual path if needed

# Define the topic names
TOPICS = [
    "Application Quality and Security",
    "Core Ruby Concepts",
    "Data Management and Processing",
    "Development Environment and Infrastructure",
    "Software Architecture and Performance",
    "Web Application Development"
]

# Observed and expected frequency data for each topic
OBSERVED_DATA = [
    [18528, 8726, 7820, 6290, 25553],
    [20121, 6465, 4869, 3305, 6272],
    [15670, 8084, 7418, 5879, 20833],
    [8174, 3967, 4016, 3681, 19624],
    [1784, 1008, 950, 803, 2922],
    [19229, 9512, 8569, 7082, 30781]
]

EXPECTED_DATA = [
    [80, 172, 163, 110, 36],
    [69, 113, 125, 79, 38],
    [104, 169, 174, 125, 42],
    [103, 161, 213, 128, 43],
    [28, 52, 73, 35, 29],
    [186, 305, 336, 220, 68]
]


def perform_chi_squared_test(observed, expected):
    """
    Perform chi-squared test on observed and expected frequency arrays.

    Args:
        observed (np.array): Observed frequencies.
        expected (np.array): Expected frequencies.

    Returns:
        tuple: chi-squared statistic and p-value.
    """
    scaling_factor = observed.sum() / expected.sum()
    expected_scaled = expected * scaling_factor
    return chisquare(f_obs=observed, f_exp=expected_scaled)


def analyze_topic_distributions(topics, observed_data, expected_data):
    """
    Loop through each topic and run a chi-squared test to compare distributions.

    Args:
        topics (list): List of topic names.
        observed_data (list): Observed frequencies for each topic.
        expected_data (list): Expected frequencies for each topic.
    """
    for i, topic in enumerate(topics):
        observed = np.array(observed_data[i])
        expected = np.array(expected_data[i])
        chi2_stat, p_value = perform_chi_squared_test(observed, expected)

        logger.info(f"\n{topic}:")
        logger.info(f"Chi-squared Statistic: {chi2_stat:.3f}")
        logger.info(f"P-value: {p_value:.4f}")

        if p_value < 0.05:
            logger.info("The distributions are significantly different for this topic.")
        else:
            logger.info("No significant difference between the distributions for this topic.")


def main():
    analyze_topic_distributions(TOPICS, OBSERVED_DATA, EXPECTED_DATA)


if __name__ == '__main__':
    main()
