'''
Goal(s):
- Perform some Word Reduction
- Remove Stop Words
- Remove Basic Plurals forms
- Match on a keyword
- Return an appropriate result (logic can be simple IF&#39;s or Validators)
'''

from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings
from chatbot.validators import payload_validator
from chatbot_utils import PreprocessorStringHelper, Reducer, ReductionEngine

r1 = Reducer("audio|mic|hear|sound|loud|quiet", "microphone")
r2 = Reducer("cam|picture|see", "camera")
re = ReductionEngine([r1, r2])

@payload_validator
def contains(phrase, payload):
    """Custom validator to see if message contains the phrase.

    :param phrase: phrase to search for in payload message.
    """
    return phrase in payload.message.lower()

@contains("start")
def start_message(payload):
    """Message contains 'start'"""
    start_text = "We will be checking your microphone and camera to see if you're on a device that can support virtual calling!"
    start_text_end = "If something is wrong come back and type 'help'"
    return f"{start_text}<a href='https://www.loom.com/webcam-mic-test' target='_blank'>Click here</a>. {start_text_end}"

@contains("help")
def help_message(payload):
    """Message contains 'help'"""
    return "What seems to be the problem? If both your microphone and camera aren't working please type 'both'."

@contains("microphone")
def microphone_message(payload):
    """Message contains 'microphone'"""
    return "If your microphone isn't working try to allow access, else I would recommending using an external mic!"

@contains("camera")
def camera_message(payload):
    """Message contains 'camera'"""
    return "If your camera isn't working then try to allow access in your browser settings."

@contains("both")
def both_message(payload):
    """Message contains 'both'"""
    return "Seems like your device may not be suitable for video calling"

def default(payload):
    """Default response"""
    return "Hey! It doesn't look like I understand you, try typing 'start'"

def message_simplication(payload):
    '''Performs message cleanup'''

    startingPhrase = payload.message.lower()
    startingPhrase = PreprocessorStringHelper.removeDigitsPuncDupsSpaces(startingPhrase)
    stopWords = PreprocessorStringHelper.COMMON_NOISE_PRONOUN_WORDS
    startingPhrase = PreprocessorStringHelper.removeStopWords(startingPhrase, stopWords=stopWords)
    startingPhrase = PreprocessorStringHelper.pluralsToSingular(startingPhrase)


# Set up the message director.
director = MessageDirector(observers=[
    start_message, help_message, microphone_message, camera_message, both_message, message_simplication
],
                           fallback=default)


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
