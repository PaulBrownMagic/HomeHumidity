#!/usr/bin/env python3.6
"""Read Humidity from Redis Queue and make display on SenseHat"""

from numpy import zeros, reshape
from sense_hat import SenseHat, ACTION_PRESSED
from signal import pause
from time import sleep

from redis_connection import RedisConnection


class Display:
    """Controls the SenseHat LEDs to display humidity"""

    colours = [(255,   0,   0),  # 0
               (255,  80,   0),  # 1
               (255, 165,   0),  # 2
               (255, 255,   0),  # 3
               (165, 255,   0),  # 4
               (0, 255,   0),  # 5
               (0, 165, 255),  # 6
               (0,   0, 255)]  # 7
    step = 12.5

    def __init__(self, display, conn):
        self.display = display
        self.conn = conn
        self.display.stick.direction_up = self.graph
        self.display.stick.direction_down = self.graph
        self.display.stick.direction_left = self.show_humidity
        self.display.stick.direction_right = self.show_humidity

    def avg_humidity(self, duration):
        recent_humidity = self.conn.retrieve(duration)
        return sum(recent_humidity)/len(recent_humidity)

    def make_graph(self):
        leds = zeros([8, 8, 3], dtype=int)
        humidity = self.avg_humidity(10)
        for i, colour in enumerate(self.colours):
            if humidity > i * self.step:
                leds[7-i, :, :] = colour
        return reshape(leds, [64, 3])

    def show_humidity(self, event):
        if event.action == ACTION_PRESSED:
            humidity = round(self.avg_humidity(10))
            self.display.show_message(f"{humidity}%")
            self.display.clear()

    def graph(self, event):
        if event.action == ACTION_PRESSED:
            for _ in range(30):
                leds = self.make_graph()
                self.display.set_pixels(leds)
                sleep(1)
            self.display.clear()


if __name__ == "__main__":
    display = Display(SenseHat(), RedisConnection())
    pause()
