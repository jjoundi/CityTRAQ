# CityTRAQ
This repo is the main repo for the CityTRAQ project.
This project aims at increasing air quality awareness at schools.   
The installation has 3 parts:
* A mobility tracker (the High Five Robot)
* An interactive display
* A playground bike installation

# Components

**High 5 robot**
* Big cutout board
* Wood for construction
* Arcade buttons
* Arduino Nano 33 IOT
* LED matrixes   

**Interactive display**
* Big sreen
* Even bigger coutour board
* Wood for construction
* Big screen
* Raspi 5

**Design files**

🖊️ [Figma File](https://www.figma.com/design/ofaMDt9rZNW918LpECFY7c/CityTraq?node-id=0-1&node-type=canvas&t=k0b37edLJHGb4BCb-0)  
🖥️ [Protopie file]()

## Code
* [Arduino code](HighFive_Interface_w_Data.ino) for the High Five robot (sends data to MQTT)
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