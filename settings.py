"""My custom settings for my bot.

Update all variables in the '.env' file.
"""
import os
import socket

# Get Chatbot Credentials specified in .env file
CHATBOT_ID = os.environ.get('CHATBOT_ID')
SECRET_KEY = os.environ.get('SECRET_KEY')

# Below code gets your computer's IP address.
# If you use VPN and do not explicitly set this to your
# computer's IP address, your bot may be assigned the VPN
# Proxy server IP address and will not work.
IP = socket.gethostbyname(socket.gethostname())

# Get Port specified in .env file
PORT = os.environ.get('CHATBOT_PORT')

PUSH_SERVICE_URL = "http://chatbots.q.att.com:19221"
