
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

try:
    from ml.generate_data import generate_insurance_data, download_insurance_data
except ImportError:
    from generate_data import generate_insurance_data, download_insurance_data

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent / "insurance.csv"
PLOT_PATH = ROOT / "robust_vs_ols.png"


def load_or_generate_data(path: Path) -> pd.DataFrame:
    if path.exists():
        print(f"Loaded {path}")
        return pd.read_csv(path)

    print(f"Warning: {path} not found. Downloading real insurance data from the web.")
    df = download_insurance_data(path)
    return df


def evaluate(model, X_test, y_test, name: str):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print(f"\n{name} Results:")
    print(f"  MAE: {mae:.2f}")
    print(f"  MSE: {mse:.2f}")
    print(f"  R²: {r2:.4f}")
    print(f"  MAPE: {mape:.4%}")
    print(f"  Coefficients: {model.coef_}")
    print(f"  Intercept: {model.intercept_:.2f}")
    return y_pred


def main():
    df = load_or_generate_data(DATA_PATH)

    df = df.rename(columns={
        'age': 'Age',
        'sex': 'Sex',
        'bmi': 'BMI',
        'children': 'Children',
        'smoker': 'Smoker',
        'charges': 'Claim'
    })
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    df['Smoker'] = df['Smoker'].map({'no': 0, 'yes': 1})

    X = df[['Age', 'BMI', 'Children', 'Sex', 'Smoker']]
    y = df['Claim']

    print(f"Data Shape: {df.shape}")
    print(df.head())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\nTraining Robust Regression (Huber)...")
    huber = HuberRegressor(epsilon=1.35, max_iter=2000)
    huber.fit(X_train, y_train)

    print("Training Linear Regression (OLS) for comparison...")
    ols = LinearRegression()
    ols.fit(X_train, y_train)

    _ = evaluate(huber, X_test, y_test, "Huber Regressor")
    _ = evaluate(ols, X_test, y_test, "Ordinary Least Squares (OLS)")

    plt.figure(figsize=(10, 6))
    plt.scatter(X_test['Age'], y_test, color='black', label='Test Data', alpha=0.3)

    mean_bmi = df['BMI'].mean()
    mean_children = df['Children'].mean()
    mean_sex = df['Sex'].mean()
    mean_smoker = df['Smoker'].mean()
    age_range = np.linspace(df['Age'].min(), df['Age'].max(), 100)
    X_vis = pd.DataFrame({
        'Age': age_range,
        'BMI': mean_bmi,
        'Children': mean_children,
        'Sex': mean_sex,
        'Smoker': mean_smoker
    })

    y_vis_huber = huber.predict(X_vis)
    y_vis_ols = ols.predict(X_vis)

    plt.plot(age_range, y_vis_huber, color='green', linewidth=2, label='Robust Huber Fit')
    plt.plot(age_range, y_vis_ols, color='red', linestyle='--', linewidth=2, label='OLS Fit')

    plt.title("Robust vs OLS Regression on Real Data")
    plt.xlabel("Age")
    plt.ylabel("Insurance Charges")
    plt.legend()
    plt.grid(True)
    plt.savefig(PLOT_PATH)
    print(f"\nComparison plot saved to '{PLOT_PATH}'")

    print("\n" + "=" * 30)
    print("ARDUINO CONFIGURATION (REAL DATA)")
    print("=" * 30)
    print("// Copy these values into your Arduino Sketch")
    print(f"float INTERCEPT = {huber.intercept_:.4f};")
    print(f"float WEIGHT_AGE = {huber.coef_[0]:.4f};")
    print(f"float WEIGHT_BMI = {huber.coef_[1]:.4f};")
    print(f"float WEIGHT_CHILDREN = {huber.coef_[2]:.4f};")
    print(f"float WEIGHT_SEX = {huber.coef_[3]:.4f};")
    print(f"float WEIGHT_SMOKER = {huber.coef_[4]:.4f};")
    print("=" * 30)


if __name__ == "__main__":
    main()
