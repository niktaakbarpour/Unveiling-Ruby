import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from scipy.stats import linregress
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load the data
df = pd.read_csv('survey/survey_data.csv')
stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')
response_time_df = pd.read_csv('results/data/median_response_time_step1.csv')  # Add the path to your median response time CSV

# Prepare column names and descriptions
columns = ['Q9_{}'.format(i) for i in range(1, 36)]
descriptions = df.iloc[0, 26:61].tolist()

# Clean descriptions
cleaned_descriptions = []
for desc in descriptions:
    if isinstance(desc, str) and '-' in desc:
        cleaned_descriptions.append(desc.split('-')[-1].strip())
    else:
        cleaned_descriptions.append('')

# Convert the relevant columns to numeric values
df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# Process data for regression
data = []
for idx, col in tqdm(enumerate(columns), total=len(columns)):
    filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
    rating_counts = filtered_data.value_counts().sort_index()

    # Count ratings and calculate average
    count_1 = rating_counts.get(1, 0)
    count_2 = rating_counts.get(2, 0)
    count_3 = rating_counts.get(3, 0)
    count_4 = rating_counts.get(4, 0)
    count_5 = rating_counts.get(5, 0)

    average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

    data.append({
        'column': col,
        'description': cleaned_descriptions[idx],
        'norm_count_1': count_1,
        'norm_count_2': count_2,
        'norm_count_3': count_3,
        'norm_count_4': count_4,
        'norm_count_5': count_5,
        'average': (average - 1) * 25,  # Scale the average
    })

# Merge with Stack Overflow data
combined_df = pd.DataFrame(data).merge(stackoverflow_df, left_on='description', right_on='topic_name')

# Now merge with the median response time CSV
# Assuming 'category' in median_response_time.csv matches 'description' in combined_df
combined_df = combined_df.merge(response_time_df[['topic_name', 'response_time']], 
                                 left_on='description', right_on='topic_name', how='left')

# Extract relevant columns for analysis
categories = combined_df['description'].values  # Category names
difficulty_measures = combined_df['average'].values  # Difficulty measures
no_accepted_answers = combined_df['without_accepted_answer'].values  # Median times
median_response_times = combined_df['response_time'].values  # Median response times from the 3rd CSV

# --- Add standardization ---
# Initialize the scaler
scaler = StandardScaler()

# Standardize the features (difficulty_measures, no_accepted_answers, and median_response_times)
scaled_features = scaler.fit_transform(np.column_stack((difficulty_measures, no_accepted_answers, median_response_times)))

# Extract the standardized values
scaled_difficulty_measures = scaled_features[:, 0]
scaled_no_accepted_answers = scaled_features[:, 1]
scaled_median_response_times = scaled_features[:, 2]

# Perform multiple linear regression (using both difficulty measures, no accepted answers, and median response time)
from sklearn.linear_model import LinearRegression

# Create the regression model
regressor = LinearRegression()

# Prepare the independent variables and dependent variable
X = np.column_stack((scaled_no_accepted_answers, scaled_median_response_times))  # Independent variables
y = scaled_difficulty_measures  # Dependent variable

# Fit the model
regressor.fit(X, y)

# Output multiple regression results
print("Multiple Regression Results:")
print(f"Slope for 'No Accepted Answers': {regressor.coef_[0]}")
print(f"Slope for 'Median Response Time': {regressor.coef_[1]}")
print(f"Intercept: {regressor.intercept_}")
print(f"R-squared: {regressor.score(X, y)}")

# --- Check for Multicollinearity ---
# Calculate the VIF for each independent variable
vif_data = pd.DataFrame()
vif_data["Variable"] = ["No Accepted Answers", "Median Response Time"]
vif_data["VIF"] = [variance_inflation_factor(X, i) for i in range(X.shape[1])]

print("\nVIF Data:")
print(vif_data)

# ---- Scatter Plot ----
# Create a scatter plot of the standardized data
plt.figure(figsize=(8, 6))
plt.scatter(scaled_no_accepted_answers, scaled_median_response_times, color='blue', label='Data Points')

# Plot the regression line
plt.plot(scaled_no_accepted_answers, regressor.coef_[0] * scaled_no_accepted_answers + regressor.coef_[1] * scaled_median_response_times + regressor.intercept_, color='red', label='Fit Line')

# Customize the plot
plt.title('Standardized Difficulty Measure vs Standardized Median Response Time')
plt.xlabel('Standardized Difficulty Measure')
plt.ylabel('Standardized Median Response Time')
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()







# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.optimize import curve_fit
# from tqdm import tqdm

# # Load the data
# df = pd.read_csv('survey/survey_data.csv')
# stackoverflow_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')

# # Prepare column names and descriptions
# columns = ['Q9_{}'.format(i) for i in range(1, 36)]
# descriptions = df.iloc[0, 26:61].tolist()

# # Clean descriptions
# cleaned_descriptions = []
# for desc in descriptions:
#     if isinstance(desc, str) and '-' in desc:
#         cleaned_descriptions.append(desc.split('-')[-1].strip())
#     else:
#         cleaned_descriptions.append('')

# # Convert the relevant columns to numeric values
# df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# # Process data for regression
# data = []
# for idx, col in tqdm(enumerate(columns), total=len(columns)):
#     filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
#     rating_counts = filtered_data.value_counts().sort_index()

#     # Count ratings and calculate average
#     count_1 = rating_counts.get(1, 0)
#     count_2 = rating_counts.get(2, 0)
#     count_3 = rating_counts.get(3, 0)
#     count_4 = rating_counts.get(4, 0)
#     count_5 = rating_counts.get(5, 0)

#     average = (count_1 + (count_2 * 2) + (count_3 * 3) + (count_4 * 4) + (count_5 * 5)) / len(filtered_data)

#     data.append({
#         'column': col,
#         'description': cleaned_descriptions[idx],
#         'norm_count_1': count_1,
#         'norm_count_2': count_2,
#         'norm_count_3': count_3,
#         'norm_count_4': count_4,
#         'norm_count_5': count_5,
#         'average': (average - 1) * 25,  # Scale the average
#     })

# # Merge with Stack Overflow data
# combined_df = pd.DataFrame(data).merge(stackoverflow_df, left_on='description', right_on='topic_name')

# # Extract relevant columns for analysis
# categories = combined_df['description'].values  # Category names
# difficulty_measures = combined_df['average'].values  # Difficulty measures
# median_times = combined_df['without_accepted_answer'].values  # Median times

# # Logarithmic Regression Model
# def logarithmic(x, a, b):
#     return a * np.log(b * x)



# # Perform Logarithmic Regression
# params_log, _ = curve_fit(logarithmic, difficulty_measures, median_times)
# log_a, log_b = params_log


# # Output overall regression results for Logarithmic and Exponential models
# print("Logarithmic Regression Results:")
# print(f"Parameters: a = {log_a}, b = {log_b}")



# # Plotting
# plt.figure(figsize=(12, 8))

# # Scatter Plot
# plt.scatter(difficulty_measures, median_times, color='blue', label='Data Points')

# # Plot Logarithmic Fit
# x_vals = np.linspace(min(difficulty_measures), max(difficulty_measures), 100)
# y_log_vals = logarithmic(x_vals, *params_log)
# plt.plot(x_vals, y_log_vals, color='red', label=f'Logarithmic Fit: y = {log_a:.2f} * log({log_b:.2f} * x)')

# # Customize the plot
# plt.title('Difficulty Measure vs Median Time with Logarithmic and Exponential Fits')
# plt.xlabel('Difficulty Measure (%)')
# plt.ylabel('Median Time for Accepted Answer (%)')
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.tight_layout()
# plt.show()
