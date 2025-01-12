# Description: This script connects to the Protopie server and sends data to Protopie when requested.
# More specifically, this script listens for a message from Protopie with the messageId 'update_hi5'. When this message is received, the script fetches the latest data from a Google Sheet and sends it to Protopie.

#!/usr/bin/env python3
# pip install python-socketio
# python -m pip install websocket-client

# libraries
import socketio
import fileinput
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
hi5_sheet = spreadsheet.worksheet('Hi5_live') # name of the sheet with live HI5 data
AQ_sheet = spreadsheet.worksheet('AQ_live') # name of the sheet with AQ data
manual_sheet = spreadsheet.worksheet('manual') # name of the sheet with manual data

# Change the address below to yours if localhost is not working
address = 'http://localhost:9981'

# create a socketio client
io = socketio.Client()

# don't do anything else until there is connection with the socket.io server
def wait_for_server(address, delay=5):
    while True:
        try:
            # Attempt to connect to the server if not already connected
            if not io.connected:
                io.connect(address)
                print("Connected to the Socket.io Protopie server")
            return
        except socketio.exceptions.ConnectionError:
            print("Protopie Connect Server not available, retrying...")
            time.sleep(delay)

# Wait for the server to be available
wait_for_server(address)

# function to handle the connection
# identify the device as 'python' to the socket.io server
@io.on('connect')
def on_connect():
    print('[SOCKET IO] Connected to server')
    print('This script can now receive and send messages to Protopie ...')
    io.emit('ppBridgeApp', { 'name': 'Python script' })

# function to handle incoming messages from protopie connect
# message is stored as a dictionary in the 'data' variable, with the messageId and value as keys
@io.on('ppMessage')
def on_message(data):
    messageId = data['messageId']
    value = data['value'] if 'value' in data else None
    print('[SOCKET IO] Received a Message from Protopie: ', data)

    ############
    # TRIGGERS #
    ############
    # documentation: https://github.com/jjoundi/CityTRAQ/?tab=readme-ov-file#socketio-call-response-documentation 

    # 1 # react if protopie sends an 'update_hi5' message
    if messageId == 'update_hi5':
        print('[SOCKET IO] Protopie requires an update of the Hi5 data')
        print('Getting the latest data from Google Sheets ...')
        data = hi5_sheet.get_all_values()
        # print('Data from Google Sheets:', data)

        # RESPONSE
        # Send the data of each row to Protopie (skip header row)
        # e.g. byCar:2
        for entry in data[1:]: 
            message = entry[0]
            value = entry[1]
            print('Sending data to Protopie:', message, ":",value)
            io.emit('ppMessage', {'messageId':message, 'value':value})

    # 2 # react if protopie sends an 'update_realtime' message
    if messageId == 'update_realtime':
        print('[SOCKET IO] Protopie requires an update of the realtime airquality data.')
        print('Getting the latest data from Google Sheets ...')
        data = AQ_sheet.get_all_values()

        # RESPONSE
        for entry in data[1:]: 
            if entry[0] == "actual" and  entry[1] == "krekelberg":
                message = "variabelekrekel"
                value = entry[4]
            elif entry[0] == "actual" and  entry[1] == "Louis Schuerman":
                message = "variabelelouis"
                value = entry[4]
            print('Sending data to Protopie:', message, ":",value)
            io.emit('ppMessage', {'messageId':message, 'value':value})

    # 3 # react if protopie sends an 'update_avg' message
    if messageId == 'update_avg':
        print('[SOCKET IO] Protopie requires an update of the airquality data (hourly averages).')
        print('Getting the latest data from Google Sheets ...')
        data = AQ_sheet.get_all_values()

        # Time orientation & time ranges
        currentHour = datetime.now().hour
        print(f'It is now {currentHour} o\'clock.')
        if currentHour < 11:
            range_start = 4
            range_end = 8
            print(f"[MORNING] giving back data from {range_start} to {range_end} o'clock")
        elif currentHour >=11:
            range_start = 12
            range_end = 16
            print(f"[MORNING] giving back data from {range_start} to {range_end} o'clock")

        # RESPONSE
        for entry in data[3:]: 
            # check if the entry is in the range
            if range_start <= entry[0] <= range_end:
                message = value+entry[1]+entry[0]+u
                value = entry[4]
                print('Sending data to Protopie:', message, ":",value)
                io.emit('ppMessage', {'messageId':message, 'value':value})

    # 4 # react if protopie sends an 'update_manualdata' message
    if messageId == 'update_manualdata':
        print('[SOCKET IO] Protopie requires an update of the manually entered data.')
        print('Getting the latest data from Google Sheets ...')
        data = manual_sheet.get_all_values()

        # RESPONSE
        for entry in data: 
            message = entry[0]
            value = entry[1]
            print('Sending data to Protopie:', message, ":",value)
            io.emit('ppMessage', {'messageId':message, 'value':value})

# keep the line open for receiving messages
io.wait()