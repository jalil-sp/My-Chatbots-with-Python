"""Adaptive Card Pizza Card Example.

Example from Python SDK:
https://docs.q.att.com/python/chatbot-sdk-rc/tutorials/examples.html#pizza-card

Slight modifications made for CELL Training.
"""
# Copyright (c) 2020. AT&T Knowledge Ventures. All rights reserved.
# Bot using an adaptive card featuring handling submit and input validation.

from enum import Enum
from typing import Set

# Dotenv must be called before importing chatbot.config.settings
from dotenv import load_dotenv
load_dotenv()

from bottle import post, request, run, HTTPResponse
from chatbot.card import Card, actions, elements, inputs, const
from chatbot.card.exceptions import ValidationError
from chatbot.config import settings
from chatbot.director import MessageDirector
from chatbot.payload import parse_payload
from chatbot.services import register_url, set_presence, AVAILABLE, user_info, get_key_value, set_key_value
from chatbot.validators import message_is
from datetime import datetime

def get_user_info(payload):
    """returns user info"""
    return user_info(payload.sender)

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
            order_message += " Your pizza will be ready in 30 mins"
        elif data.delivery == Delivery.delivery.name:
            order_message += f" We will arrive at your office located at {info.office.address} in 45 mins"
        else:
            order_message += " Your order is being processed"

        return order_message

    def on_cancel(self, payload, data):
        """User pressed cancel button"""
        # Set the cancellation time
        return "Order has been cancelled"

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


def help_message(payload):
    """Fallback message"""
    return "Type 'order' to begin your order"


director = MessageDirector(observers=[send_card, OrderSub()], fallback=help_message)



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
