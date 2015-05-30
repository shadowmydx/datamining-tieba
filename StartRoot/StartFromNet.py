# -*- coding: utf-8 -*-
__author__ = 'wmydx'

import threading
import Queue
import urllib
import sys
from DataSource import DataFromNet
from DataSource import TiebaHelper
from DataAnalysis import Analysis
from DataBase import DataSaver


class StartFromNet(threading.Thread):

    def __init__(self, user):
        threading.Thread.__init__(self)
        self.user = user
        self.start_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=[tieba]&qw=&rn=30&un=[userid]&sm=1'
        self.end_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=[tieba]&qw=&rn=30&un=[userid]&sm=0'
        self.starting_url = None
        self.ending_url = None
        # self.lock_for_analysis = threading.Condition()
        # self.lock_for_save = threading.Condition()
        self.analysis_thread = None
        self.source_thread = None
        self.save_thread = None
        self.analysis_queue = Queue.Queue(80)
        self.save_data_queue = Queue.Queue(80)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # self.setup_all_thread()

    def gen_init_url(self, tieba_name=''):
        user_id = urllib.quote(self.user)
        tieba_name = urllib.quote(tieba_name)
        self.starting_url = self.start_url.replace('[tieba]', tieba_name)
        self.ending_url = self.end_url.replace('[tieba]', tieba_name)
        self.starting_url = self.starting_url.replace('[userid]', user_id)
        self.ending_url = self.ending_url.replace('[userid]', user_id)

    def setup_all_thread(self, url):
        self.setup_data_source(url)
        self.setup_analysis()
        self.setup_data_saver()

    def setup_data_source(self, url):
        self.source_thread = DataFromNet.FindingPart(url, self.save_data_queue)
        self.source_thread.setDaemon(True)
        self.source_thread.start()

    def setup_analysis(self):
        self.analysis_thread = Analysis.Analysis(self.analysis_queue)
        self.analysis_thread.setDaemon(True)
        self.analysis_thread.start()

    def setup_data_saver(self):
        self.save_thread = DataSaver.DataSaver(self.user, self.save_data_queue, self.analysis_queue)
        # self.save_thread.setDaemon(True)
        self.save_thread.start()

    @staticmethod
    def merge_tieba_set(set1, set2):
        for i in set1:
            if i not in set2:
                set2[i] = i
        return set2

    def run(self):
        self.gen_init_url()
        print 'now catching data from start '
        self.setup_all_thread(self.starting_url)
        self.source_thread.join()
        print 'start is over.'
        tieba_set = self.source_thread.get_all_tieba()
        print 'now catching data from end '
        self.setup_data_source(self.ending_url)
        self.source_thread.join()
        print 'end is over.'
        tieba_set = StartFromNet.merge_tieba_set(tieba_set, self.source_thread.get_all_tieba())
        tieba_set = StartFromNet.merge_tieba_set(tieba_set, TiebaHelper.TiebaHelper.get_all_tieba_from_id(self.user))
        for tieba_name in tieba_set:
            self.gen_init_url(str(tieba_name))
            print self.starting_url
            print self.ending_url
            tieba_data = DataFromNet.FindingPart(self.starting_url, self.save_data_queue)
            print 'now catching data from tieba ' + tieba_name + ' at start:'
            tieba_data.start()
            tieba_data.join()
            tieba_data = DataFromNet.FindingPart(self.ending_url, self.save_data_queue)
            print 'now catching data from tieba ' + tieba_name + ' at end:'
            tieba_data.start()
            tieba_data.join()
        self.save_data_queue.join()
        self.save_thread.working.clear()
        self.analysis_queue.join()
        self.gen_report('report_' + self.user)

    def gen_report(self, filename):
        self.gen_count_report(filename)
        self.gen_rule_report(filename)

    def gen_count_report(self, filename):
        result_str = ''
        f = open('./Report/' + self.user + '_' + filename, 'ab')
        year_dict = self.analysis_thread.get_post_dict()
        for year in year_dict.keys():
            result_str += 'In ' + year + ' year:\n'
            tieba_dict = year_dict[year]
            for tieba in tieba_dict.keys():
                result_str += '  In ' + tieba + ' there are ' + str(tieba_dict[tieba]) + ' posts.\n'
            result_str += '\n'
        print result_str
        f.write(result_str)
        f.close()

    def gen_rule_report(self, filename):
        result_str = ''
        f = open('./Report/' + self.user + '_' + filename, 'ab')
        rules = self.analysis_thread.get_rule_dict()
        for rule in rules:
            result_str += rule + ' rules：\n'
            for data_item in rules[rule]:
                result_str += str(data_item) + '\n'
            result_str += '\n'
        f.write(result_str)
        f.close()


