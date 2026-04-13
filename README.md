# Robust Insurance Claim Prediction System

A complete project for robustly predicting insurance claim amounts using Huber regression. The system includes:

- synthetic data generation
- model training and evaluation
- a virtual CLI prediction demo
- a minimal browser interface
- optional Arduino deployment

## Project Structure
- `main.py`: root entry point to run the virtual demo, train the model, or generate the dataset.
- `ml/generate_data.py`: synthetic insurance dataset generator.
- `ml/train_model.py`: trains the Huber regression model, evaluates it, and prints Arduino coefficients.
- `ml/virtual_predict.py`: interactive CLI demo for browser-free prediction.
- `ml/robust_vs_ols.png`: comparison plot showing robust vs OLS regression.
- `web-showcase/index.html`: minimal black-and-white browser UI for prediction.
- `arduino/insurance_predictor/insurance_predictor.ino`: optional Arduino firmware for offline inference.

## How to Use

### 1. Install Dependencies
Create or activate a Python virtual environment, then install:

```bash
pip install -r requirements.txt
```

### 2. Run the Virtual Demo
Use the CLI demo to predict claims without any hardware:

```bash
python main.py virtual
```

Enter values for `Age`, `BMI`, and `Children` when prompted.

### 3. Open the Browser Demo
Open the static page in a browser:

- `web-showcase/index.html`

This page performs prediction in the browser using pre-trained model coefficients.

### 4. Train the Model (Optional)
To retrain the model and produce updated evaluation output:

```bash
python main.py train
```

### 5. Regenerate the Dataset (Optional)
To recreate the synthetic dataset:

```bash
python main.py generate
```

### 6. Optional Arduino Deployment
The Arduino sketch is optional and can be used later for a physical deployment.

## Overview
This project is built around robust regression with **Huber loss**. That means the model is less sensitive to extreme outliers than ordinary least squares, while still fitting the bulk of the data accurately.

## Notes
- The prediction model uses three inputs: `Age`, `BMI`, and `Children`.
- The browser demo is fully virtual and does not require a backend server.
- The Arduino sketch is included only as an optional extension.
