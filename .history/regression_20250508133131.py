# regression_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor


def clean_descriptions(raw_descriptions):
    return [desc.split('-')[-1].strip() if isinstance(desc, str) and '-' in desc else '' for desc in raw_descriptions]


def compute_scaled_average_rating(df, columns, descriptions):
    data = []
    for idx, col in tqdm(enumerate(columns), total=len(columns)):
        filtered_data = df[col][(df[col] >= 1) & (df[col] <= 5)]
        rating_counts = filtered_data.value_counts().sort_index()

        average = sum(rating_counts.get(i, 0) * i for i in range(1, 6)) / len(filtered_data)

        data.append({
            'column': col,
            'description': descriptions[idx],
            'average': (average - 1) * 25,
        })
    return pd.DataFrame(data)


def standardize_and_regress(df):
    scaler = StandardScaler()
    X = scaler.fit_transform(df[['without_accepted_answer', 'response_time']])
    y = scaler.fit_transform(df[['average']]).ravel()

    model = LinearRegression()
    model.fit(X, y)

    # VIF calculation
    vif_data = pd.DataFrame({
        "Variable": ['No Accepted Answers', 'Median Response Time'],
        "VIF": [variance_inflation_factor(X, i) for i in range(X.shape[1])]
    })

    return model, model.score(X, y), vif_data


def plot_multivariate_regression(df, model):
    X = StandardScaler().fit_transform(df[['without_accepted_answer', 'response_time']])
    y = StandardScaler().fit_transform(df[['average']]).ravel()
    y_pred = model.predict(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c='blue', label='Data Points')
    plt.plot(X[:, 0], y_pred, 'r.', label='Fit Line')
    plt.title('Standardized Difficulty Measure vs Inputs')
    plt.xlabel('Standardized No Accepted Answers')
    plt.ylabel('Standardized Median Response Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def logarithmic(x, a, b):
    return a * np.log(b * x)


def plot_logarithmic_fit(x, y, params):
    a, b = params
    x_vals = np.linspace(min(x), max(x), 100)
    y_vals = logarithmic(x_vals, a, b)

    plt.figure(figsize=(12, 8))
    plt.scatter(x, y, color='blue', label='Data Points')
    plt.plot(x_vals, y_vals, color='red', label=f'Logarithmic Fit: y = {a:.2f} * log({b:.2f} * x)')
    plt.title('Difficulty vs Median Time with Logarithmic Fit')
    plt.xlabel('Difficulty Measure (%)')
    plt.ylabel('Median Time (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    survey_df = pd.read_csv('survey/survey_data.csv')
    so_df = pd.read_csv('results/data/no_accepted_answers_step1.csv')
    time_df = pd.read_csv('results/data/median_response_time_step1.csv')

    columns = [f'Q9_{i}' for i in range(1, 36)]
    raw_descriptions = survey_df.iloc[0, 26:61].tolist()
    descriptions = clean_descriptions(raw_descriptions)

    survey_df[columns] = survey_df[columns].apply(pd.to_numeric, errors='coerce')
    data_df = compute_scaled_average_rating(survey_df, columns, descriptions)

    merged = data_df.merge(so_df, left_on='description', right_on='topic_name')
    merged = merged.merge(time_df[['topic_name', 'response_time']], left_on='description', right_on='topic_name', how='left')

    model, r_squared, vif = standardize_and_regress(merged)
    print("Multiple Regression Results:")
    print(f"Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print(f"R^2: {r_squared}")
    print("\nVIF Data:")
    print(vif)

    plot_multivariate_regression(merged, model)

    # Logarithmic regression
    x = merged['average'].values
    y = merged['without_accepted_answer'].values
    params_log, _ = curve_fit(logarithmic, x, y)
    print("\nLogarithmic Regression Parameters:", params_log)
    plot_logarithmic_fit(x, y, params_log)


if __name__ == '__main__':
    main()
