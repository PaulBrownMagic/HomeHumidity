#!/usr/bin/env python3.6
"""Serve Humidity information via Flask"""

from time import time
from flask import Flask, render_template

from redis_connection import RedisConnection

app = Flask(__name__)
rconn = RedisConnection()


@app.route("/")
def home_page():
   humidities = rconn.retrieve(10)
   humidity = round(sum(humidities)/len(humidities), 2)
   #return f"<h1>Humidity {humidity}%</h1>"
   return render_template("index.html")

@app.route("/data")
def humidity_data():
    humidity = rconn.retrieve(1)[0]
    return f'[[{time()},{humidity}]]'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
