
import numpy as np
import pandas as pd

def generate_insurance_data(n=1000):
    np.random.seed(42)
    
    # 1. Features
    # Age: Uniform 18-64
    age = np.random.randint(18, 65, n)
    
    # BMI: Normal distribution, Mean=30.6, Std=6
    bmi = np.random.normal(30.6, 6, n)
    
    # Children: Poisson-like or simple probabilities
    # 0: 45%, 1: 25%, 2: 15%, 3: 10%, 4: 3%, 5: 2%
    children = np.random.choice(
        [0, 1, 2, 3, 4, 5], 
        n, 
        p=[0.45, 0.25, 0.15, 0.10, 0.03, 0.02]
    )
    
    # Sex: Male/Female (Not used in our simple Arduino model yet, but good for realism)
    sex = np.random.choice(['male', 'female'], n)
    
    # Smoker: 20% smokers
    smoker = np.random.choice(['yes', 'no'], n, p=[0.2, 0.8])
    
    # Region (Optional, not used for price in this simple model)
    region = np.random.choice(['southwest', 'southeast', 'northwest', 'northeast'], n)

    # 2. Charges Calculation (The "Real" Formula approximation)
    # Base cost
    charges = 2500 + (age * 250) + (bmi * 320) + (children * 480)
    
    # Smoker penalty (Massive outlier effect)
    # Smokers cost ~24000 more on average
    smoker_mask = (smoker == 'yes')
    charges[smoker_mask] += 23500 + np.random.normal(0, 2000, np.sum(smoker_mask))
    
    # Add random noise to everyone
    charges += np.random.normal(0, 1000, n)
    
    # Ensure no negative charges
    charges = np.maximum(1000, charges)
    
    # Create DataFrame
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
    df = generate_insurance_data(1338) # Size of the famous dataset
    df.to_csv('insurance.csv', index=False)
    print("Generated insurance.csv with 1338 samples.")
