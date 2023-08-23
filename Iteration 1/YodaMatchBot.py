"""YodaChatBot"""
# Dotenv must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE
from chatbot.config import settings
from chatbot.validators import payload_validator

bike_markdown = """I used to have this bike:

![Bike (Alternate Text goes here)](https://target.scene7.com/is/image/Target/GUEST_3b7384b3-d512-4b75-b25e-a6212c24f53c?wid=325&hei=325&qlt=80&fmt=pjpeg)
"""

gym_markdown = """Here are my maxes:

+ Squat
    * 375 lbs
+ Bench
    * 305 lbs
+ Deadlift
    * 500 lbs

"""

code_markdown = """Check this out:


[FreeCodeCamp's website](https://www.freecodecamp.org/)
"""

cook_markdown = """Meals:


| Dishes        | Rating (out of 5)     | Cook Time  |
| ------------- |:---------------------:| ----------:|
| Skillet       | 3                     | Medium     |
| Lasagna       | 5                     | Slow       |
| Stir-Fry      | 4                     | Quick      |
"""

@payload_validator
def contains(phrase, payload):
    """Custom validator to see if message contains the phrase.

    :param phrase: phrase to search for in payload message.
    """
    return phrase in payload.message.lower()

@contains("start")
def start_message(payload):
    """Message contains 'start'"""
    return "Welcome to WordMatchBot! I would love to tell you about some of my hobbies. Type 'help' to see some words I understand!"

@contains("help")
def help_message(payload):
    """Message contains 'help'"""
    return "A few words I know: <br> run <br>bike <br>gym <br>fish <br>code <br>cook"


@contains("run")
def force_message(payload):
    """Message contains 'run'"""
    return "I used to do cross country in highschool, now I run about 15 miles a week just to maintain. I may be running a marathon next year!"


@contains("bike")
def bike_message(payload):
    """Message contains 'bike'"""
    bike_text = "Every now and again I love to go on a nice bike ride. "
    return f"{bike_text}<md>{bike_markdown}</md>"


@contains("gym")
def gym_message(payload):
    """Message contains 'gym'"""
    gym_text = "I've been taking the gym seriously for the past year and a half! I mainly enjoy powerlifting."
    return f"{gym_text}<md>{gym_markdown}</md>"


@contains("fish")
def fish_message(payload):
    """Message contains 'fish'"""
    return "I am still relatively new to fishing so nothing much to say here, I'm really enjoying it though!"


@contains("code")
def code_message(payload):
    """Message contains 'code'"""
    code_text = "I'm currently working to become a software engineer so I've been learning a lot! Let me share a resource! "
    return f"{code_text}<md>{code_markdown}</md>"


@contains("cook")
def cook_message(payload):
    """Message contains 'cook'"""
    cook_text = "I normally don't do anything crazy in the kitchen but here are some of my favorite dishes to make!"
    return f"{cook_text}<md>{cook_markdown}</md>"


def default(payload):
    """Default response"""
    return "Hey! It doesn't look like I understand you, try typing 'help'"



# Set up the message director.
director = MessageDirector(observers=[
    start_message, help_message, force_message, bike_message, gym_message, fish_message,
    code_message, cook_message
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
