#! /usr/bin/env python
#coding:utf-8

'''
author by: zyb
create time: 2015-9-24
'''

import os,re,sys


with open(test.log,'r+') as f:
        lines = f.readlines()
        for line in lines:    
                phone = re.compile(r'loginName=[0-9]\{11\}.*"retMsg":"您办理了详单禁查业务，因此不能查询详单，感谢您使用中国移动网上商城"')
                match = phone.findall(line)
