# -*- coding:utf8 -*-
__author__ = 'wmydx'

from StartRoot import StartFromNet


class MainEnv:

    def __init__(self):
        pass

    @staticmethod
    def run():
        front_thread = StartFromNet.StartFromNet('')
        front_thread.run()

MainEnv.run()