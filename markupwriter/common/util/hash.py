#!/usr/bin/python

class Hash(object):
    # https://en.wikipedia.org/wiki/Jenkins_hash_function
    def compute(text: str) -> int:
        value: int = 0
        for i in text:
            value += ord(i)
            value += value << 10
            value ^= value >> 6

        value += value << 3
        value ^= value >> 11
        value += value << 15

        return value