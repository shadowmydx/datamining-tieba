# -*- coding:utf8 -*-
__author__ = 'wmydx'

from StartRoot import StartFromNet


class MainEnv:

    def __init__(self):
        pass

    @staticmethod
    def run():
        front_thread = StartFromNet.StartFromNet('二吧丧尸')
        front_thread.run()

MainEnv.run()