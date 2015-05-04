# -*- coding:utf8 -*-
__author__ = 'wmydx'

import urllib
import Queue


class MainEnv:

    def __init__(self, user):
        self.user = user
        self.start_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=&qw=&rn=10&un=[userid]&sm=1'
        self.end_url = r'http://tieba.baidu.com/f/search/ures?ie=utf-8&kw=&qw=&rn=10&un=[userid]&sm=0'
        self.gen_init_url()

    def gen_init_url(self):
        user_id = urllib.quote(self.user)
        self.start_url = self.start_url.replace('[userid]', user_id)
        self.end_url = self.end_url.replace('[userid]', user_id)
        print self.end_url
        print self.start_url


if __name__ == '__main__':
    test = MainEnv('wmydx')
    test.gen_init_url()
