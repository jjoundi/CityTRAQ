# dependencies 
# pip install paho-mqtt, gspread, oauth2client

# niet vergeten switchen: auto, voetganger en fiets 

#libraries
import paho.mqtt.client as mqtt  

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# MQTT broker details
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "CityTraqMobilityCounter"

# Google Sheets API details:
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name("./tests/key.json", scope)
# Authorize the client
client = gspread.authorize(creds)
# Open the Google Sheet using the URL
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit').sheet1

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

    # data = msg.payload.decode()
    data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]
    for row in data:
        sheet.append_row(row)

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
