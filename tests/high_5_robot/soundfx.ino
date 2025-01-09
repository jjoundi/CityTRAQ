// This script plays a random audiofile when a button is pressed
// The audiofiles are stored on the SD card

// Hardware: DFPlayer Mini

// On Arduino Nano 33IOT the TX & RX pins are added to the Serial1 object
// Name Serial1 as AudioSerial to make it clear that it is used for the DFPlayer

// Wires:
// Arduino RX to DF player TX
// Arduino TX (via 1k resistor) to DF player RX
// Arduino GND to DF player GND
// Arduino 5V to DF player VCC (5V pads on nano need be soldered)
// Speaker - to DF player SPK1
// Speaker + to DF player SPK2
// Arduino GND to button side 1
// Arduino pin 9 to button side 2

// File structure  (SD card):
// files need to start with 4 digits: e.g. 0001.mp3, 0002.mp3, 0003.mp3, etc.
// after these 4 digits, the file name can be anything: e.g. 0001.mp3, 0001_hello.mp3, 0001_hello_world.mp3, etc.
// the folder name needs to be "MP3", placed under the SD card "root" directory

// voices: the voices say thank you in 9 languages
// source: https://nl.wikipedia.org/wiki/Talen_in_Belgi%C3%AB
// Generated via Google Translate and Chrome Audio Capture

// libs
#include "DFRobotDFPlayerMini.h"

// pins
#define BUTTONPIN 9
#define AudioSerial Serial1
DFRobotDFPlayerMini myDFPlayer;

// variables
int buttonState = 0;
int lastButtonState = 0;

void setup() {

    Serial.begin(9600);

    // set pins
    pinMode(BUTTONPIN, INPUT_PULLUP);
    
    // Initialize lastButtonState to the current state of the button
    lastButtonState = !digitalRead(BUTTONPIN);

    // initialize serial communication to the DF player (RX & TX)
    AudioSerial.begin(9600);

    // Open the SD card stream
    myDFPlayer.begin(AudioSerial);
    myDFPlayer.volume(30);  // Set volume value. From 0 to 30
}

void loop() {
    // print button state, one each time the button is pressed
    buttonState = !digitalRead(BUTTONPIN);
    if (buttonState != lastButtonState) {
        if (buttonState == 1){
            playSound();
        }
        lastButtonState = buttonState;
    }
    delay(10);
}

void playSound() {
    // generate random number between 1 and 9
    int randomFile = random(1,9);
    // play the audio file
    myDFPlayer.playMp3Folder(randomFile);
    Serial.print("Playing AudioFile: ");
    Serial.println(randomFile);
}
  