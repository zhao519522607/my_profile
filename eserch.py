#! /usr/bin/env python
#coding:utf-8

import time,os,json
a=0
b=0
c=0
d=0
date = time.strftime('%Y.%m.%d',time.localtime(time.time()))
list = ["DO WORK MONITOR","DO WORK COST", "SUCCESS CRAWLER", "FAILED CRAWLER", "TIMEOUT FAILED CRAWLER", "START CRAWLER"]
for i in list:
    command = '''curl -X GET -s 'localhost:9200/heka-crawler-%s/_search?pretty=true' -d  '
    {
        "from":0, "size":5,
            "query":{
                "match":{
                        "Message": {
                            "query":"%s",
                                "operator":"and"
                            }
                        }
                    }
                }'
    ''' %(date,i)
    #print command
    aa = os.popen(command).read()
    if i == "DO WORK COST":
        a = json.loads(aa)["hits"]["total"]
        print "COST=%s" %a
    elif i == "DO WORK MONITOR":
        b = json.loads(aa)["hits"]["total"]
        print "MONITOR=%s" %b
    elif i == "START CRAWLER":
        c = json.loads(aa)["hits"]["total"]
        print "TOTAL=%s" %c
    else:
        d = json.loads(aa)["hits"]["total"]
        print "%s=%s" %(i.split()[0],d)


print "成功率%.3f %%" % ((a/(c*1.000))*100)


#备用
    #file_name = "file_" + i
    #tmp_file = "/tmp/" + file_name
    #with open(tmp_file,'w+') as f:
    #    f.write(aa)
                                           
