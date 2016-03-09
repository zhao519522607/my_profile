 #! /usr/bin/env python
#coding:utf-8
'''
author: zyb
create: 2015/8/14
'''

import os,sys,smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

reload(sys)
sys.setdefaultencoding("utf-8")
base_path=os.path.dirname(os.path.abspath(__file__))
email_file = os.path.join(base_path,"email_file")
mail_host = "smtp.exmail.qq.com"
mail_user = "aa@qq.com"
mail_pass = "9900jdjjd"
sender_name = "11"
mailto_list = []
up_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def eamilfile(path,arg):
        command = "cd %s && git log -%s >> %s"  %(path,arg,email_file)
        result = os.system(command)
        if result == 0:
                print "命令执行成功."
        else:
                print "命令执行失败."

def eamilfile_many(path,arg):
        file_com = "echo "" > %s" %email_file
        os.system(file_com)
        for i in path:
                name = i.split("/")[2]
                command = "echo %s >> %s && cd %s && git log -%s >> %s"  %(name,email_file,i,arg,email_file)
                result = os.system(command)
        if result == 0:
                print "命令执行成功."
        else:
                print "命令执行失败."

def mail_to(it):
        #msg = MIMEMultipart()
        with open(email_file, 'rb') as f:
                lines = f.readlines()
        #'gb2312'
        #att1 = MIMEText(open(email_file, 'rb').read(), 'base64', _charset='utf-8')
        #att1["Content-Type"] = 'application/octet-stream'
        #att1["Content-Disposition"] = 'attachment; filename="git_logs.pdf"'
        my_txt = '''
                更新结果：已更新
                生产系统：%s
                发版时间：%s
                服务器：%s


        更新内容变更如下：
        ''' %(it[1],up_time,it[0])
        content = my_txt + '\n' + "".join(lines)
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        #msg.attach(att1)
        #msg.attach("".join(lines))
        me = sender_name + "<" + mail_user + ">"
        msg['From'] = me
        msg['To'] = ";".join(mailto_list)
        msg['Subject'] = "生产线更新邮件通知"

        try:
                server = smtplib.SMTP()
                server.connect(mail_host)
                server.login(mail_user,mail_pass)
                server.sendmail(me, mailto_list, msg.as_string())
                server.quit()
                print '发送成功'
        except Exception, e:
                print str(e)

def main(choice,line):
        if choice == "biz":
                pro_name = "biz-portal"
                ip_list = "123.2.3.4"
                choice_com = "echo 'biz-portal' > %s" %email_file
                os.system(choice_com)
                path = "/data/car_ranting/"
                eamilfile(path,line)
        if choice == "js":
                pro_name = "car_ranting_web"
                ip_list = "15.8.10.2"
                choice_com = "echo 'car_ranting_web' > %s" %email_file
                os.system(choice_com)
                path = "/data/car_ranting_web/"
                eamilfile(path,line)
        if choice == "web-pro":
                pro_name = "web-portal"
                ip_list = "15.28.10.24"
                choice_com = "echo 'web-portal' > %s" %email_file
                os.system(choice_com)
                path = "/data/web-portal/"
                eamilfile(path,line)
        if choice == "b-j":
                pro_name = "nodejs-web/biz-portal"
                ip_list = "115.28.150.234,123.57.38.148"
                path = ["/data/car_ranting/","/data/car_ranting_web/"]
                eamilfile_many(path,line)
        if choice == "b-w":
                pro_name = "biz-portal/web-portal"
                ip_list = "15.28.50.24,13.57.38.48"
                path = ["/data/car_ranting/","/data/web-portal/"]
                eamilfile_many(path,line)
        if choice == "j-w":
                pro_name = "nodejs-web/web-portal"
                ip_list = "115.28.150.234"
                path = ["/data/car_ranting_web/","/data/web-portal/"]
                eamilfile_many(path,line)
        if choice == "all":
                pro_name = "biz-portal/web-portal/nodejs-web"
                ip_list = "15.8.10.24,13.7.38.18"
                path = ["/data/car_ranting/","/data/car_ranting_web/","/data/web-portal/"]
                eamilfile_many(path,line)
        return (ip_list,pro_name)

def help():
        print '''
                你只能输入两个参数，
                第一个参数为更新的类型 biz/js/web-pro/b-j/b-w/j-w/all，
                第二个参数为你要打印的记录行，
                example: python %s biz 2
              ''' %py_file
        sys.exit(1)

if __name__ == '__main__':
        py_file = sys.argv[0]
        if len(sys.argv) != 3:
                help()
        else:
                choice = sys.argv[1]
                line = sys.argv[2]
                items = main(choice,line)
                mail_to(items)
