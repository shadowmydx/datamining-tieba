# -*- coding:utf8 -*-
__author__ = 'wmydx'


from bs4 import BeautifulSoup


# 主贴题目：
# 发言内容：
# 所在贴吧：
# 发言时间：
# 发言地址：
# 发言作者：

class DataItem:

    def __init__(self, content):
        self.host = r'http://tieba.baidu.com'
        self.content = content
        self.result = {}
        self.gen_all_content()

    def __str__(self):
        result_str = '''
        主贴题目： %(title)s\n
        发言内容： %(content)s\n
        所在贴吧： %(tieba)s\n
        发言时间： %(time)s\n
        发言地址： %(addr)s\n
        作者： %(author)s\n
        ''' % self.result
        return result_str

    def get_item_content(self):
        return self.result

    def gen_all_content(self):
        html = BeautifulSoup(self.content)
        self.result['title'] = self.gen_title_from_html(html).strip()
        self.result['content'] = self.gen_content_from_html(html).strip()
        self.result['tieba'] = self.gen_tieba_from_html(html).strip()
        self.result['time'] = self.gen_time_from_html(html).strip()
        self.result['addr'] = self.gen_addr_from_html(html).strip()
        self.result['author'] = self.gen_author_from_html(html).strip()

    def gen_title_from_html(self, html):
        return html.select('.p_title > .bluelink')[0].text

    def gen_content_from_html(self, html):
        local_str = html.select('.p_content')[0].text
        index1 = local_str.find('回复')
        index2 = local_str.find(':')
        if index1 != -1:
            if index2 != -1:
                local_str = local_str[index2 + 1:]
        return local_str

    def gen_tieba_from_html(self, html):
        return html.select('.p_forum > .p_violet')[0].text

    def gen_time_from_html(self, html):
        return html.select('font.p_date')[0].text

    def gen_addr_from_html(self, html):
        return self.host + html.select('.p_title > .bluelink')[0]['href']

    def gen_author_from_html(self, html):
        return html.select('font.p_violet')[1].text

    def get_tieba_part(self):
        return self.result['tieba']


if __name__ == '__main__':
    f = DataItem(r'<div class="s_post"><span class="p_title"><a class="bluelink" href="/p/3733322094?pid=67790123762&amp;cid=#67790123762" target="_blank">回复：【贴吧外交】3D海战《雷霆舰队》,欢迎太平洋战争吧吧友</a></span><div class="p_content">贵司51加班，需不需要法律服务？</div>        贴吧：<a class="p_forum" href="/f?kw=%CC%AB%C6%BD%D1%F3%D5%BD%D5%F9" target="_blank"><font class="p_violet">太平洋战争</font></a>作者：<a href="/i/sys/jump?un=wmydx" target="_blank"><font class="p_violet">wmydx</font></a><font class="p_green p_date">2015-05-01 19:49</font></div>')