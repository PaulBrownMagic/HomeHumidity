# Home Humidity Monitor with Raspberry Pi and Sense Hat

This collection of applications use the Sense Hat to gather humidity readings
and then makes them available for display on the Sense Hat or via a local
web app.

## Requirements

- Raspberry Pi to run the processes on, preferably a model with multiple cores.
- Sense Hat, required for the humidity sensor, LED display and JoyStick input.
- Redis Server, Uses an in memory data store to avoid writes to the SD card.
Should be configured to not save to disk (comment out three save lines in
/etc/redis/redis.conf). Can be installed with 'sudo apt install redis-server'
- flask, web framework for flask_humidty.py
- python-daemon to run humidity_gen in daemon mode
