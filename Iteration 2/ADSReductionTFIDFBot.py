# Based on TF-IDF Chat Bot and Word Reduction Bot
import os
import sys
# Dotenv must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings
from chatbot.validators import payload_validator
from chatbot_utils import AltSyntaxHelper

@payload_validator
def contains(phrase, payload):
    """Custom validator to see if message contains the phrase.

    :param phrase: phrase to search for in payload message.
    """
    return phrase in payload.message.lower()

def message_handler(payload):
    """Handle all messages."""
    message = payload.message

    # Attempt reduction on the message.
    ok = alt.wasReductionSuccessful(message)

    if not ok:
        # Message was NOT reduced successfully.
        # Get the reduced statement which will include the error
        # that occurred during reduction.
        return alt.getReducedStatement()

    # If here, then the message was reduced successfully.
    # Let's get the best response.
    best_response = alt.getBestResponse()

    if best_response:
        # We found a best response.
        return best_response


    # If best_response is None, then the maximum cosine similarity was less than the threshold.
    # Default threshold value is 0.0 in alt.getBestResponse().  You can tune this value based
    # on testing and your document labels.
    # Need to display our default message.
    return f"I am unsure how to respond to '{message}'. Please type 'help'."

# Set up the message director.
director = MessageDirector(observers=[message_handler])


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
    # Get the directory where this Python file resides.
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Load the Alternative Direct Syntax File
    adsFile = os.path.join(dir_path, "ADSGrammar.txt")

    # Initialize AltSyntaxHelper and check the Grammar Syntax
    alt = AltSyntaxHelper()
    goodSyntaxRules = alt.getAndTestGrammarFileSyntax(True, adsFile, "mygroup")

    if not goodSyntaxRules:
        alt.printSyntaxErrorMessagesToConsole()
        sys.exit("There are problems with the grammar file. Please resolve before launching bot again")

    # Grammar File has good syntax, so Register and Start the bot.
    registerAndStartBot()
