# install dependencies with: pip install paho-mqtt

# niet vergeten switchen: auto, voetganger en fiets 


import paho.mqtt.client as mqtt  

# MQTT broker details
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "CityTraqMobilityCounter"

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
