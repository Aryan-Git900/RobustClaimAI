
import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# 1. Load Data
try:
    df = pd.read_csv('insurance.csv')
    print("Loaded insurance.csv")
except FileNotFoundError:
    print("Error: insurance.csv not found. Run generate_data.py first.")
    exit()

# Rename columns to match our convention if needed
# The generator produces lowercase columns, let's standardize
df.rename(columns={'age': 'Age', 'bmi': 'BMI', 'children': 'Children', 'charges': 'Claim'}, inplace=True)

# 2. Preprocessing
# We only use Age, BMI, Children for the Arduino model
X = df[['Age', 'BMI', 'Children']]
y = df['Claim']

print(f"Data Shape: {df.shape}")
print(df.head())

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Model Training
print("\nTraining Robust Regression (Huber)...")
# epsilon=1.35 is standard. higher epsilon -> closer to OLS.
huber = HuberRegressor(epsilon=1.35, max_iter=2000) 
huber.fit(X_train, y_train)

print("Training Linear Regression (OLS) for comparison...")
ols = LinearRegression()
ols.fit(X_train, y_train)

# 4. Evaluation
def evaluate(model, name):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f"\n{name} Results:")
    print(f"  MAE: {mae:.2f}")
    print(f"  MSE: {mse:.2f}")
    print(f"  Coefficients: {model.coef_}")
    print(f"  Intercept: {model.intercept_:.2f}")
    return y_pred

y_pred_huber = evaluate(huber, "Huber Regressor")
y_pred_ols = evaluate(ols, "Ordinary Least Squares (OLS)")

# 5. Visualization (Effect of Outliers)
plt.figure(figsize=(10, 6))
plt.scatter(X_test['Age'], y_test, color='black', label='Test Data', alpha=0.3)

# To visualize the "fit", we can predict using mean BMI and Children
mean_bmi = df['BMI'].mean()
mean_children = df['Children'].mean()

age_range = np.linspace(df['Age'].min(), df['Age'].max(), 100)
X_vis = pd.DataFrame({'Age': age_range, 'BMI': mean_bmi, 'Children': mean_children})

y_vis_huber = huber.predict(X_vis)
y_vis_ols = ols.predict(X_vis)

plt.plot(age_range, y_vis_huber, color='green', linewidth=2, label='Robust Huber Fit')
plt.plot(age_range, y_vis_ols, color='red', linestyle='--', linewidth=2, label='OLS Fit')

plt.title("Robust vs OLS Regression on Real Data")
plt.xlabel("Age")
plt.ylabel("Insurance Charges")
plt.legend()
plt.grid(True)
plt.savefig("ml/robust_vs_ols.png")
print("\nComparison plot saved to 'ml/robust_vs_ols.png'")

# 6. Generate Arduino Code Snippet
print("\n" + "="*30)
print("ARDUINO CONFIGURATION (REAL DATA)")
print("="*30)
print("// Copy these values into your Arduino Sketch")
print(f"float INTERCEPT = {huber.intercept_:.4f};")
print(f"float WEIGHT_AGE = {huber.coef_[0]:.4f};")
print(f"float WEIGHT_BMI = {huber.coef_[1]:.4f};")
print(f"float WEIGHT_CHILDREN = {huber.coef_[2]:.4f};")
print("="*30)
