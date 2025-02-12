// this script runs in the High 5 Robot
// It takes pushen on 3 arcade buttons as input and displays the count on 3 LED matrices
// When a button is pressed, an audio file is played to thank the kids for their input
// It also sends the count to a MQTT broker

// local network
const char* local_server_ip = "192.168.0.155"; // replace with local raspi server IP address
const char* ssid = ""; // replace with local wifi SSID
const char* password = ""; // replace with local wifi password

// libraries
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include "DFRobotDFPlayerMini.h"

// Pin Definitions and LED Matrices
#define PIN1 12 //for display 1
#define PIN2 11 //for display 2
#define PIN3 10 //for display 3
#define BUTTON_PIN1 14
#define BUTTON_PIN2 15
#define BUTTON_PIN3 16
#define AudioSerial Serial1

// define DF player instance
DFRobotDFPlayerMini myDFPlayer;

// configure LED matrices
Adafruit_NeoMatrix matrix1 = Adafruit_NeoMatrix(32, 8, PIN1, NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG, NEO_GRB + NEO_KHZ800);
Adafruit_NeoMatrix matrix2 = Adafruit_NeoMatrix(32, 8, PIN2, NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG, NEO_GRB + NEO_KHZ800);
Adafruit_NeoMatrix matrix3 = Adafruit_NeoMatrix(32, 8, PIN3, NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG, NEO_GRB + NEO_KHZ800);
const uint16_t colors[] = {matrix1.Color(255, 0, 0), matrix2.Color(0, 255, 0), matrix3.Color(0, 0, 255)};

// Counter Variables
int counter1 = 0;  // Cyclist counter
int counter2 = 0;  // Walking counter
int counter3 = 0;  // Car counter

// Timer
unsigned long lastTime = 0;
// unsigned long updateDelay = 1000*10; // update each 3 minutes
unsigned long updateDelay = 10; // update each 10 milliseconds

// button checker
int lastButtonState1 = HIGH; // Last state of button 1
int lastButtonState2 = HIGH; // Last state of button 2
int lastButtonState3 = HIGH; // Last state of button 3


// MQTT Credentials
const char* mqtt_server = local_server_ip;
const int mqtt_port = 1883;
const char* topic_main = "/citytraq";

// define the WiFi client
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// define the HTTP server
WiFiServer server(80); // HTTP server on port 80

void setup() {
  Serial.begin(9600);

  // Configure Button Pins
  pinMode(BUTTON_PIN1, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);
  pinMode(BUTTON_PIN3, INPUT_PULLUP);

  // Initialize LED Matrices
  initializeMatrices();

  // Initialize pullup buttons
  lastButtonState1 = digitalRead(BUTTON_PIN1);
  lastButtonState2 = digitalRead(BUTTON_PIN2);
  lastButtonState3 = digitalRead(BUTTON_PIN3);

  // initialize serial communication to the DF player (RX & TX)
  AudioSerial.begin(9600);

  // Open the SD card stream for audio
  myDFPlayer.begin(AudioSerial);
  myDFPlayer.volume(25);  // Set volume value. From 0 to 30

  // Connect to Wi-Fi and MQTT
  connectToWiFi();
  client.setServer(mqtt_server, mqtt_port);
  connectToMQTT();

  // Start HTTP server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // Check Wi-Fi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi connection lost. Attempting to reconnect...");
    connectToWiFi();
  }

  // Check MQTT connection
  if (!client.connected()) {
    Serial.println("MQTT connection lost. Attempting to reconnect...");
    connectToMQTT();
  }
  client.loop();

  // Handle HTTP requests
  handleHttpRequests();

  // Button Handling and Counter Update
  handleButtonPress(BUTTON_PIN1, counter1, lastButtonState1);
  handleButtonPress(BUTTON_PIN2, counter2, lastButtonState2);
  handleButtonPress(BUTTON_PIN3, counter3, lastButtonState3);

  // Update Displays
  updateDisplays();

  // short delay for stability
  delay(10);

}


// Function to initialize LED Matrices
// Set the brightness and text color
void initializeMatrices() {
  matrix1.begin();
  matrix1.setTextWrap(false);
  matrix1.setBrightness(20);
  matrix1.setTextColor(colors[0]);

  matrix2.begin();
  matrix2.setTextWrap(false);
  matrix2.setBrightness(20);
  matrix2.setTextColor(colors[1]);

  matrix3.begin();
  matrix3.setTextWrap(false);
  matrix3.setBrightness(20);
  matrix3.setTextColor(colors[2]);
}

// Function to handle HTTP Requests
// Send JSON data with counter values
void handleHttpRequests() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New HTTP request received");
    String request = client.readStringUntil('\r');
    client.flush();

    // Send HTTP Response with JSON Data
    if (request.indexOf("GET /counters") != -1) {
      StaticJsonDocument<256> jsonResponse;
      jsonResponse["cyclist"] = counter1;
      jsonResponse["walking"] = counter2;
      jsonResponse["car"] = counter3;

      String jsonOutput;
      serializeJson(jsonResponse, jsonOutput);

      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println(jsonOutput);

      Serial.println("JSON Response Sent: ");
      Serial.println(jsonOutput);
    }

    // Close the connection
    delay(1);
    client.stop();
  }
}

// Function to handle the button pressses
// Increment the counter and publish the data
void handleButtonPress(int buttonPin, int &counter, int &lastButtonState) {
  int buttonState = digitalRead(buttonPin);

  // Detect falling edge (transition from HIGH to LOW)
  if (buttonState != lastButtonState) {
    if (buttonState == LOW){
      counter++;
      publishCounters();
      Serial.print("Button Press Detected. Counter: ");
      Serial.println(counter);
      unsigned long currentTime = millis();
      // Serial.println(currentTime);
      // Serial.println(lastTime);
      playSound();
    }
    lastButtonState = buttonState;
    delay(10);
  }
}

// Function to play a random audio file
void playSound() {
    // generate random number between 1 and 9
    int randomFile = random(1,9);
    // play the audio file
    myDFPlayer.playMp3Folder(randomFile);
    Serial.print("Playing AudioFile: ");
    Serial.println(randomFile);
}


// Update LED Matrices with Counter Values
void updateDisplays() {
  displayCounter(matrix1, counter1);
  displayCounter(matrix2, counter2);
  displayCounter(matrix3, counter3);
}

void displayCounter(Adafruit_NeoMatrix &matrix, int counter) {
  matrix.fillScreen(0);
  matrix.setCursor(1, 1);
  matrix.print(counter);
  matrix.show();
}

// Wi-Fi Connection
void connectToWiFi() {
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    WiFi.begin(ssid, password);
    Serial.println("Attempting to reconnect to Wi-Fi...");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Failed to connect to Wi-Fi.");
  }
}

// MQTT Connection
void connectToMQTT() {
  Serial.println("Connecting to MQTT...");
  while (!client.connected()) {
    String clientId = "PublisherArduino-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("MQTT connected!");
    } else {
      Serial.print("MQTT connection failed, rc=");
      Serial.print(client.state());
      Serial.println(". Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

// Publish Counter Data --> MQTT 
void publishCounters() {
  unsigned long currentTime = millis();
  if (currentTime - lastTime > updateDelay) {
    StaticJsonDocument<128> doc;
    doc["byCar"] = counter1;
    doc["onFoot"] = counter2;
    doc["byBike"] = counter3;

  char message[128];
  serializeJson(doc, message);

  if (client.publish(topic_main, message)) {
    Serial.print("Published message: ");
    Serial.println(message);
  } else {
    Serial.println("Failed to publish message.");
  }
    lastTime = currentTime;
  } 
}