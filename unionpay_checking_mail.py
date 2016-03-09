#! /usr/bin/env python
#coding:utf-8
import MySQLdb
import smtplib  
import sys,os,csv
import urllib  
import urllib2  
from email.mime.text import MIMEText
from time import gmtime, strftime
import datetime 
reload(sys) 
sys.setdefaultencoding("utf-8") 
path=os.path.dirname(os.path.abspath(__file__))
csv_dir= path + "/table/"
sql_file="unionpay_checking.sql"
no_clients="(27528,27529,27537,27538,27539,27543,27546,27551,27461,27524)"
template_file="template"
base_file="unionpaybase.html"
log_file="statistical.log"
score=0.0
blacklist="hit"
#mailto_list=[""] 
mailto_list=[""] 
me_list=[""] 
mail_host="smtp.exmail.qq.com"  #设置服务器
mail_user=""    #用户名
mail_pass=""   #口令 
sender_name=""
host=""
database=""
username=""
password=""
time = (datetime.date.today () - datetime.timedelta (days=16)).strftime ("%Y-%m-%d")
my_client_id="27551"
my_username="wecash_private_url"
my_password="qwefpijanvijsnviaiou416541651"
token = "&account=" + my_client_id + "&username=" + my_username + "&password=" + my_password 
http_post_query="http://127.0.0.1:8080/biz-portal/private/query-bank-card-bill"
http_post_score="http://127.0.0.1:8080/biz-portal/private/score-insurance-detail"
yesterday = (datetime.date.today () - datetime.timedelta (days=1)).strftime ("%Y-%m-%d")
today = datetime.datetime.today().strftime("%Y-%m-%d")
start_time=yesterday + " 00:00:00"
end_time=yesterday + " 23:59:59"

#发送邮件
def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me=sender_name+"<"+mail_user+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
#查询数据库
def select(sql,db):
    result_list=[]
    try:
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor()
            # 使用execute方法执行SQL语句
            cursor.execute(sql)
            results = cursor.fetchall()
            for item in results:
                    result_list.append(item[0])
                    result_list.append(item[1])
                    result_list.append(item[2])
            cursor.close()
    except Exception, e:
        print "Error: unable to fecth data" + str(e)
    return result_list
#获取格式化sql
def getFormatSql(sql,time=today):
    return sql.replace("#{no_clients}",no_clients).replace("#{time}",time).replace("\n","")
#获取所有商户
def getAllCustomer(sql,time,db):
    return select(getFormatSql(sql,time=time),db)
#
def post(url, data):
    try:
        req = urllib2.Request(url)
        data = urllib.urlencode(data)
        #enable cookie  
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
        return response.read()
    except Exception, e:
        print "Error: unable to post " + url + " " + str(e)
#读sql
def readSql(file_name):
    lines=[]
        lines=file_sql.readlines()
        file_sql.close()
    except Exception, e:
        print "Error: unable to read sql" + str(e)
    return lines
def writeCSV(file_name,table_header,data):
    try:
        csvto = file(file_name, 'wb')
        writer = csv.writer(csvto)
        writer.writerow(table_header)
        writer.writerows(data)
        csvto.close()
    except Exception, e:
        print "Error: unable to write csv " + str(e)
def getTemplate(left,right,data):
    temp="<tr>"
    for item in data:
        if type(item) != unicode:
            temp += left + str(item) + right
        else:
            temp += left + item + right
    return temp + "</tr>"
#解决
def solve():
    try:
        # 打开数据库连接
        #table_header1=[u'监控日期',u'商户数',u'用户数',u'最新分数高危数(='+str(score)+')']
        table_header1=[u'监控日期',u'商户数',u'用户数']
        tot_line = [datetime.datetime.today().strftime("%Y-%m-%d")]
        clients=[]
        cids=[]
        hit_high=[]
        table_header=[u'商户号',u'商户名',u'用户号',u'用户名',u'身份证',u'车牌号',u'租车时间',u'绑定车牌号时间',u'快照分数',u'银行卡号',u'银行卡流水更新数']
        #table_header=[u'商户号',u'商户名',u'用户号',u'用户名',u'身份证',u'车牌号',u'租车时间',u'绑定车牌号时间',u'快照分数',u'银行卡号',u'银行卡流水更新数',u'最新分数']
        #arg_name=['clientId','clientName','customerId','name','idCard','plateNumber','rentTime','time','affordValue','card','updateCount','finalValue']
        arg_name=['clientId','clientName','customerId','name','idCard','plateNumber','rentTime','time','affordValue','card','updateCount']
        data=[]
        db = MySQLdb.connect(host,username,password,database,charset="utf8" )
        sqls=readSql(sql_file)
        customers=getAllCustomer(sqls[0],time,db)
        log=[today]
        hit_list=[]
        failed=[]
        i=0
        while(True):
            if ( i+2 > len(customers) ):
                break
            table_line=[]
            #银联流水
            http_post_query_url = http_post_query + "?" + "id=" + str(customers[i]) + "&clientId=" + str(customers[i+1]) + "&customerId=" + str(customers[i+2]) + token
            #打分
            http_post_score_url = http_post_score + "?" + "id=" + str(customers[i]) + "&clientId=" + str(customers[i+1]) + "&customerId=" + str(customers[i+2]) + token
            try:
                log.append(http_post_query_url)
                result = post(http_post_query_url,{})
                log.append(result)
                res_dict1 = eval(result)

                log.append(http_post_score_url)
                result = post(http_post_score_url,{})
                log.append(result)
                res_dict2 = eval(result)

                for key in arg_name:
                    if res_dict1 is not None and key in res_dict1.keys():
                        table_line.append(res_dict1[key])
                    elif res_dict2 is not None and key in res_dict2.keys():
                        table_line.append(res_dict2[key])
                    else:
                        table_line.append('unknown')
                data.append(tuple(table_line))
                if customers[i+1] not in clients:
                    clients.append(customers[i+1])
                if customers[i+2] not in cids:
                    cids.append(customers[i+2])
                #if res_dict2['finalValue'] <= score:
                #    hit_high.append(customers[i+2])
            except Exception, e:
                list_tmp=[str(customers[i]),str(customers[i+1]),str(customers[i+2])]
                failed.append(",".join(list_tmp))
                print "Error: unable to post data " + ",".join(list_tmp) + str(e)
            i = i + 3
        tot_line.append(len(clients))
        tot_line.append(len(cids))
        #tot_line.append(len(hit_high))
        writeCSV(csv_dir + datetime.datetime.today().strftime("%Y-%m-%d") + "-tot.csv",table_header1,[tuple(tot_line)])
        writeCSV(csv_dir + datetime.datetime.today().strftime("%Y-%m-%d") + "-detail.csv",table_header,data)
        print log
        print "failed to ",failed
        if len(failed) > 0:
            send_mail(me_list,u'failed to checking','='.join(failed))
        base_template=base_template.replace("#{data1}",getTemplate("<td>","</td>",tot_line))
        temp=""
        for item in data:
            temp += getTemplate("<td>","</td>",list(item))
        base_template=base_template.replace("#{data2}",temp)
        send_mail(mailto_list,u'银联流水监控',base_template)
        db.close()
    except Exception, e:
        print "Error: unable to fecth data" + str(e)
if __name__ == '__main__':
    solve()
