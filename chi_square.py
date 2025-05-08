import numpy as np
from scipy.stats import chisquare

# Define topics
topics = [
    "Application Quality and Security", 
    "Core Ruby Concepts", 
    "Data Management and Processing", 
    "Development Environment and Infrastructure", 
    "Software Architecture and Performance", 
    "Web Application Development"
]

# Observed and expected frequencies (raw counts)
observed_data = [
    [18528, 8726, 7820, 6290, 25553],  # Topic 1 Stack Overflow data
    [20121, 6465, 4869, 3305, 6272],
    [15670, 8084, 7418, 5879, 20833],
    [8174, 3967, 4016, 3681, 19624],
    [1784, 1008, 950, 803, 2922],
    [19229, 9512, 8569, 7082, 30781]
]

expected_data = [
    [80, 172, 163, 110, 36],  # Topic 1 Survey data
    [69, 113, 125, 79, 38],
    [104, 169, 174, 125, 42],
    [103, 161, 213, 128, 43],
    [28, 52, 73, 35, 29],
    [186, 305, 336, 220, 68]
]

# Loop over each topic and perform Chi-squared test
for i, topic in enumerate(topics):
    observed_frequencies = np.array(observed_data[i])
    expected_frequencies = np.array(expected_data[i])

    # Scale expected frequencies to match the total of observed frequencies
    scaling_factor = observed_frequencies.sum() / expected_frequencies.sum()
    expected_frequencies = expected_frequencies * scaling_factor

    # Perform Chi-squared test
    chi2_stat, p_value = chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)
    
    print(f"\n{topic}:")
    print(f"Chi-squared Statistic: {chi2_stat}")
    print(f"P-value: {p_value}")

    if p_value < 0.05:
        print("The distributions are significantly different for this topic.")
    else:
        print("No significant difference between the distributions for this topic.")
