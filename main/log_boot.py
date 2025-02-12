# this script is used to log the boots of the raspberry pi
# when the pi boots add a timestamp to a google sheet
# this Google Sheet us monitored by and IFTTT applet that sends an Android message to a specific number
# (this has about a 5 minute delay)

# libraries
import gspread
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

print("Logging new boot...")

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
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1rPa1s33FuQhjH8xmab3BLgaVMThTJ2OO98Aii11TUmE/edit')
bootsheet = spreadsheet.worksheet('bootlog')

# get timestamps
ts = datetime.now()
unix_ts = int(ts.timestamp())
human_ts = ts.strftime("%Y-%m-%d %H:%M:%S")

# write data to google sheet
new_boot = [unix_ts, human_ts]
bootsheet.append_row(new_boot)
print(f"Boot logged at {human_ts}")