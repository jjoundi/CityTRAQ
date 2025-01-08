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
creds = ServiceAccountCredentials.from_json_keyfile_name("./tests/key.json", scope)
# Authorize the client
client = gspread.authorize(creds)
# Open the Google Sheet using the URL
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YUWfkA1w6GezTzYUTnjYmWHWe1nIyDaAK0Ytp2pUTw0/edit')
hi5_sheet = spreadsheet.worksheet('Hi5_live') # name of the sheet with live data

# Change the address below to yours of localhost is not working
address = 'http://localhost:9981'

# create a socketio client
io = socketio.Client()

# function to handle the connection
# identify the device as 'python' to the server
@io.on('connect')
def on_connect():
    print('[SOCKET IO] Connected to server')
    print('This script can now receive and send messages to Protopie ...')
    io.emit('ppBridgeApp', { 'name': 'Python script' })


# function to handle incoming messages
@io.on('ppMessage')
def on_message(data):

    # the message is stored as a dictionary
    messageId = data['messageId']
    value = data['value'] if 'value' in data else None
    print('[SOCKET IO] Received a Message from Protopie: ', data)

    # react if protopie sends an 'update_h5' message
    if messageId == 'update_hi5':
        print('[SOCKET IO] Protpie requires an update of the Hi5 data')
        print('Getting the latest data from Google Sheets ...')
        data = hi5_sheet.get_all_values()
        # print('Data from Google Sheets:', data)

        # Send the data of each row to Protopie (skip header row)
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