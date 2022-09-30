#!/bin/python3
from sys import path
from flask import Flask

# Define the logfile.
logging.basicConfig(filename=f"{CWD()}/.logfile", encoding="utf-8", level=logging.DEBUG)

# Bring in the core functionality.
from functionality import *

# The AlpacaAPI is what drives our brokerage; this is how we interface with it.
from AlpacaAPI import *

broker = Flask(__name__)

@broker.route("/")
@broker.route("/home")
""" Provide a little bit of detail explaining this section of the
domain in greater, less technical, depth. """

@broker.route("/login")
""" Allow someone who already knows they have an account to attempt
to sign in using an html form. """

@broker.route("/signup")
""" Create a new user from scratch;
requires a market key & secret beforehand. """

@broker.route("/home/{username}")
""" The user's home space; where they can get a quick overview of their
holdings. """

@broker.route("/positions/{username}")
""" Pie-Charts for breaking down exactly what a user has, their P/L, and
the average price for what they've got. """

@broker.route("/orders/{username}")
""" Display any outstanding limit/stop orders the user may have in play. """

@broker.route("/charts/{username}")
""" Report the user and their bot's performance over time. """