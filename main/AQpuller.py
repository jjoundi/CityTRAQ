# This script pulls aur qualitay data from an API and writes it to a Google Sheet

# dependencies 
# pip install gspread, oauth2client, requests

#libraries
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict
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

# Google Sheets API details:
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/jjoundi/CityTRAQ/main/keys/key.json", scope)
# Authorize the client
client = gspread.authorize(creds)
# Open the Google Sheet using the URL
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit')
sheet_AQ = spreadsheet.worksheet('AQ_live') # name of the sheet with ariquality data


# Read username and password from the file
with open('/home/jjoundi/CityTRAQ/main/keys/credentials.txt', 'r') as file:
    username = file.readline().strip()
    password = file.readline().strip()

# Get the current timestamp for log data
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Make a GET request to the API - Live Krekelberg #
###################################################

url = 'https://kunakcloud.com/openAPIv0/v1/rest/devices/0423440187/elements/NO2 GCc/info'
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
# If successful, print the data
if response.status_code == 200:
    data = response.json()
    last_read = data.get('last_read', {})
    ts = last_read.get('ts')
    value = last_read.get('value')
    print(f"Received data from Krekelberg Live || Value: {value}")

    # Convert the ts to a human-readable timestamp
    human_ts = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # Transform the data to the desired structure for writing to Google Sheets
    transformed_data = [["type", "locatie", "ts", "human ts", "value"], 
                        ["actual", "krekelberg", ts, human_ts, value]]

else:
    print(f"Failed to retrieve data: {response.status_code}")

# Make a GET request to the API - Live Louis Schuermanstraat #
##############################################################

url = 'https://kunakcloud.com/openAPIv0/v1/rest/devices/0423440204/elements/NO2%20GCc/info'
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
# If successful, print the data
if response.status_code == 200:
    data = response.json()
    last_read = data.get('last_read', {})
    ts = last_read.get('ts')
    value = last_read.get('value')
    print(f"Received data from Louis Schuermanstraat Live || Value: {value}")

    # Convert the ts to a human-readable timestamp
    human_ts = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # Transform the data to the desired structure for writing to Google Sheets
    new_row = ["actual", "Louis Schuerman", ts, human_ts, value]
    transformed_data.append(new_row)

else:
    print(f"Failed to retrieve data: {response.status_code}")

# Make a GET request to the API - Uurgemiddelden laatste 24 uur Krekel #
########################################################################

# timestamps laatste 24 uur
end = datetime.now()
start = end - timedelta(days=1)
ts_start = int(start.timestamp() * 1000)
ts_end = int(end.timestamp() * 1000)
# print(ts_start)
# print(ts_end)

url = f'https://kunakcloud.com/openAPIv0/v1/rest/devices/0423440187/elements/NO2%20GCc/reads/fromTo?startTs={ts_start}&endTs={ts_end}'
# print(url)
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Received data from Krekelberg, calculating hourly averages ... ")

    # Initialize a dictionary to store values by hour
    hourly_values = defaultdict(list)
    hourly_timestamps = {}

    # Process each entry in the data
    for entry in data:
        value = round(float(entry["value"]), 2)
        ts = entry["ts"]
        # Convert timestamp to datetime
        dt = datetime.utcfromtimestamp(ts / 1000)
        hour = dt.hour
        # Append the value to the corresponding hour
        hourly_values[hour].append(value)
        # Keep the latest timestamp for each hour
        hourly_timestamps[hour] = ts

    # Calculate the average for each hour
    hourly_averages = {hour: round(sum(values) / len(values),2) for hour, values in hourly_values.items()}

    # Sort the hours from 1 to 24 and print the hourly averages
    for hour in sorted(hourly_averages.keys()):
        # print(f"Hour: {hour}, Average Value: {hourly_averages[hour]}, Last Timestamp: {hourly_timestamps[hour]}")

        new_row = [f"{hour}", "krekel", hourly_timestamps[hour], datetime.utcfromtimestamp(hourly_timestamps[hour] / 1000).strftime('%Y-%m-%d %H:%M:%S'), hourly_averages[hour]]
        transformed_data.append(new_row)

else:
    print(f"Failed to retrieve data: {response.status_code}")

# Make a GET request to the API - Uurgemiddelden laatste 24 uur Live Louis Schuermanstraat #
#############################################################################################


url = f'https://kunakcloud.com/openAPIv0/v1/rest/devices/0423440204/elements/NO2%20GCc/reads/fromTo?startTs={ts_start}&endTs={ts_end}'
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Received data from Louis Schuerman straat, calculating hourly averages ... ")

    # Initialize a dictionary to store values by hour
    hourly_values = defaultdict(list)
    hourly_timestamps = {}

    # Process each entry in the data
    for entry in data:
        value = round(float(entry["value"]), 2)
        ts = entry["ts"]
        # Convert timestamp to datetime
        dt = datetime.utcfromtimestamp(ts / 1000)
        hour = dt.hour
        # Append the value to the corresponding hour
        hourly_values[hour].append(value)
        # Keep the latest timestamp for each hour
        hourly_timestamps[hour] = ts

    # Calculate the average for each hour
    hourly_averages = {hour: round(sum(values) / len(values),2) for hour, values in hourly_values.items()}

    # Sort the hours from 1 to 24 and print the hourly averages
    for hour in sorted(hourly_averages.keys()):
        # print(f"Hour: {hour}, Average Value: {hourly_averages[hour]}, Last Timestamp: {hourly_timestamps[hour]}")

        new_row = [f"{hour}", "louis", hourly_timestamps[hour], datetime.utcfromtimestamp(hourly_timestamps[hour] / 1000).strftime('%Y-%m-%d %H:%M:%S'), hourly_averages[hour]]
        transformed_data.append(new_row)

else:
    print(f"Failed to retrieve data: {response.status_code}")

# Put everything in the Google Sheet #
#######################################

# Clear the existing content in the sheet
sheet_AQ.clear()
    
# Append the transformed data to the Google sheet (live data sheet)
sheet_AQ.append_rows(transformed_data)
    
print("Data written to Google Sheets!")