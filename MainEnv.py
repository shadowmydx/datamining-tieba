# -*- coding:utf8 -*-
__author__ = 'wmydx'

from StartRoot import StartFromNet


class MainEnv:

    def __init__(self):
        pass

    def run(self):
        front_thread = StartFromNet.StartFromNet('wmydx')
        front_thread.start()

MainEnv().run()