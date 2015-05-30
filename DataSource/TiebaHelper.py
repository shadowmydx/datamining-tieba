# -*- coding: utf-8 -*-
__author__ = 'wmydx'

import urllib2
from bs4 import BeautifulSoup


class TiebaHelper:

    url = 'http://tieba.baidu.com/home/main/?un=[userid]&ie=utf-8&fr=frs'

    def __init__(self):
        pass

    @staticmethod
    def get_all_tieba_from_id(user_id):
        local_url = TiebaHelper.url.replace('[userid]', user_id)
        tieba_html = urllib2.urlopen(local_url).read()
        tieba_soup = BeautifulSoup(tieba_html)
        res = dict()
        result = []
        local_tmp = tieba_soup.select('a.u-f-item')
        for item in local_tmp:
            if 'title' not in item.attrs:
                for key in item.select('span'):
                    result.append(key)
            else:
                res[item['title']] = item['title']
        for item in [key for key in result if 'class' not in key.attrs]:
            res[item.text] = item.text
        return res


if __name__ == '__main__':
    a = TiebaHelper.get_all_tieba_from_id('二吧丧尸')
    for i in a:
        print i