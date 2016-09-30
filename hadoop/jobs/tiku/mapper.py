#!/usr/bin/env python
#!coding: utf-8

import os,sys
import json
import re
import time
reload(sys)
sys.setdefaultencoding("utf-8")

class Strategy():
    def __init__(self):
        self.record = {}

    def threadInit(self):
        self.record = {}

    def threadDestroy(self):
        pass
    
    def set(self, key, value):
        self.record[key] = value

    def get(self, key):
        if self.record.has_key(key):
            return self.record[key]
        else:
            return None

    def run(self, s):
        for line in sys.stdin:
            self.threadInit()
            self.parseLine(line)
            flag = s.process()
            if flag == 1:
                self.writeBck()
            self.threadDestroy()

    def parseLine(self, line):
        line = line.strip()
        f = line.split('')
        if len(f) != 6:
            return None
        id = f[0]
        cls = f[1]
        content = json.loads(f[2])
        source = f[3]
        update_time = f[4]
        taskid = f[5]
        self.record['id'] = id
        self.record['class'] = cls
        self.record['content'] = content
        self.record['source'] = source
        self.record['update_time'] = update_time
        self.record['taskid'] = taskid
    
    def writeBck(self):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        update_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
        self.record['update_time'] = update_time
        id = self.record['id']
        cls = self.record['class']
        content = self.record['content']
        source = self.record['source']
        update_time = self.record['update_time']
        taskid = self.record['taskid']
        print '%s%s%s%s%s%s' %(id, cls, json.dumps(content), source, update_time, taskid)


class TestStrategy(Strategy):
    def process(self):
        cls = self.get('class')
        if cls == '8':
            return 1
        else:
            return 0

class TikuStrategy(Strategy):
    def process(self):
        record_new = {}
        content_dict = self.record['content']
        record_new['title'] = content_dict['title']
        record_new['url'] = content_dict['url']
        record_new['id'] = self.record['id']
        record_new['class'] = '35'
        record_new['source'] = self.record['source']
        record_new['update_time'] = self.record['update_time']
        record_new['question'] = content_dict['title']
        record_new['analyse'] = content_dict['analyse']
        record_new['result'] =content_dict['answer']
        record_new['subject'] = content_dict['subject']
        self.record['content'] = record_new
        return 1

if __name__=='__main__':
    #s = TestStrategy()
    s = TikuStrategy()
    s.run(s)
