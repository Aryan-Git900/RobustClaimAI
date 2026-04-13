from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor

try:
    from ml.generate_data import generate_insurance_data
except ImportError:
    from generate_data import generate_insurance_data

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent / "insurance.csv"


def load_or_generate_data(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)

    df = generate_insurance_data(1338)
    df.to_csv(path, index=False)
    return df


def train_model(df: pd.DataFrame) -> HuberRegressor:
    df = df.rename(columns={
        'age': 'Age',
        'bmi': 'BMI',
        'children': 'Children',
        'charges': 'Claim'
    })
    X = df[['Age', 'BMI', 'Children']]
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

        bmi = prompt_float("BMI: ")
        children = prompt_float("Children: ")

        features = pd.DataFrame(
            [[age, bmi, children]],
            columns=['Age', 'BMI', 'Children']
        )
        prediction = model.predict(features)[0]
        print(f"\nPredicted claim amount: ${prediction:,.2f}\n")

    print("Goodbye.")


if __name__ == "__main__":
    main()
