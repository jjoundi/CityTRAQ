# This script is a simple Python script that sends and receives messages from Protopie. It uses the socketio library to connect to the Protopie server and send and receive messages. The script connects to the server, identifies itself as 'python', and then waits for messages from Protopie. When a message is received, it prints the message to the console. The script also prompts the user to input a message id and value, which it then sends to Protopie. The script will continue to prompt the user for input and send messages until it is terminated.

#!/usr/bin/env python3
# pip install python-socketio
# python -m pip install websocket-client

# libraries
import socketio
import fileinput
import sys

# if localhost is not working, change the address to your local ip address
address = 'http://localhost:9981'

# create a socketio client
io = socketio.Client()

# connect to the server
@io.on('connect')
def on_connect():
    print('[SOCKERIO] Connected to server')
    io.emit('ppBridgeApp', { 'name': 'python' })

# RECEIVING MESSAGES
@io.on('ppMessage')
def on_message(data):
    messageId = data['messageId']
    value = data['value'] if 'value' in data else None
    print('[SOKCET IO] Received a Message from Protopie connect', data)
    # format: {'messageId': 'test', 'value': '1', 'time': 1736363158148}

    if messageId == 'update':
        print('Updating data')
        io.emit('ppMessage', {'messageId':response, 'value':1})


# connect to the server
io.connect(address)

# KEEP OPEN LINE FOR RECEIVING MESSAGES
while 1:    
  messageId = input('Please input a message id: ')
  value = input('Please input a value: ')

  print('\tSend ', messageId, ':', value, ' data to Connect');
  io.emit('ppMessage', {'messageId':messageId, 'value':value})