# coding=utf-8
from ansi_colours import AnsiColours as Colour


class Underline:

    @staticmethod
    def create(title):
        return Colour.light_grey("".join(['-' for _ in range(len(title))]))
