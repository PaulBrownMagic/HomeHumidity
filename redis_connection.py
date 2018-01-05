#!/usr/bin/env python3.6
"""Create and share a connection to redis."""
import redis


class RedisConnection:
    """Abstraction to Redis Connection"""

    _HOST = "localhost"
    _PORT = 6379
    _DB = 0
    _HUMIDITY_KEY = "humidity"

    def __init__(self):
        self._conn = redis.StrictRedis(host=self._HOST,
                                       port=self._PORT,
                                       db=self._DB)
        self.lengths = dict()

    def set(self, key, value):
        return self._conn.set(key, value)

    def get(self, key):
        return self._conn.get(key)

    def add(self, value, key=_HUMIDITY_KEY):
        self._conn.ltrim(key, 0, 100)
        length = self._conn.lpush(key, value)
        self.lengths[key] = length
        return length

    def retrieve(self, number=10, key=_HUMIDITY_KEY):
        if number < 1:
            raise ValueError("Can't retrieve less than 1 element")
        res = self._conn.lrange(key, 0, number-1)
        return list(map(float, res))


    def set_humidity(self, value):
        return self.set(self._HUMIDITY_KEY, value)

    def get_humidity(self):
        return float(self.get(self._HUMIDITY_KEY))
