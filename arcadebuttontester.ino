const int buttonPin = 12; // Pin where the button is connected

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set the button pin as an input with pullup resistor
  pinMode(buttonPin, INPUT_PULLUP);

  // Print initialization message
  Serial.println("Single Button Tester Initialized");
  Serial.println("Press the button to see its status.");
}

void loop() {
  // Read the button state
  int buttonState = digitalRead(buttonPin);

  // Check if the button is pressed
  if (buttonState == LOW) { // LOW indicates the button is pressed due to pullup
    Serial.println("Button is PRESSED");
  } else {
    Serial.println("Button is NOT pressed");
  }

  delay(200); // Small delay to avoid spamming the serial monitor
}
