#!/usr/bin/python


class BaseConfig:
    def init(wd: str):
        raise NotImplementedError()

    def reset(wd: str):
        raise NotImplementedError()
