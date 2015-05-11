# -*- coding: utf-8 -*-
__author__ = 'wmydx'

import threading
import Queue
import urllib
from DataSource import DataFromNet
from DataAnalysis import Analysis
from DataBase import DataSaver


class StartFromNet(threading.Thread):

    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user
        self.start_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=&qw=&rn=10&un=[userid]&sm=1'
        self.end_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=&qw=&rn=10&un=[userid]&sm=0'
        self.lock_for_analysis = threading.Condition()
        self.lock_for_save = threading.Condition()
        self.analysis_thread = None
        self.gen_init_url()
        self.analysis_queue = Queue.Queue(40)
        self.save_data_queue = Queue.Queue(40)
        # self.setup_all_thread()

    def gen_init_url(self):
        user_id = urllib.quote(self.user)
        self.start_url = self.start_url.replace('[userid]', user_id)
        self.end_url = self.end_url.replace('[userid]', user_id)

    def setup_all_thread(self, url):
        self.setup_data_source(url)
        self.setup_analysis()
        self.setup_data_saver()

    def setup_data_source(self, url):
        DataFromNet.FindingPart(url, (self.analysis_queue, self.save_data_queue),
                                (self.lock_for_analysis, self.lock_for_save)).setDaemon(True).start()

    def setup_analysis(self):
        self.analysis_thread = Analysis.Analysis(self.analysis_queue)
        self.analysis_thread.setDaemon(True).start()

    def setup_data_saver(self):
        DataSaver.DataSaver(self.user, self.save_data_queue).setDaemon(True).start()

    def run(self):
        self.lock_for_save.acquire()
        self.lock_for_analysis.acquire()
        self.setup_all_thread(self.start_url)
        self.lock_for_analysis.wait()
        self.lock_for_save.wait()

        self.gen_report('start')

        self.lock_for_save.acquire()
        self.lock_for_analysis.acquire()
        self.setup_all_thread(self.end_url)
        self.lock_for_analysis.wait()
        self.lock_for_save.wait()

        self.gen_report('end')

    def gen_report(self, filename):
        self.gen_rule_report(filename)
        self.gen_count_report(filename)

    def gen_count_report(self, filename):
        result_str = ''
        f = open('../Report/' + self.user + '_' + filename, 'a+')
        year_dict = self.analysis_thread.get_post_dict()
        for year in year_dict.keys():
            result_str += 'In ' + year + 'year:\n'
            tieba_dict = year_dict[year]
            for tieba in tieba_dict.keys():
                result_str += '  In ' + tieba + ' there is ' + tieba_dict[tieba] + ' posts.\n'
            result_str += '\n'
        f.write(result_str)
        f.close()

    def gen_rule_report(self, filename):
        result_str = ''
        f = open('../Report/' + self.user + '_' + filename, 'a+')
        rules = self.analysis_thread.get_rule_dict()
        for rule in rules:
            result_str += rule + ' rules：\n'
            for data_item in rules[rule]:
                result_str += str(data_item) + '\n'
            result_str += '\n'
        f.write(result_str)
        f.close()



