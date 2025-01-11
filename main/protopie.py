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

# Google Sheets API details:
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name("./main/keys/key.json", scope)
# Authorize the client
client = gspread.authorize(creds)
# Open the Google Sheet using the URL
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit')
hi5_sheet = spreadsheet.worksheet('Hi5_live') # name of the sheet with live HI5 data
AQ_sheet = spreadsheet.worksheet('AQ_live') # name of the sheet with AQ data

# Change the address below to yours of localhost is not working
address = 'http://localhost:9981'

# create a socketio client
io = socketio.Client()

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

    # 1 # react if protopie sends an 'update_h5' message
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

    # 2 # react if protopie sends an 'AQ' message (airquality)
    if messageId == 'AQ':
        print('[SOCKET IO] Protopie requires an update of the airquality data.')
        print('Getting the latest data from Google Sheets ...')
        data = AQ_sheet.get_all_values()

        # RESPONSE
        for entry in data[1:]: 
            message = entry[0]
            value = entry[1]
            print('Sending data to Protopie:', message, ":",value)
            io.emit('ppMessage', {'messageId':message, 'value':value})

# connect to the server
io.connect(address)

# keep the line open for receiving messages
while True:
  pass