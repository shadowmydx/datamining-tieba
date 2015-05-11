# -*- coding: utf-8 -*-
__author__ = 'wmydx'


import threading


class Finish(threading.Thread):

    def __init__(self, queue, condition):
        threading.Thread.__init__(self)
        self.condition = condition
        self.queue = queue

    def run(self):
        self.queue.join()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()
