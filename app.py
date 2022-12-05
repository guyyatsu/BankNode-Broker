#!/bin/python3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from functionality import *


app= Flask(__name__)
socket= SocketIO(app)


@socket.on("connect")
def ack():
  # Acknowledge the clients presence.
  # 


@app.route("/<StockSymbol>/<StartDate>/<EndDate>")
def DeliverGraph(StockSymbol, StartDate, EndDate):
  # Convert StartDate and EndDate to UNIX timestamp.
  StartDate= ConvertToTimestamp(str(StartDate))
  EndDate= ConvertToTimestamp(str(EndDate))

  # Select all .db entries between START and END.
  cursor.execute( "SELECT * FROM ? WHERE start_date >= ? AND end_date <= ?",
                  ( StockSymbol, StartDate, EndDate )                        )

  # Feed results into matplotlib.Figure()
  # Send results to client as an event.


