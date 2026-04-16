from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor

try:
    from ml.generate_data import generate_insurance_data, download_insurance_data
except ImportError:
    from generate_data import generate_insurance_data, download_insurance_data

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent / "insurance.csv"


def load_or_generate_data(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)

    print(f"Warning: {path} not found. Downloading real insurance data from the web.")
    df = download_insurance_data(path)
    return df


def train_model(df: pd.DataFrame) -> HuberRegressor:
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

    model = HuberRegressor(epsilon=1.35, max_iter=2000)
    model.fit(X, y)
    return model


def prompt_float(prompt: str) -> float:
    while True:
        try:
            value = input(prompt).strip()
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def prompt_sex(prompt: str) -> int:
    while True:
        value = input(prompt).strip().lower()
        if value in {'male', 'm'}:
            return 0
        if value in {'female', 'f'}:
            return 1
        if value in {'exit', 'quit'}:
            raise KeyboardInterrupt
        print("Please enter 'male' or 'female'.")


def prompt_smoker(prompt: str) -> int:
    while True:
        value = input(prompt).strip().lower()
        if value in {'yes', 'y'}:
            return 1
        if value in {'no', 'n'}:
            return 0
        if value in {'exit', 'quit'}:
            raise KeyboardInterrupt
        print("Please enter 'yes' or 'no'.")


def main():
    df = load_or_generate_data(DATA_PATH)
    model = train_model(df)

    print("\nVirtual Insurance Claim Prediction")
    print("Enter values to predict claim amount without any hardware.")
    print("Type 'exit' to quit.\n")

    while True:
        age_text = input("Age (years): ").strip()
        if age_text.lower() in {'exit', 'quit'}:
            break
        try:
            age = float(age_text)
        except ValueError:
            print("Enter a valid number for age.")
            continue

        try:
            bmi = prompt_float("BMI: ")
            children = prompt_float("Children: ")
            sex = prompt_sex("Sex (male/female): ")
            smoker = prompt_smoker("Smoker (yes/no): ")
        except KeyboardInterrupt:
            break

        features = pd.DataFrame(
            [[age, bmi, children, sex, smoker]],
            columns=['Age', 'BMI', 'Children', 'Sex', 'Smoker']
        )
        prediction = model.predict(features)[0]
        print(f"\nPredicted claim amount: ${prediction:,.2f}\n")

    print("Goodbye.")


if __name__ == "__main__":
    main()
