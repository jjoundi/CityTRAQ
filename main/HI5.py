# this script is used to read data from the MQTT broker and write it to a Google Sheet

# dependencies 
# pip install paho-mqtt, gspread, oauth2client

# niet vergeten switchen: auto, voetganger en fiets 

#libraries
import paho.mqtt.client as mqtt  
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime 
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

# MQTT broker details
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "CityTraqMobilityCounter"

# Google Sheets API details:
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/jjoundi/CityTRAQ/main/keys/key.json", scope)
# Authorize the client
def authorize_client():
    try:
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Failed to authorize client: {e}")
        time.sleep(5)
        return authorize_client()

client = authorize_client()
# Open the Google Sheet using the URL
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit')
sheet_live = spreadsheet.worksheet('Hi5_live') # name of the sheet with live data
sheet_log = spreadsheet.worksheet('Hi5_log') # name of the sheet with log data

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)  # Subscribe to the topic
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

    # Decode the message
    data = msg.payload.decode()

    # Load the JSON data into a dictionary
    data_dict = json.loads(data)
    
    # Transform the dictionary to the desired structure for writing to Google Sheets
    transformed_data = [["Mode of Transport", "Count"]]
    for key, value in data_dict.items():
        transformed_data.append([key, value])
    
    # Print the transformed data (debgugging)
    # print(transformed_data)

    # Clear the existing content in the sheet
    sheet_live.clear()

    # Append the transformed data to the Google sheet (live data sheet)
    for row in transformed_data:
        sheet_live.append_row(row)

    # Get the current timestamp for log data
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append the data to the log sheet
    anno_data = []
    for key, value in data_dict.items():
        anno_data.append([key, value, timestamp])

    # Append the data to the Google sheet (log data sheet)
    for row in anno_data:
        sheet_log.append_row(row)
    
    print("Data written to Google Sheets!")

# Create MQTT client instance
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
print("Connecting to broker...")
client.connect(BROKER, PORT, 60)

# Start the loop to process network events
client.loop_forever()
