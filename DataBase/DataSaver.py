# -*- coding:utf8 -*-
__author__ = 'wmydx'


import sqlite3
import threading


class DataSaver(threading.Thread):

    def __init__(self, user_id, consume_queue, producer_queue):
        threading.Thread.__init__(self)
        self.consume_queue = consume_queue
        self.producer_queue = producer_queue
        self.user_id = user_id
        self.all_post = 0
        self.conn = None
        self.working = threading.Event()
        self.working.set()

    def init_all_table(self):
        local_cur = self.conn.cursor()
        create_post = '''
        CREATE TABLE IF NOT EXISTS S_POST (
            title TEXT,
            content TEXT,
            tieba TEXT,
            time TEXT,
            addr TEXT PRIMARY KEY NOT NULL,
            author TEXT
        );
        '''
        local_cur.execute(create_post)

    def get_data_item(self):
        data_item = self.consume_queue.get()
        return data_item

    def store_data_item(self, data_item):
        local_cur = self.conn.cursor()
        local_dict = data_item.get_item_content()
        for key in local_dict:
            local_dict[key] = local_dict[key].replace('"', '[.]')
            local_dict[key] = local_dict[key].replace("'", "[.]")
        insert_data = '''
            INSERT INTO S_POST VALUES (
                '%(title)s',
                '%(content)s',
                '%(tieba)s',
                '%(time)s',
                '%(addr)s',
                '%(author)s'
            );
        ''' % local_dict
        try:
            local_cur.execute(insert_data)
            self.producer_queue.put(data_item)
            self.all_post += 1
        except sqlite3.IntegrityError:
            pass
        except sqlite3.OperationalError:
            print insert_data

    def turn_off_connection(self):
        print 'success'
        print 'There are ' + str(self.all_post) + ' posts.'
        self.conn.commit()
        self.conn.close()

    def run(self):
        self.conn = sqlite3.connect('./LocalData/' + self.user_id + '.db')
        self.init_all_table()
        while self.working.is_set():
            if self.consume_queue.empty():
                continue
            data_item = self.get_data_item()
            self.store_data_item(data_item)
            self.consume_queue.task_done()
        self.turn_off_connection()
