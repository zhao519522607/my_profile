#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import sys
import time

sys.path.append("../..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gevent import monkey;monkey.patch_all()
import threading, signal
import traceback
import json
import logging
from logger import Logger
import gevent
from gevent.pool import Group
from gevent import getcurrent
import re
from test import MysqlInstance
import threading
import sched
from gevent.queue import Queue,Empty
import copy

DEFAULT_OFFSET          = 5000
DEFAULT_CONCURRENT_FILE = 100

class ReadWriteLock(object):

    def __init__(self):
        self.__monitor = threading.Lock()
        self.__exclude = threading.Lock()
        self.readers = 0

    def acquire_read(self):
        with self.__monitor:
            self.readers += 1
            if self.readers == 1:
                self.__exclude.acquire()

    def release_read(self):
        with self.__monitor:
            self.readers -= 1
            if self.readers == 0:
                self.__exclude.release()

    def acquire_write(self):
        self.__exclude.acquire()

    def release_write(self):
        self.__exclude.release()

class IdMapSql(object):
    def __init__(self,logger=None):
        self._logger   = logger
        self._sql_list = list()

    def write_file(self,file_handle,id_key):
        try:
            if file_handle:
                for item in self._sql_list:
                    info = str(id_key) +":" + item + '\n'
                    file_handle.write(info)
        except:
            self._logger.error(traceback.format_exc())

    """:method:set_sql_to_list 设置id到sql list 组里"""
    def set_sql_to_list(self,sql_str):
        try:
            if sql_str not in self._sql_list:
                self._sql_list.append(sql_str)
        except:
            self._logger.error(traceback.format_exc())

    def remove_all_list(self):
        del self._sql_list[:]

    def get_sqlstr_from_list(self):
        try:
            if len(self._sql_list):
                return self._sql_list.pop()
            return None
        except:
            self._logger.error(traceback.format_exc())

    def show_sql_from_list(self,id):
        try:
            info=None
            for sql_str in self._sql_list:
                info = id + ":" + sql_str
            return info
        except:
            self._logger.error(traceback.format_exc())

    """:method:get_all_sql_from_list 得到对应的id组的全部sql语句"""
    def get_all_sql_from_list(self,id_key,parse_log_handle):
        try:
            info=""
            mysql_handle = None
            is_transaction =False #是否是事务

            if mysql_handle is None:
                mysql_handle = parse_log_handle.get_mysql_handle_from_pool()

            for sql_str in self._sql_list:
                info = id_key + ":" + sql_str

                if info is not None:
                     try:
                            temp_str = sql_str.replace("\n"," ")
                            temp_str = temp_str.replace("\t"," ")

                            pos = temp_str.find("show")

                            if pos == 0:
                                return None,False

                            info_context = "mysql_conn_handle:%d,Greenlet %s,info:%s"%(id(mysql_handle),gevent.getcurrent(),info)

                            row = mysql_handle.execute(temp_str)

                            if row <0:
                                self._logger.error(info_context)
                                if re.search("START TRANSACTION",temp_str):
                                    is_transaction = True
                            else:
                                if re.search("START TRANSACTION",temp_str):
                                    is_transaction = True
                                    print "success, trnas"
                                    break

                                self._logger.info(info_context)
                     except:
                         if re.search("START TRANSACTION",temp_str):
                             is_transaction = True

                         self._logger.error(info_context)
                         mysql_handle.close()

                         return None,is_transaction

            if is_transaction:
                mysql_handle.close()
                mysql_handle = None

            if mysql_handle:
                parse_log_handle.set_mysql_handle_to_pool(mysql_handle)

            return info,is_transaction
        except:
            self._logger.error(traceback.format_exc())

class ParseLog(object):
    def __init__(self,logger=None):
        self._logger = logger
        self._id_map = dict()
        self._serail_num = 0
        self._index  = 0
        self._mutex = threading.Lock()#ReadWriteLock()
        self._mysql_pool = Queue()
        self._group = Group()

    def is_hashid(self,id):
        try:
            if self._id_map.has_key(id):
                return True
            return False
        except:
            self._logger.error(traceback.format_exc())

    """初始化 Mysql 连接池"""
    def init_mysql_pool(self):
        try:
            for i in range(1000):
                mysql_handle = MysqlInstance(self._logger)

                if mysql_handle.init():
                    self._mysql_pool.put(mysql_handle)
        except:
            self._logger.error(traceback.format_exc())

    """从Mysql 连接池返回一个 Mysql 实例"""
    def get_mysql_handle_from_pool(self):
        try:
            mysql_hanle = None
            if self._mysql_pool.qsize() > 0:
                mysql_hanle = self._mysql_pool.get(1)
            else:
                self._mutex.acquire()
                mysql_hanle = MysqlInstance(self._logger)
                mysql_hanle.init()
                self._mutex.release()
            return mysql_hanle
        except:
            self._logger.error(traceback.format_exc())

    """设置 Mysql 实例到连接池里面"""
    def set_mysql_handle_to_pool(self,mysql_handle):
        try:
            if mysql_handle:
                self._mysql_pool.put_nowait(mysql_handle)
        except:
            self._logger.error(traceback.format_exc())

    def init_obj(self,id_key,sql_str):
        try:
             if not self._id_map.has_key(id_key):
                   id_map_sql_obj   = IdMapSql(self._logger)

                   if id_key.isdigit():
                       self._id_map[id_key] = id_map_sql_obj
                       id_map_sql_obj.set_sql_to_list(sql_str.strip())
             else:
                 self.parse_log_data(id_key,sql_str)
        except:
             self._logger.error(traceback.format_exc())

    def write_file(self,file_name):
        try:
            target_file_name = "/data1/fengming/log/general-bak/order_file/" + os.path.basename(file_name)
            target_file_handle = open(target_file_name,'wb')

            for item in self._id_map:
                id_map_obj = self._id_map[item]

                if id_map_obj:
                   id_map_obj.write_file(target_file_handle,item)

            print "target file write success!!!",target_file_name
            target_file_handle.close()
        except:
            self._logger.error(traceback.format_exc())

    def read_file(self,file_name):
        try:
            file_handle = open(file_name, "r")
            begin_time=time.time()

            print "###begin read file:",file_name
            for line in file_handle:
                id_key = (line.strip()).split('!@#$')[0]
                sql_str = (line.strip()).split('!@#$')[1]
                self.init_obj(id_key,sql_str)
            end_time = time.time()
            info = "###read file:%s end! offset_time:%d"%(file_name,end_time-begin_time)
            print info
            self._logger.info(info)
            file_handle.close()
        except:
            self._logger.error(traceback.format_exc())

    """:method:parse_log_data 解析日志数据"""
    def parse_log_data(self,id_key,sql_str):
        try:
            if self._id_map.has_key(id_key):
                id_map_sql_obj = self._id_map[id_key]
                id_map_sql_obj.set_sql_to_list(sql_str.strip())
        except:
            self._logger.error(traceback.format_exc())

    def get_concurrent_parse_log_data(self,n_begin,n_end):
        try:
            id_map_list = self._id_map.keys()
            while True:
                for id_key in id_map_list[n_begin:n_end]:
                    id_map_sql_obj = self._id_map[id_key]
                    if id_map_sql_obj:
                        id_map_sql_obj.get_all_sql_from_list(id_key,self)
                        #id_map_sql_obj.remove_all_list()
        except:
           self._logger.error(traceback.format_exc())

    def process_mysql_concurrent_data(self,file_name):
        try:
            self.read_file(file_name)

            begin_time = time.time()
            nsize    = len(self._id_map)
            n_group  = nsize/DEFAULT_OFFSET #把id分组
            n_offset = nsize%DEFAULT_OFFSET

            if n_offset > 0:
                groups = n_group + 1
            else:
                groups = n_group

            print "groups:",n_group

            for index in range(groups):
                if index == (groups-1):
                    g = gevent.spawn(self.get_concurrent_parse_log_data,index*DEFAULT_OFFSET,index*DEFAULT_OFFSET+n_offset)
                else:
                    g = gevent.spawn(self.get_concurrent_parse_log_data,index*DEFAULT_OFFSET,index*DEFAULT_OFFSET+DEFAULT_OFFSET)
                self._group.add(g)

                print "gevent,index:%d"%(index)

            self._group.join()
            end_time = time.time()
            info_context = "###end parse file,file name%s,offset_time:%d:" % (file_name, end_time - begin_time)

            print info_context
            self._logger.info(info_context)
        except:
           self._logger.error(traceback.format_exc())

    def get_parse_log_data(self,id_map_sql_obj,id_key):
        try:
            if id_map_sql_obj is not None:
                mysql_handle = MysqlInstance(self._logger)
                mysql_handle.init()
                info = id_map_sql_obj.get_all_sql_from_list(id_key,mysql_handle)
                id_map_sql_obj.remove_all_list()
                mysql_handle.close()
        except:
            self._logger.error(traceback.format_exc())

def read_file(file_name,parse_log_handle):
    file_handle = open(file_name,"r")

    count=0
    for line in file_handle:

        if re.search("Connect",line):
            continue

        if re.search("SET NAMES utf8",line):
            continue

        count+=1
        id = (line.strip()).split(' ')[0]

        if re.search("Init DB  orders",line):#"Init DB  orders"
            parse_log_handle.init_obj(id)
        else:
            parse_log_handle.parse_log_data(count,line)

    file_handle.close()

def handler(signalNum,e):
	print "ctrl +c\n"
	sys.exit(0)

def main(dirname,logger=None):

    signal.signal(signal.SIGINT,handler)
    signal.signal(signal.SIGTERM,handler)

    parse_log_handle_list = list()

    # for i in range(DEFAULT_CONCURRENT_FILE):
    #     parse_log_handle = ParseLog(logger.logger)
    #     parse_log_handle.init_mysql_pool()  # 初始化Mysql 连接池
    #     parse_log_handle_list.append(parse_log_handle)

    # parse_log_handle_list_bakcup = copy.copy(parse_log_handle_list)
    # file_list = list()
    #
    # root=None
    # for root,dirs,files in os.walk(dirname):
    #     for file in files:
    #         file_name = root + os.sep + file
    #         file_ext_name  = file_name.split('.')[-1]
    #
    #         if file_ext_name == "log":
    #             file_log = file_name.split('_')[-1]
    #             file_list.append(int(file_log.split('.')[0]))

    parse_log_handle = ParseLog(logger.logger)
    parse_log_handle.init_mysql_pool()  # 初始化Mysql 连接池

    if parse_log_handle is not None:
        parse_log_handle.process_mysql_concurrent_data("/data1/fengming/log/general-bak/order_test/order.log")

    # sort_list = sorted(file_list)
    #
    # n_group  = len(sort_list)/DEFAULT_CONCURRENT_FILE
    # n_offset = len(sort_list)%DEFAULT_CONCURRENT_FILE
    #
    # if n_offset > 0:
    #     n_groups = n_group + 1
    # else:
    #     n_groups = n_group
    #
    # for i in range(n_groups):
    #     if i == n_groups - 1:
    #         begin = i * DEFAULT_CONCURRENT_FILE
    #         end = i * DEFAULT_CONCURRENT_FILE + n_offset
    #     else:
    #         begin = i * DEFAULT_CONCURRENT_FILE
    #         end   = i * DEFAULT_CONCURRENT_FILE + DEFAULT_CONCURRENT_FILE
    #
    #     g_group = Group()
    #
    #     for index in sort_list[begin:end]:
    #         file_name = root + '/' + "general-bak_" + str(index) + ".log"
    #         parse_log_handle = parse_log_handle_list.pop()
    #
    #         if parse_log_handle is not None:
    #             g = gevent.spawn(parse_log_handle.process_mysql_concurrent_data,file_name)
    #             g_group.add(g)
    #
    #         print "gevent",index
    #
    #     g_group.join()
    #     parse_log_handle_list = copy.copy(parse_log_handle_list_bakcup)

if __name__ == '__main__':

    cur_path = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(cur_path, 'log')
    pid_file = os.path.join(cur_path, 'bin/server.pid')

    if not Logger.init(log_path):
        os._exit(1)

    test_info = "/home/fengming/stat/statistics_api_tools/test/test"
    info_test = "/data1/fengming/log/general-bak/general-bak"

    order_info = "/data1/fengming/log/general-bak/order_file"
    order_coll = "/data1/fengming/log/general-bak/order_test"

    main(order_coll,Logger)
