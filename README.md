# CityTRAQ
This repo is the main repo for the installation built in the city of Ghent, in the context of the EU Life project [CityTRAQ](https://www.life-citytraq.eu/) project. 
This project aims at increasing air quality awareness at elementary schools, making use of ream time data (both air quality data, self-reported monility data and objective mobility data).  

*An imec-MICT-UGent feat. design.nexus project, By Jamil Joundi, Bas Baccarne, Dennis Ossei Tutu, Tim Theys & Olivia De Ruyck, in close collabotation with the City of Ghent, VMM, and basisschool De Krekel.*

The installation has 3 parts:
* A **mobility tracker** (the High Five Robot), that measures school transport behavior using arcade buttons and counters.
* An **interactive display**, that gets data from several sources and shows this data using several screens. 
* A **playground bike installation**, that engages children on the school yard to interact with these data.

Data sources:
* Self-reported mobility behavior (local)
* Kunak sensor data (by VMM)
* A 'telslang' that measures objective mobility using a pressure detecting strip on the street   

🖥️ [Proxy Data Set](https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit?usp=sharing)

# Components

**High 5 robot**
* Big cutout board
* Wood for construction
* 3 big arcade buttons
* 3 Led matrices 
* Arduino Nano 33 IOT
* DFmini player
* Sound system   

**Interactive display**
* Big sreen
* Even bigger coutour board
* Raspi 5

**Design files**

🖊️ [Figma File](https://www.figma.com/design/ofaMDt9rZNW918LpECFY7c/CityTraq?node-id=0-1&node-type=canvas&t=k0b37edLJHGb4BCb-0)  
🖥️ [Protopie file]()

## Code
* [Arduino code](main/HI5.ino) for the High Five robot (sends data to MQTT)
* [High Five server code](main/HI5.py) (listens for MQTT data and saves in a Google Sheet)
* [Air quality aggregatror script](main/AQpuller.py) (Python script to aggregate data to visualize in protopie)
* [Socket IO](main/protopie.py) that listens for Protopie calls and gives the required data back

### Running the code
Activate High 5 server
```
$ cd citytraq
$ source venv/bin/activate
$ python HI5.py
```
Activate Socket IO server
```
$ cd citytraq
$ source venv/bin/activate
$ python protopie.py
```
Retreive aggregated air quality data
```
$ cd citytraq
$ source venv/bin/activate
$ python AQpuller.py
```

## Background: Audiofiles
To play the audio files, we are using the [DF Mini](https://www.tinytronics.nl/en/audio/audio-sources/dfrobot-dfplayer-mini-mp3-module). With an SD card. This module communicated of the Arduino TX en RX (Serial1 on Arduino Nano 33IOT).   

voices:
* The voices say thank you in 9 languages
* These are the 9 most spoken languages in Belgium ([source](https://nl.wikipedia.org/wiki/Talen_in_Belgi%C3%AB))
* Generated via Google Translate and Camptured using Chrome Audio Capture

setup:
* Prepare an SD card:
    * folder `MP3` in root
    * filenames as 0001.mp3 (see [audiofiles](data/mp3/))
* wires:
    * Arduino RX to DF player TX
    * Arduino TX (via 1k resistor, if you're working on 5V or get unstable connections) to DF player RX
    * Arduino GND to DF player GND
    * Arduino 5V to DF player VCC (5V pads on nano need be soldered, or get 5V from external)
    * Speaker - to DF player SPK1
    * Speaker + to DF player SPK2

🖥️ [Sample code](tests/high_5_robot/soundfx.ino)

## Background: Saving data in Google Sheets

**(How to write data to a Google Sheet)**

* Create a Google Cloud Platform (GCP) Project:
    * Click on the project drop-down and select "New project"
    * Enter a project name and click "Create".
* Enable the Google Sheets API:
    * In the Google Cloud Console, navigate to the "APIs & Services" > "Library".
    * Search for "Google Sheets API" and click on it.
    * Click the "Enable" button.
* Create a Service Account:
    * Go to the "APIs & Services" > "Credentials" page.
    * Click on "Create Credentials" and select "Service Account".
    * Enter a name for the service account and click "Create".
    * In the "Service account permissions" (optional) step, click "Continue".
    * In the "Grant users access to this service account" (optional) step, click "Done".
* Generate the JSON Key File:
    * After creating the service account, you will be redirected to the "Service Accounts" page.
    * Find the service account you just created and click on it.
    * Click on the "Keys" tab.
    * Click on "Add Key" and select "Create new key".
    * Choose the "JSON" key type and click "Create".
    * A JSON file will be downloaded to your computer. This is your service account key file.
* Share Your Google Sheet with the Service Account:
    * Open your Google Sheet.
    * Click on the "Share" button in the top right corner.
    * Share with all
* Use the JSON Key File in Your Python Script:
    * Place the downloaded JSON key file in your project directory.
    * See code for use
