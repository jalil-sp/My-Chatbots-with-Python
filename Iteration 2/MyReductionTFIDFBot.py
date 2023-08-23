'''
Goal(s):
- Create a custom preprocessor function that uses reductions
- Pass your custom preprocessor function to getTFIDFcosineBestResponse
- Return the best response to the user, or a default response if no best response is found
'''

# Dotenv must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings
from chatbot.validators import payload_validator
from chatbot_utils import PreprocessorStringHelper, Reducer, ReductionEngine

r1 = Reducer("audio|microphone|hear|sound|loud|quiet", "mic")
r2 = Reducer("camera|picture|see", "cam")
re = ReductionEngine([r1, r2])

@payload_validator
def contains(phrase, payload):
    """Custom validator to see if message contains the phrase.

    :param phrase: phrase to search for in payload message.
    """
    return phrase in payload.message.lower()


start_text = "We will be checking your microphone and camera to see if you're on a device that can support virtual calling!"
start_text_end = "if something is wrong come back and type 'help'."


# Dictionary with keys as what we will compare the user's message to using
# TF-IDF and cosine similarity, and the values as our response if there is a match.
response_dict = {
    "microphone": "If your microphone isn't working try to allow access, else I would recommending using an external mic!",
    "camera": "If your camera isn't working then try to allow access in your browser settings",
    "help": "Type 'start'",
    "both": "Seems like your device may not be suitable for video calling",
    "start": f"{start_text} <a href='https://www.loom.com/webcam-mic-test' target='_blank'> Click here</a>, {start_text_end}"
}

def message_handler(payload):
    """Handle all messages."""
    startingPhrase = payload.message.lower()
    startingPhrase = PreprocessorStringHelper.removeDigitsPuncDupsSpaces(startingPhrase)
    stopWords = PreprocessorStringHelper.COMMON_NOISE_PRONOUN_WORDS
    startingPhrase = PreprocessorStringHelper.removeStopWords(startingPhrase, stopWords=stopWords)
    startingPhrase = PreprocessorStringHelper.pluralsToSingular(startingPhrase)
    best_response = PreprocessorStringHelper.getTFIDFcosineBestResponse(docs=response_dict,
                                               query=startingPhrase,
                                               # threshold=0.0,  # By default threshold is 0.0; you can adjust this as-needed.
                                               preprocessor=re.reduce,
                                               echoOn=True)

    if best_response:
        return f"<br/>{best_response}"
    else:
        return f"I am unsure how to respond to '{startingPhrase}'.  Please type 'help'."


# Set up the message director.
director = MessageDirector(observers=[ message_handler])


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
