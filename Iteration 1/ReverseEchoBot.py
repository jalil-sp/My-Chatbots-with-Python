'''
Goal(s):
- Copy MyEchoBot.py to ReverseEchoBot.py
- Customize ReverseEchoBot.py to reverse the received message in some form (reverse
the letters, reverse the word order, etc.)
'''

# Dotenv must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings


def echo_message(payload):
    """Echo the message back to the sender."""
    #reversing word order
    sep = payload.message.split()
    reversal = ' '.join(reversed(sep))
    #mirroring word
    #mirror = payload.message[::-1]

    return f"Hello {payload.sender} you said \"{reversal}\""


# Set up the message director.
director = MessageDirector(observers=[echo_message])


@post("/")
def index():
    """Handles POST requests to our Chatbot.
    This function:
        1) Converts the incoming data into the correct version of payload.
        2) Sends the payload to the Message Director to handle with
            the appropriate observer.
        3) Sends the response from the observer back to the user.
    """
    payload = parse_payload(request.headers, request.json)
    status, message = director.handle(payload)
    return HTTPResponse(status=status, body=message)


def registerAndStartBot():
    """This performs the necessary setup and starts the Chatbot.

    1) Register the URL (HTTP/HTTPS, IP, and port) of the machine the
        chatbot is running on with the Chatbot servers. When messages
        arrive at the Chatbot servers for your bot, they will send
        them to the registered URL.

    2) Sets the bot presence and status.

    3) Starts the local server that responds to incoming messages.
    """
    # Register IP address so Chatbot Service knows where to find your bot.
    register_url(settings.IP)

    # Set the presence and status message.
    set_presence(AVAILABLE, "Python-Powered Q")

    # Start the bottle server. After this starts, your bot
    # should be able to receive messages.
    run(host="0.0.0.0", port=settings.PORT, debug=True)


if __name__ == "__main__":
    registerAndStartBot()
