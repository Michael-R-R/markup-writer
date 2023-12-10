#!/usr/bin/python

# https://en.wikipedia.org/wiki/Jenkins_hash_function
def getHash(text: str) -> int:
    value: int = 0
    for i in text:
        value += ord(i)
        value += value << 10
        value ^= value >> 6

    value += value << 3
    value ^= value >> 11
    value += value << 15

    return value