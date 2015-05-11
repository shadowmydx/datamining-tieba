# -*- coding:utf8 -*-
__author__ = 'wmydx'


import sqlite3
import threading


class DataSaver(threading.Thread):

    def __init__(self, user_id, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.conn = sqlite3.connect('LocalData/' + user_id + '.db')
        self.init_all_table()

    def init_all_table(self):
        local_cur = self.conn.cursor()
        create_post = '''
        CREATE TABLE IF NOT EXISTS S_POST (
            title TEXT,
            content TEXT,
            tieba TEXT,
            time TEXT,
            addr TEXT PRIMARY KEY NOT NULL,
            author TEXT,
        )
        '''
        local_cur.execute(create_post)

    def get_data_item(self):
        data_item = self.queue.get()
        return data_item

    def store_data_item(self, data_item):
        local_cur = self.conn.cursor()
        local_dict = data_item.get_item_content()
        insert_data = '''
            INSERT INTO S_POST VALUES (
                %(title)s,
                %(content)s,
                %(tieba)s,
                %(time)s,
                %(addr)s,
                %(author)s
            )
        ''' % local_dict
        local_cur.execute(insert_data)

    def run(self):
        while True:
            data_item = self.get_data_item()
            self.store_data_item(data_item)
            self.queue.task_done()
