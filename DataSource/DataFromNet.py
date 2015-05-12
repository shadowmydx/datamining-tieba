# -*- coding: utf-8 -*-
__author__ = 'wmydx'

import urllib2
import threading
import re
from bs4 import BeautifulSoup

import DataItem
from DataAnalysis import Rule
from FinishFlag import Finish


class FindingPart(threading.Thread):
    # 时间顺序还是逆序，由上层处理。
    def __init__(self, start_url, queues, locks):
        threading.Thread.__init__(self)
        self.rule_list = Rule.Rules().get_rule_list()
        self.url = start_url
        self.if_repeat = ''  # 使用该变量来标记动态产生的百度地址是否重复
        self.host = r'http://tieba.baidu.com'
        self.pattern = re.compile(r'pn=(?P<page>\d+)')
        self.queues = queues
        self.locks = locks

    def get_html_content(self):
        content = urllib2.urlopen(self.url).read()
        return content

    def run(self):
        count = 1
        if self.queues is None:
            raise NameError, 'U have not setup queue yet!'
        while True:
            print 'start a new ' + str(count) + ' page..'
            html = self.get_html_content()
            html = BeautifulSoup(html, 'html5')  # http://stackoverflow.com/questions/16316793/beautifulsoup-lost-nodes
            try:
                self.url = self.host + html.select('a.next')[0]['href']
            except IndexError:
                self.url = self.gen_hide_url()
            item_list = html.find_all('div', class_='s_post')
            try:
                item_string = item_list[0].__str__()
            except IndexError:
                break
            if item_string == self.if_repeat:
                break
            else:
                self.if_repeat = item_string
            for item in item_list:
                item_string = item.__str__()
                data_item = DataItem.DataItem(item_string)
                self.put_data_to_queue(data_item)
            count += 1
        finish1 = Finish.Finish(self.queues[0], self.locks[0])
        finish1.setDaemon(True)
        finish1.start()
        finish2 = Finish.Finish(self.queues[1], self.locks[1])
        finish2.setDaemon(True)
        finish2.start()

    def gen_hide_url(self):
        pages = self.pattern.search(self.url)
        next_page = int(self.url[pages.start('page'):pages.end('page')]) + 1
        return self.url[:pages.start('page')] + str(next_page)

    def put_data_to_queue(self, item):
        # for rule in self.rule_list:
        #     if rule.judge_input(item):
        #         print rule.get_description() + ': '
        #         show_item(item)
        for queue in self.queues:
            queue.put(item)

    def show_item(self, item):
        local_dict = item.get_item_content()
        for i in local_dict:
            print 'dict[%s]=' % i, local_dict[i]


