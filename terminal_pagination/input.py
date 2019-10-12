# coding=utf-8


class Input:

    @staticmethod
    def get(*args, **kwargs):
        player_input = input(*args, **kwargs)
        return player_input
