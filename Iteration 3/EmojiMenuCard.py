"""EmojiMenuCard Bot"""
#Based on EmojiBot, MenuBot, AdaptiveCardValidationBot, AdaptiveCardPizzaBot
from random import choice
from enum import Enum
from typing import Set
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from bottle import run, request, post, HTTPResponse
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE, user_info, get_key_value, set_key_value
from chatbot.config import settings
from chatbot.menu import Reply, Submenu, Url, send_menu
from chatbot.validators import message_is
from chatbot.card import Card, actions, elements, inputs, const
from chatbot.card.exceptions import ValidationError



# String representation of various emoji's.
emojis = [":q_heart:", ":q_hungry:", ":q_happy_dance_low:", ":q_head_spin:", ":q_drum:", ":q_guitar:"]


def get_user_info(payload):
    """returns user info"""
    return user_info(payload.sender)

def default(payload):
    """Returns a default message with an emoji"""
    return f"Type 'start' to see what I can do {choice(emojis)}"

@message_is("start")
def start_message(payload):
    """Returns a welcome message with user and office info as well as emojis"""
    info = get_user_info(payload)
    return f"{choice(emojis)} Hello {info.first_name} from {info.office.state}! Type 'menu' to see the menu or 'order' if you're hungry. {choice(emojis)}"

@message_is("menu")
def menu_message(payload):
    """Send Menu to the sender."""
    # Build Sub-Menu first.
    sm = Submenu("Useful Links", actions=[
        Url("Moose", "https://moose.web.att.com/"),
        Url("HROneStop", "https://www.e-access.att.com/hronestop"),
        Url("WebPhone", "https://webphone.att.com")
    ])

    # Build Menu Actions.
    actions = [
        Reply("ATTUID", "attuid"),
        Reply("Business Unit", "business_unit"),
        Reply("Position", "position"),
        sm  # Include sub-menu in our main menu.
    ]

    # Send Menu to user.
    send_menu(actions, payload.sender)

    return "The Menu has been sent to you."

#Handles messages of the Reply item type of the Menu
@message_is("attuid")
def id_message(payload):
    """return user's attuid"""
    info = get_user_info(payload)
    return f"Your ATTUID is {info.attuid}"

@message_is("business_unit")
def business_unit_message(payload):
    """return user's office address"""
    info = get_user_info(payload)
    return f"Your business unit is {info.business_unit_description}"

@message_is("position")
def position_message(payload):
    """return user's position"""
    info = get_user_info(payload)
    return f"Your supervisor is {info.position_description}"


# create some enums for our choices, we can turn them into choice sets easily
class Size(str, Enum):
    """Size options for ChoiceSet drop-down"""
    six_inch = "Six Inch $5"
    footlong = "Footlong $10"
    submarine = "SUBMARINE $20"

class Toppings(str, Enum):
    """Delivery options for ChoiceSet multi-select"""
    turkey = "Turkey"
    tuna = "Tuna"
    ham = "Ham"
    peppers = "Peppers"
    tomatoes = "Tomatoes"
    olives = "Olives"
    pickles = "Pickles"
    lettuce = "Lettuce"
    cheese = "Cheese"
    cucumbers = "Cucumbers"

class Delivery(str, Enum):
    """Delivery options for ChoiceSet drop-down"""
    pick_up = "Pick Up"
    delivery = "Deliver to Office"


def enum_to_choices(enum):
    """ Takes an enum and creates a list of input choices to select one or many """
    return [inputs.Choice(member.value, member.name) for member in enum]


def out_of_stock_toppings(toppings: Set[str]):
    """Validate all toppings selected are in stock"""
    # you can also have no toppings
    if not toppings:
        return
    errors = []

    # select a few items that are out of stock
    for item in ["cucumbers", "ham"]:
        if item in toppings:
            errors.append(ValidationError(f"{item.title()} is currently out of stock"))

    # we can have multiple out of stock items in our list
    if errors:
        raise ValidationError(errors=errors)


def max_toppings(toppings):
    """Validate the maximum number of toppings"""
    if toppings and len(toppings) > 6:
        raise ValidationError("Can only have 6 toppings")


class OrderSub(Card):
    """ Creates a mini sub ordering form that can be validated in multiple ways """

    size_label = elements.TextBlock("Size")
    size = inputs.ChoiceSet(enum_to_choices(Size), value=Size.six_inch.name)
    toppings_label = elements.TextBlock("Select your toppings, up to 6")
    toppings_price_label = elements.TextBlock(
        "First 3 are free, then $0.50 each", is_subtle=True, size=const.SIZE_SMALL
    )
    toppings = inputs.ChoiceSet(
        enum_to_choices(Toppings),
        is_multi_select=True,
        validator=[out_of_stock_toppings, max_toppings],
    )
    delivery_label = elements.TextBlock("Delivery")
    delivery = inputs.ChoiceSet(enum_to_choices(Delivery), value=Delivery.pick_up.name)
    order = actions.Submit(title="Order")
    # cancel does not validate inputs
    cancel = actions.Submit(title="Cancel", bypass_validation=True)

    def on_order_validate(self, payload, data):
        """ after each input is validated, we can validate the whole card """
        errors = []
        if data.size == Size.submarine.name and data.delivery == Delivery.delivery.name:
            errors.append(ValidationError("We do not deliver submarines"))
        if errors:
            raise ValidationError(errors=errors)

    def on_order(self, payload, data):
        """User pressed order button"""
        info = get_user_info(payload)
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        set_key_value('order_time', order_time)

        order_message = f"Day and Time of order: {order_time}."

        if data.delivery == Delivery.pick_up.name:
            order_message += f" Your pizza will be ready in 30 mins {choice(emojis)}"
        elif data.delivery == Delivery.delivery.name:
            order_message += f" We will arrive at your office located at {info.office.address} in 45 mins"
        else:
            order_message += " Your order is being processed"

        return order_message

    def on_cancel(self, payload, data):
        """User pressed cancel button"""
        return f"Order has been cancelled{emojis[1]}"

    def get_order_time(self):
        """Retrieve the order time"""
        order_time = get_key_value('order_time')
        if order_time:
            return f"Day and Time of order: {order_time}"
        else:
            return "No order time found"

@message_is("order")
def send_card(payload):
    """User entered 'order', so send the card"""
    OrderSub().send(payload.sender)
    return ""


director = MessageDirector(observers=[start_message, id_message, business_unit_message, position_message, menu_message, send_card, OrderSub()], fallback=default)

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
