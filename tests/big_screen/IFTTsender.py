# this script is used to log the boots of the raspberry pi
# when the pi boots add a timestamp to a google sheet
# this Google Sheet us monitored by and IFTTT applet that sends an Android message to a specific number
# (this has about a 5 minute delay)

# libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

print("Logging new boot...")

# Google Sheets API details:
# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name("./main/keys/key.json", scope)
# Authorize the client
client = gspread.authorize(creds)
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