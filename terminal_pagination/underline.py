# coding=utf-8
from ansi_colours import AnsiColours as Colour


class Underline:

    @staticmethod
    def create(length):
        return Colour.light_grey("".join(['-' for _ in range(length)]))
