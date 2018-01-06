#!/usr/bin/env python3.6
"""Serve Humidity information via Flask"""

from flask import Flask, render_template, session
from os import urandom

from redis_connection import RedisConnection

app = Flask(__name__)
rconn = RedisConnection()

@app.route("/")
def home_page():
    # humidities = rconn.retrieve(10)
    # humidity = round(sum(humidities)/len(humidities), 2)
    # return f"<h1>Humidity {humidity}%</h1>"
    return render_template("index.html")


@app.route("/data")
def humidity_data():
    if "count" in session:
        c = session["count"]
    else:
        c = 100
        session["count"] = c
    humidity = rconn.retrieve(100)
    return str([[x, h] for x, h in zip(range(c-100, c), humidity)])


@app.route("/dataUpdate")
def humidity_data_update():
    session["count"] += 1
    humidity = rconn.retrieve(1)[0]
    return f'[[{session["count"]}, {humidity}]]'

if __name__ == "__main__":
    app.secret_key = urandom(24)
    app.run(host='0.0.0.0', debug=True)
