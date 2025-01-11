# this script is used to send a whatsapp message to a specific number
# we can use this to give us a notification when the pi boots
# when is script  runs, the browser opens and send a whatsapp message is send using the whatsapp web interface

# Importing the Required Library
import pywhatkit

# Defining the Receiving Phone Number (can't be your own number)
phone_number = "00"
message = "test"

# Sending the WhatsApp Message
pywhatkit.sendwhatmsg_instantly(phone_number, message)

# Displaying a Success Message
print("WhatsApp message sent!")