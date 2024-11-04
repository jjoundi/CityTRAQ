#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

#define PIN1 12 // for display 1
#define PIN2 11 // for display 2
#define PIN3 10 // for display 3
#define BUTTON_PIN1 14 // Pin for the button 1
#define BUTTON_PIN2 15 // Pin for the button 2
#define BUTTON_PIN3 16 // Pin for the button 3

//Display 1
Adafruit_NeoMatrix matrix1 = Adafruit_NeoMatrix(32, 8, PIN1,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

//Display 2
Adafruit_NeoMatrix matrix2 = Adafruit_NeoMatrix(32, 8, PIN2,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

//Display 3
Adafruit_NeoMatrix matrix3 = Adafruit_NeoMatrix(32, 8, PIN3,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

const uint16_t colors[] = {
  matrix1.Color(255, 0, 0), matrix2.Color(0, 255, 0), matrix3.Color(0, 0, 255) };

//button 1
int counter1 = 0; // Variable to store the number
int buttonState1 = 0; // Variable for reading the button status
int lastButtonState1 = HIGH; // Stores the last button state
bool buttonPressed1 = false; // To track button press event

//button 2
int counter2 = 0; // Variable to store the number
int buttonState2 = 0; // Variable for reading the button status
int lastButtonState2 = HIGH; // Stores the last button state
bool buttonPressed2 = false; // To track button press event

//button 3
int counter3 = 0; // Variable to store the number
int buttonState3 = 0; // Variable for reading the button status
int lastButtonState3 = HIGH; // Stores the last button state
bool buttonPressed3 = false; // To track button press event


void setup() {
  Serial.begin(9600);
// Display 1
  matrix1.begin();
  matrix1.setTextWrap(false);
  matrix1.setBrightness(20);
  matrix1.setTextColor(colors[0]); // Choose the color for the text

// Display 2
  matrix2.begin();
  matrix2.setTextWrap(false);
  matrix2.setBrightness(20);
  matrix2.setTextColor(colors[1]); // Choose the color for the text

// Display 3
  matrix3.begin();
  matrix3.setTextWrap(false);
  matrix3.setBrightness(20);
  matrix3.setTextColor(colors[2]); // Choose the color for the text
  
  pinMode(BUTTON_PIN1, INPUT_PULLUP); // Set button pin 1 as input with pull-up
  pinMode(BUTTON_PIN2, INPUT_PULLUP); // Set button pin 2 as input with pull-up
  pinMode(BUTTON_PIN3, INPUT_PULLUP); // Set button pin 3 as input with pull-up
}

void loop() {
  // Read the button state
  buttonState1 = digitalRead(BUTTON_PIN1);
  buttonState2 = digitalRead(BUTTON_PIN2);
  buttonState3 = digitalRead(BUTTON_PIN3);
  Serial.print(buttonState3);

  // Check if the button 1 is pressed (LOW) and was not pressed before
  if (buttonState1 == LOW && lastButtonState1 == HIGH) {
    buttonPressed1 = true; // Mark that the button was pressed
    }
  // Check if the button 2 is pressed (LOW) and was not pressed before
  if (buttonState2 == LOW && lastButtonState2 == HIGH) {
    buttonPressed2 = true; // Mark that the button was pressed
    }
  // Check if the button 3 is pressed (LOW) and was not pressed before
  if (buttonState3 == LOW && lastButtonState3 == HIGH) {
    buttonPressed3 = true; // Mark that the button was pressed
    }
    delay(50); // Debounce delay
  
  
  // If the button was pressed, increment the counter
  if (buttonPressed1) {
    counter1++; // Increment the counter
    buttonPressed1 = false; // Reset the button pressed flag
    }
  // If the button was pressed, increment the counter
  if (buttonPressed2) {
    counter2++; // Increment the counter
    buttonPressed2 = false; // Reset the button pressed flag
    }
  // If the button was pressed, increment the counter
  if (buttonPressed3) {
    counter3++; // Increment the counter
    buttonPressed3 = false; // Reset the button pressed flag
    }
  
  // Update last button state
  lastButtonState1 = buttonState1;
  lastButtonState2 = buttonState2;
  lastButtonState3 = buttonState3;

  // Display the counter value on the LED matrix 1
  matrix1.fillScreen(0); // Clear the screen
  matrix1.setCursor(1, 1); // Adjust position as needed

  matrix1.print(counter1); // Display the counter value

  matrix1.show(); // Show the content on the LED matrix

  // Display the counter value on the LED matrix 2
  matrix2.fillScreen(0); // Clear the screen
  matrix2.setCursor(1, 1); // Adjust position as needed

  matrix2.print(counter2); // Display the counter value

  matrix2.show(); // Show the content on the LED matrix

  // Display the counter value on the LED matrix 3
  matrix3.fillScreen(0); // Clear the screen
  matrix3.setCursor(1, 1); // Adjust position as needed

  matrix3.print(counter3); // Display the counter value

  matrix3.show(); // Show the content on the LED matrix
  
  delay(100); // Adjust update speed if needed
}
