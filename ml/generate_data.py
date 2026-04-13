import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "insurance.csv"

def generate_insurance_data(n=1000):
    np.random.seed(42)

    age = np.random.randint(18, 65, n)
    bmi = np.random.normal(30.6, 6, n)
    children = np.random.choice(
        [0, 1, 2, 3, 4, 5],
        n,
        p=[0.45, 0.25, 0.15, 0.10, 0.03, 0.02]
    )
    sex = np.random.choice(['male', 'female'], n)
    smoker = np.random.choice(['yes', 'no'], n, p=[0.2, 0.8])
    region = np.random.choice(['southwest', 'southeast', 'northwest', 'northeast'], n)

    charges = 2500 + (age * 250) + (bmi * 320) + (children * 480)
    smoker_mask = (smoker == 'yes')
    charges[smoker_mask] += 23500 + np.random.normal(0, 2000, np.sum(smoker_mask))
    charges += np.random.normal(0, 1000, n)
    charges = np.maximum(1000, charges)

    df = pd.DataFrame({
        'age': age,
        'sex': sex,
        'bmi': bmi,
        'children': children,
        'smoker': smoker,
        'region': region,
        'charges': charges
    })

    return df

if __name__ == "__main__":
    df = generate_insurance_data(1338)
    df.to_csv(DATA_PATH, index=False)
    print(f"Generated {DATA_PATH} with {len(df)} samples.")
