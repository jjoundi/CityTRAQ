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
🖥️ [Protopie file](https://universiteitgent.protopie.cloud/p/27dabdd85df1a2d35c851425?ui=true&scaleToFit=true&enableHotspotHints=true&cursorType=touch&mockup=true&bgColor=%23F5F5F5&bgImage=undefined&playSpeed=1)

## Code
* [Arduino code](main/HI5.ino) for the High Five robot (sends data to MQTT)
* [High Five server code](main/HI5.py) (listens for MQTT data and saves in a Google Sheet)
* [Air quality aggregatror script](main/AQpuller.py) (Python script to aggregate data to visualize in protopie)
* [Socket IO](main/protopie.py) that listens for Protopie calls and gives the required data back

## socket.io call-response documentation
| call | response message | response value (example)|
|------|------------------|-------------------------|
|**update_hi5**|byCar|4|
||onFoot|9|
||byBike|10|
|**update_realtime**|variabelekrekel|4.7|
||variabelelouis|9.0|
|**update_realtime**|||
|*if currentTime < 11 hours*|valuekrekel4u|4.5|
||valuekrekel5u |4.7|
||valuekrekel6u |4.8|
||valuekrekel7u |4.2|
||valuekrekel8u |5.0|
||valuelouis4u | 4.7|
||valuelouis5u | 4.7|
||valuelouis6u | 4.7|
||valuelouis7u | 4.7|
||valuelouis8u | 4.7|
|*else*|valuekrekel12u|4.5|
||valuekrekel13u |4.7|
||valuekrekel14u |4.7|
||valuekrekel15u |4.8|
||valuekrekel16u |4.2|
||valuelouis12u | 4.7|
||valuelouis13u | 4.7|
||valuelouis14u | 4.7|
||valuelouis15u | 4.7|
||valuelouis16u | 4.7|
|**update_manualdata**|krekel_pieken|10|
||krekel_carcount|10|
||louis_pieken|10|
||louis_pieken|10|

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

## Background: cron jobs
Cron jobs allow you to run scripts as specific times.

To check which cron jobs are running as a list (-l)
```
$ cd crontab -l
```
To edit the list of cron jobs (-e-)  
(If you're a first time user: choose nano as an editor the first time)
```
$ cd crontab -e
```
This opens the cron tab with many commented lines. You can replace this text with the following text (see [wiki](https://en.wikipedia.org/wiki/Cron)). This is a good overview of the structure.
```
# * * * * * <command to execute>
# | | | | |
# | | | | day of the week (0–6) (Sunday to Saturday; 
# | | | month (1–12)             7 is also Sunday on some systems)
# | | day of the month (1–31)
# | hour (0–23)
# minute (0–59)
```
A correct cron line is formatted like this. e.g. A star for the minutes means that it will run *every* minute. If you use a number, it will only run at that number. E.g. 20 * * * * * will run every 20th minute of every hour, of every day, of every month ,of every day of the week (not every 20 minues!). 

If you want to run something every x minutes using a slash seperator `/` . Let's say every 5 minutes, this looks like this
```
*/5 * * * * [command]
```
You can use multiple moments using a comma  `,` seperator, or ranges with a minus  `-`   seperator.

This is an interesting online editor [here](https://crontab.guru/), whcih translates your crontab to human language. 

For this project we use the following logic:

* On boot, [the boot is logged and a message is send as an alert](/main/log_boot.py)
* On boot, [the python server to detect high fives is started](/main/HI5.py)
* On boot, start the protopie connect server, delay, and [start the protopie socket io server](/main/protopie.py)
* Every hour (at minute 45), [the air quality script gets the latest data](/main/AQpuller.py)

```
@reboot /home/pi/citytraq/venv/bin/python /home/pi/citytraq/main/log_boot.py
@reboot	/home/pi/citytraq/venv/bin/python /home/pi/citytraq/main/HI5.py
@reboot	/home/pi/citytraq/venv/bin/python /home/pi/citytraq/main/protopie.py
45 * * * *  /home/pi/citytraq/venv/bin/python /home/pi/citytraq/main/AQpuller.py
```

### Managing cron scripts and boot logic
* *issue:* Python scripts that require connection to a server (in this case the Google API), will fail if you run them on boot.
* *solution:* Add a failsafe to the beginning of pyhton code that requires internet connection:
    ```python
    # libraries
    import socket
    import time

    # don't do anything else until there is connection with the google server
    # retry every 5 seconds

    def is_connected():
        try:
            # Try to resolve the hostname
            socket.gethostbyname('oauth2.googleapis.com')
            return True
        except socket.error:
            return False

    # Wait until the network is available
    while not is_connected():
        print("Waiting for network...")
        time.sleep(5)

    # Put the rest of the script below this
    ```

* *issue:* It can be hard to monitor all these cron triggered python scripts running in the background. Especially to monitor if the script actually ran.
* *solution:* First add the script to the crontab. Then manage the scripts using [Cronitor](https://cronitor.io/). This platform monitors the cro jobs and gives you a nice dashboard to manage and monitor all python scripts (you can manage up to 5 cronjobs in the free version).