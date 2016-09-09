#! /usr/bin/env python
#coding:utf-8
from fabric.api import *
import datetime,os

yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
env.hosts = ["32.6.11.21", "15.8.29.2"]
env.passwords = {'root@32.6.11.21:22':'12345', 'root@15.8.29.2:22':'12345'}
def total():
        arg = env.host.split('.')[3]
        file = "/data/shell/files/total_" + arg 
        temp_arg = run('zgrep "START CRAWLER TASK" /data/tomcat-8080/logs/catalina.%s.out.gz | wc -l' %yesterday)
        with open(file,'w+') as f:
                f.write(temp_arg)

def success():
        arg = env.host.split('.')[3]
        file = "/data/shell/files/success_" + arg 
        temp_arg = run('zgrep "SUCCESS CRAWLER TASK" /data/tomcat-8080/logs/catalina.%s.out.gz | wc -l' %yesterday)
        with open(file,'w+') as f:
                f.write(temp_arg)

def failed():
        arg = env.host.split('.')[3]
        file = "/data/shell/files/failed_" + arg 
        temp_arg = run('zgrep "FAILED CRAWLER TASK" /data/tomcat-8080/logs/catalina.%s.out.gz | wc -l' %yesterday)
        with open(file,'w+') as f:
                f.write(temp_arg)

def timeout():
        arg = env.host.split('.')[3]
        file = "/data/shell/files/timeout_" + arg 
        temp_arg = run('zgrep "TIMEOUT FOR CRAWLER TASK" /data/tomcat-8080/logs/catalina.%s.out.gz | wc -l' %yesterday)
        with open(file,'w+') as f:
                f.write(temp_arg)

#def time_50():
#       arg = env.host.split('.')[3]
#       file = "/data/shell/files/maxtime_" + arg
#       temp_arg = run('sh /data/shell/cost_50.sh')
#        with open(file,'w+') as f:
#                f.write(temp_arg)
def time_per():
        #arg = env.host.split('.')[3]
        file = "/data/shell/files/cost_all"
        temp_arg = run('zgrep "DO WORK COST" /data/tomcat-8080/logs/catalina.%s.out.gz' %yesterday)
        with open(file,'a+') as f:
                f.write(temp_arg)
