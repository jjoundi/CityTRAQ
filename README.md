# CityTRAQ
Building interfaces for the CityTRAQ project

Figma file: https://www.figma.com/design/ofaMDt9rZNW918LpECFY7c/CityTraq?node-id=0-1&node-type=canvas&t=k0b37edLJHGb4BCb-0

Protopie file: 

## Google drive with API calls:

**How to write data to a Google Sheet**

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

## How to make a raspberry pi run a python script on boot
Let's say the name of the python script (called a 'service') is mqtt_pull_and_write.service and the python file is called Hi5.py
```
sudo nano /etc/systemd/system/mqtt_pull_and_write.service
```
Update the service file
```
[Unit]
Description=MQTT Pull and Write Service
After=network.target

[Service]
ExecStart=/home/jjoundi/citytraq/venv/bin/python3 /home/jjoundi/citytraq/Hi5.py
WorkingDirectory=/home/jjoundi/citytraq
StandardOutput=inherit
StandardError=inherit
Restart=always
User=jjoundi

[Install]
WantedBy=multi-user.target
```
Reload Systemd and Restart the Service:
```
sudo systemctl daemon-reload
sudo systemctl restart mqtt_pull_and_write.service
```
Check the status
```
sudo systemctl status mqtt_pull_and_write.service
```
