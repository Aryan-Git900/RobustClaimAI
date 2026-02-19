# Robust Insurance Claim Prediction System

This project implements a Robust Regression model (using Huber Loss) to predict insurance claim amounts. The trained model is deployed on an Arduino for portable, offline inference.

## Project Structure
- `ml/train_model.py`: Python script to generate data, train the model, and output Arduino coefficients.
- `ml/robust_vs_ols.png`: Visualization of the model's robustness against outliers.
- `arduino/insurance_predictor/insurance_predictor.ino`: Arduino firmware.

## How to Run

### 1. Train the Model (Optional)
The model coefficients are already hardcoded in the Arduino sketch, but if you want to retrain:
1.  Install dependencies: `pip install scikit-learn pandas matplotlib`
2.  Run the script: `python ml/train_model.py`
3.  Copy the coefficients from the output to `insurance_predictor.ino`.

### 2. Upload to Arduino
1.  Open `arduino/insurance_predictor/insurance_predictor.ino` in Arduino IDE.
2.  Connect your components:
    - **LCD**: Pins 7(RS), 6(E), 5(D4), 4(D5), 3(D6), 2(D7)
    - **Keypad (4x4)**: Rows (A0-A3), Cols (8, 9, 11, 12)
    - **SD Card**: CS Pin 10, MOSI 11, MISO 12, SCK 13 (Standard SPI)
    *Note: Check your specific shield/module pinout.*
3.  Upload the sketch.

### 3. Usage
1.  Press **A** to start.
2.  Enter **Age** (e.g., 25) and press **#**.
3.  Enter **BMI** (e.g., 30) and press **#**.
4.  Enter **Children** (e.g., 2) and press **#**.
5.  View the predicted Claim Amount.
6.  Press **D** to reset.

## Robustness
The model uses **Huber Loss** to minimize the effect of outliers (e.g., fraudulent or extreme claims) during training, resulting in more reliable predictions for typical cases compared to standard Linear Regression.
