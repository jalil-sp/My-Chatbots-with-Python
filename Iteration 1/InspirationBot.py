'''
Goal(s):
- Create bot that responds with a random Quote, Joke, Inspirational Message, Song, etc.
'''

from random import choice

# Must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings

def message_handler(payload):
    """Respond with random motivational quote"""
    replies = ["'Do one thing every day that scares you.' ―Eleanor Roosevelt",
    "'Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart.' ―Roy T. Bennett",
    "'Keep your face always toward the sunshine―and shadows will fall behind you.' ―Walt Whitman",
    "'If you obey all the rules, you miss all the fun.' ―Katharine Hepburn",
    "'Never regret anything that made you smile.' ―Mark Twain"]
    return f"Motivational Quote of the Day: {choice(replies)}"


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
    registerAndStartBot()
