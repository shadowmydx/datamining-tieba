# -*- coding:utf8 -*-
__author__ = 'wmydx'

from Rule import Rules
import threading


class Analysis(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = None
        self.rule_list = Rules().get_rule_list()
        self.rule_dict = dict()
        for rule in self.rule_list:
            self.rule_dict[rule.get_description()] = []
        self.post_dict = dict()

    def setup_blocking_queue(self, queue):
        self.queue = queue

    def get_data_item(self):
        data_item = self.queue.get()
        return data_item

    def parse_rule(self, data_item):
        for rule in self.rule_list:
            if rule.judge_input(data_item):
                self.rule_dict[rule.rule.get_description()].append(data_item)

    def count_post(self, data_item):
        post_time = data_item.get_item_content()['time']
        post_tieba = data_item.get_item_content()['tieba']
        post_time = post_time[:post_time.find('-')]  # get year in time
        if post_time in self.post_dict.keys():
            if post_tieba in self.post_dict[post_time].keys():
                self.post_dict[post_time][post_tieba] += 1
            else:
                self.post_dict[post_tieba][post_tieba] = 1
        else:
            self.post_dict[post_time] = dict()
            self.post_dict[post_time][post_tieba] = 1
            
    def run(self):
        if self.queue is None:
            raise NameError, 'Analysis module need a queue to read data!'
        while True:
            data_item = self.get_data_item()
            self.parse_rule(data_item)
            self.count_post(data_item)
            self.queue.task_done()



