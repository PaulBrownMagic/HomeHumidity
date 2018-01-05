#!/usr/bin/env python3.6
"""Read humidity values and put them onto redis queue"""


from daemon import DaemonContext
from sense_hat import SenseHat
from time import sleep

from redis_connection import RedisConnection


class Humidity_Generator:
    "Read humidity data and push to redis as a daemon."""

    interval = 1
    stdin_path = "/dev/null"
    stdout_path = "/dev/null"
    stderr_path = "/tmp/humidity_gen_err.txt"
    pidfile_path = "/tmp/humidity_gen.pid"
    pidfile_timeout = 5

    def __init__(self, sensor, conn):
        self.sense = sensor
        self.conn = conn

    def run(self):
        while True:
            self.conn.add(self.sense.humidity)
            sleep(self.interval)


if __name__ == "__main__":
    app = Humidity_Generator(SenseHat(), RedisConnection())
    with DaemonContext():
        app.run()
