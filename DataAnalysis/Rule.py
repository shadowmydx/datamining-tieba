# -*-coding:utf8-*-
__author__ = 'wmydx'


import re
import DataSource.DataItem


class Rules:

    def __init__(self):
        self.rule_list = []
        self.gen_all_rule()

    def gen_all_rule(self):
        self.rule_list.append(NumberRule())
        self.rule_list.append(IpAddrRule())
        self.rule_list.append(GraduateRule())
        self.rule_list.append(EmailRule())
        self.rule_list.append(UniversityRule())
        self.rule_list.append(SchoolRule())
        self.rule_list.append(GradeRule())
        self.rule_list.append(PrivateRule())
        self.rule_list.append(AccountRule())

    def get_rule_list(self):
        return self.rule_list


class Rule:

    def __init__(self):
        self.description = ''
        self.pattern = None

    def get_description(self):
        return self.description

    def judge_input(self, data_item):
        return True


class ReRule(Rule):

    def judge_input(self, data_item):
        local_content = data_item.get_item_content()
        local_res = self.pattern.search(local_content['content'])
        if local_res:
            return True
        local_res = self.pattern.search(local_content['title'])
        if local_res:
            return True
        local_res = self.pattern.search(local_content['tieba'])
        if local_res:
            return True
        return False


class StrRule(Rule):

    def judge_input(self, data_item):
        local_content = data_item.get_item_content()
        for key in self.pattern:
            local_res = local_content['content'].find(key)
            if local_res != -1:
                return True
            local_res = local_content['title'].find(key)
            if local_res != -1:
                return True
            local_res = local_content['tieba'].find(key)
            if local_res != -1:
                return True
            return False


class NumberRule(ReRule):

    def __init__(self):
        ReRule.__init__(self)
        self.description = 'Number Rule'
        self.pattern = re.compile(r'\d\d\d\d(\d+)')


class IpAddrRule(ReRule):

    def __init__(self):
        ReRule.__init__(self)
        self.description = 'IP Address Rule'
        self.pattern = re.compile(r'(\d+)[.](\d+)[.](\d+)[.](.*)')

    def judge_input(self, data_item):
        local_content = data_item.get_item_content()
        local_res = self.pattern.search(local_content['author'])
        if local_res:
            return True
        else:
            return False


class GraduateRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'Graduate Rule'
        self.pattern = [u'毕业']


class EmailRule(ReRule):

    def __init__(self):
        ReRule.__init__(self)
        self.description = 'Email Rule'
        self.pattern = re.compile(r'([^@]+)@([^@]+)[.]([^@]+)')


class UniversityRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'University Rule'
        self.pattern = [u'大学', u'考研', u'论文', u'职校', u'报考', u'高考', u'本科', u'硕士', u'博士', u'专科', u'职高']


class SchoolRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'School Rule'
        self.pattern = [u'学校', u'中学', u'高中', u'母校', u'鄙校', u'初中']


class GradeRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'Grade Rule'
        self.pattern = [u'大一', u'大二', u'大三', u'大四', u'高一', u'高二', u'高三', u'初一', u'初二', u'初三']


class PrivateRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'Private Rule'
        self.pattern = [u'求种', u'发种']


class AccountRule(StrRule):

    def __init__(self):
        StrRule.__init__(self)
        self.description = 'AccountRule'
        self.pattern = [u'微博', u'微信', u'帐号', u'知乎', u'小号', u'解封', u'大号']


def show_item(item):
    for i in item:
        print 'dict[%s]=' % i, item[i]
    print

if __name__ == '__main__':
    test_list = Rules().get_rule_list()
    item = DataSource.DataItem.DataItem(r'<div class="s_post"><span class="p_title"><a class="bluelink" href="/p/3733322094?pid=67790123762&amp;cid=#67790123762" target="_blank">回复：【贴吧外交】3D海战《雷霆舰队》,欢迎太平洋战争吧吧友</a></span><div class="p_content">贵司51加班，需不需要法律服务？</div>        贴吧：<a class="p_forum" href="/f?kw=%CC%AB%C6%BD%D1%F3%D5%BD%D5%F9" target="_blank"><font class="p_violet">太平洋战争</font></a>作者：<a href="/i/sys/jump?un=wmydx" target="_blank"><font class="p_violet">wmydx</font></a><font class="p_green p_date">2015-05-01 19:49</font></div>')
    result = item.get_item_content()
    result['title'] = u'题目'
    result['content'] = u'我电话是13dddsdsdf，今年大学毕业,邮箱是dddddd@gmail.com'
    # result['tieba'] = ''
    # result['time'] = ''
    # result['addr'] = ''
    result['author'] = 'ddds'
    for rule in test_list:
        if rule.judge_input(item):
            print rule.get_description() + ': '
            show_item(result)
