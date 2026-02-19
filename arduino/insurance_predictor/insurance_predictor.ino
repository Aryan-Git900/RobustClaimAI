
#include <Keypad.h>
#include <LiquidCrystal.h>
#include <SD.h>
#include <SPI.h>


// --- MODEL CONFIGURATION (Values from Python Training) ---
const float INTERCEPT = 3080.7959;
const float WEIGHT_AGE = 251.8535;
const float WEIGHT_BMI = 310.8470;
const float WEIGHT_CHILDREN = 458.2227;

// --- HARDWARE PIN CONFIGURATION ---
// SD Card
const int CS_PIN = 10; // Chip Select for SD card module

// LCD (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

// Keypad
const byte ROWS = 4;
const byte COLS = 4; // 4x4 Keypad
char keys[ROWS][COLS] = {{'1', '2', '3', 'A'},
                         {'4', '5', '6', 'B'},
                         {'7', '8', '9', 'C'},
                         {'*', '0', '#', 'D'}};
// Connect keypad ROW0, ROW1, ROW2, ROW3 to these Arduino pins.
byte rowPins[ROWS] = {A0, A1, A2, A3};
// Connect keypad COL0, COL1, COL2, COL3 to these Arduino pins.
byte colPins[COLS] = {8, 9, 11, 12};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// --- STATE MACHINE ---
enum State {
  STATE_WELCOME,
  STATE_INPUT_AGE,
  STATE_INPUT_BMI,
  STATE_INPUT_CHILDREN,
  STATE_PREDICT,
  STATE_RESULT
};

State currentState = STATE_WELCOME;

// Input Buffers
String inputBuffer = "";
float age = 0;
float bmi = 0;
float children = 0;

void setup() {
  Serial.begin(9600);

  // LCD Setup
  lcd.begin(16, 2);
  lcd.print("Robust Claim AI");
  delay(2000);

  // SD Card Setup
  lcd.clear();
  lcd.print("Init SD Card...");
  if (!SD.begin(CS_PIN)) {
    lcd.setCursor(0, 1);
    lcd.print("SD Fail!");
    Serial.println("SD Card initialization failed!");
    delay(2000);
    // Proceed even if SD fails, just won't log
  } else {
    lcd.setCursor(0, 1);
    lcd.print("SD Ready.");
    Serial.println("SD Card initialized.");
    delay(1000);
  }
}

void loop() {
  char key = keypad.getKey();

  switch (currentState) {
  case STATE_WELCOME:
    lcd.clear();
    lcd.print("Press A to Start");
    currentState = STATE_WAIT_START;
    break;

  case STATE_WAIT_START:
    if (key == 'A') {
      currentState = STATE_INPUT_AGE;
      inputBuffer = "";
      displayPrompt("Enter Age:", inputBuffer);
    }
    break;

  case STATE_INPUT_AGE:
    handleInput(key, age, STATE_INPUT_BMI, "Enter BMI:");
    break;

  case STATE_INPUT_BMI:
    handleInput(key, bmi, STATE_INPUT_CHILDREN, "Ent. Children:");
    // Note: BMI is effectively entered as integer here for simplicity,
    // or user can type 25 for 25.0.
    // If decimal needed, user would need a '.' key which standard keypad lacks
    // usually. We assume integer inputs for simplicity in this demo.
    break;

  case STATE_INPUT_CHILDREN:
    handleInput(key, children, STATE_PREDICT, "");
    break;

  case STATE_PREDICT:
    lcd.clear();
    lcd.print("Predicting...");

    float prediction = INTERCEPT + (WEIGHT_AGE * age) + (WEIGHT_BMI * bmi) +
                       (WEIGHT_CHILDREN * children);

    // Robustness Note:
    // The Huber Model is robust to outliers in training.
    // During inference, it behaves like a linear model but minimizes the impact
    // if the training data had crazy values.

    lcd.setCursor(0, 1);
    lcd.print("$");
    lcd.print(prediction);

    logToSD(age, bmi, children, prediction);

    delay(3000);
    lcd.clear();
    lcd.print("Claims: $");
    lcd.print(prediction);
    lcd.setCursor(0, 1);
    lcd.print("Press D to Rst");

    currentState = STATE_RESULT;
    break;

  case STATE_RESULT:
    if (key == 'D') {
      currentState = STATE_WELCOME;
    }
    break;
  }
}

// Add a placeholder state for waiting
const int STATE_WAIT_START_VAL = 99; // just a dummy for switch, used above

// Helper to display prompt and buffer
void displayPrompt(String line1, String line2) {
  lcd.clear();
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

// Helper to handle numeric input
void handleInput(char key, float &value, State nextState, String nextPrompt) {
  if (key) {
    if (key >= '0' && key <= '9') {
      inputBuffer += key;
      lcd.setCursor(0, 1);
      lcd.print(inputBuffer);
    } else if (key == '#') { // Enter/Next
      if (inputBuffer.length() > 0) {
        value = inputBuffer.toFloat();
        inputBuffer = "";
        currentState = nextState;
        if (nextState != STATE_PREDICT) {
          displayPrompt(nextPrompt, "");
        }
      }
    } else if (key == '*') { // Clear/Backspace
      inputBuffer = "";
      lcd.setCursor(0, 1);
      lcd.print("                "); // Clear line
      lcd.setCursor(0, 1);
    }
  }
}

void logToSD(float a, float b, float c, float pred) {
  File dataFile = SD.open("log.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.print("Age:");
    dataFile.print(a);
    dataFile.print(",BMI:");
    dataFile.print(b);
    dataFile.print(",Kids:");
    dataFile.print(c);
    dataFile.print(",Pred:");
    dataFile.println(pred);
    dataFile.close();
    Serial.println("Logged to SD.");
  } else {
    Serial.println("Error opening log.txt");
  }
}
