#! /usr/bin/env python
#coding:utf-8
from influxdb import InfluxDBClient,InfluxDBClusterClient
import time,datetime,sys

'''
author by: zyb
create time: 2016-1-4 14:24
useful: to total

'''

yesterday = datetime.date.today() + datetime.timedelta(days=-1)
yesterday_modify = str(yesterday) + "T00:00:00Z"
today_modify = str(datetime.date.today()) + "T00:00:00Z"
end_time = datetime.datetime.now()
timestamp = str(int(time.time())) + "000000000"
start_time = end_time - datetime.timedelta(minutes=15)
#单机的连接方式
#client = InfluxDBClient('localhost', 8086, 'crawler1', 'OGNjNWY5Y253', 'operator')
#集群的连接方式
operator_cc = InfluxDBClusterClient(hosts = [('1.1.1.1', 8080),
                                             ('2.2.2.2', 8080),
                                             ('3.3.3.3', 8080)],
                                             username='user',
                                             password='password',
                                             database='dbname')
operator_social = InfluxDBClusterClient(hosts = [('1.1.1.1', 8086),
                                                 ('2.2.2.2', 8086),
                                                 ('3.3.3.3', 8086)],
                                                 username='user',
                                                 password='password',
                                                 database='db_name')
#运营商一天的统计函数
def oper():
        oper_time = 'SELECT time_cost FROM "operator" WHERE time >= \'%s\' AND time < \'%s\'' %(yesterday_modify,today_modify)
        #调试语句
        #oper_time = 'SELECT time_cost FROM "operator" WHERE time >= \'2016-02-22T00:00:00Z\' AND time < \'2016-02-23T00:00:00Z\''
        oper_result_time = operator_cc.query('%s' %oper_time)
        oper_result_num = operator_cc.query('%s' %oper_num)
        while True:
                if oper_result_time and oper_result_num:
                        oper_list_tmp = oper_result_time.raw.values()[0][0]['values']
                        oper_list = sorted(oper_list_tmp, key=lambda oper_list_tmp: oper_list_tmp[1])
                        oper_num_50 = int(oper_result_num.raw.values()[0][0]['values'][0][1])
                        oper_num_95 = int(oper_result_num.raw.values()[0][0]['values'][0][2])
                        oper_num_99 = int(oper_result_num.raw.values()[0][0]['values'][0][3])
                        oper_time_50 = oper_list[oper_num_50][1]
                        oper_time_95 = oper_list[oper_num_95][1]
                        oper_time_99 = oper_list[oper_num_99][1]
                        break
                else:
                        oper_result_time = operator_cc.query('%s' %oper_time)
                        oper_result_num = operator_cc.query('%s' %oper_num)
                        time.sleep(2)
        count = 0
                        oper_success = oper_result.raw.values()[0][0]['values'][0][1]
                        oper_failure = oper_result.raw.values()[0][0]['values'][0][2]
                        oper_result = operator_cc.query('%s' %oper_sentence)
                        count += 1
                        time.sleep(2)
                else:
                        print "Total try 5 times still empty."
                        sys.exit(11)

        return oper_success,oper_failure,oper_total,'%.2f'%oper_rate,oper_time_50,oper_time_95,oper_time_99
#运营商授权预警函数
def oper_rate():
        oper_15rate = 'SELECT (sum("success")  / count("success")) * 100 as percentage FROM "operator" WHERE time > %s - 15m  GROUP BY province,operator' %timestamp
        oper_result_15rate = operator_cc.query('%s' %oper_15rate)
        operate_list = []
        oper_rate_count = 0
        while True:
                if oper_result_15rate:
                        for item in oper_result_15rate.raw.values()[0]:
                                if item['values'][0][1] < 95:
                                        operate_list.append(item)
                        break
                elif not oper_result_15rate and oper_rate_count < 5:
                        oper_result_15rate = operator_cc.query('%s' %oper_15rate)
                        oper_rate_count += 1
                        time.sleep(2)
                else:
                        print "Rate try 5 times still empty."
                        sys.exit(12)

        return operate_list
#社保一天的统计函数
def social():
        social_time = 'SELECT time_cost FROM "social_security" WHERE time >= \'%s\' AND time < \'%s\'' %(yesterday_modify,today_modify)
        #调试语句
        #social_time = 'SELECT time_cost FROM "social_security" WHERE time >= \'2016-02-22T00:00:00Z\' AND time < \'2016-02-23T00:00:00Z\''
        social_result_time = operator_social.query('%s' %social_time)
        social_result_num = operator_social.query('%s' %social_num)
        while True:
                if social_result_time and social_result_num:
                        social_list_tmp = social_result_time.raw.values()[0][0]['values']
                        social_list = sorted(social_list_tmp, key=lambda social_list_tmp: social_list_tmp[1])
                        social_num_50 = int(social_result_num.raw.values()[0][0]['values'][0][1])
                        social_num_95 = int(social_result_num.raw.values()[0][0]['values'][0][2])
                        social_num_99 = int(social_result_num.raw.values()[0][0]['values'][0][3])
                        social_time_50 = social_list[social_num_50][1]
                        social_time_95 = social_list[social_num_95][1]
                        social_time_99 = social_list[social_num_99][1]
                        break
                else:
                        social_result_time = operator_social.query('%s' %social_time)
                        social_result_num = operator_social.query('%s' %social_num)
                        time.sleep(2)

        social_result = operator_social.query('%s' %social_sentence)
        count = 0
        while True:
                if social_result.raw:
                        social_success = social_result.raw.values()[0][0]['values'][0][1]
                        social_failure = social_result.raw.values()[0][0]['values'][0][2]
                        social_total = social_result.raw.values()[0][0]['values'][0][3]
                        social_rate = social_result.raw.values()[0][0]['values'][0][4]
                        break
                elif not social_result.raw and count < 5:
                        social_result = operator_social.query('%s' %social_sentence)
                        count += 1
                        time.sleep(2)
                else:
                        print "Total try 5 times still empty."
                        sys.exit(13)

        return social_success,social_failure,social_total,'%.2f'%social_rate,social_time_50,social_time_95,social_time_99
#社保授权预警函数
def social_rate():
        social_15rate = 'SELECT (sum("success")  / count("success")) * 100 as percentage FROM "social_security" WHERE time > %s - 15m  GROUP BY city,social_security' %timestamp
        social_result_15rate = operator_social.query('%s' %social_15rate)
        social_list = []
        social_rate_count = 0
        while True:
                if social_result_15rate:
                        for item in social_result_15rate.raw.values()[0]:
                                if item['values'][0][1] < 95:
                                        social_list.append(item)
                        break
                elif not social_result_15rate and social_rate_count < 5:
                        social_result_15rate = operator_social.query('%s' %social_15rate)
                        social_rate_count += 1
                        time.sleep(2)
                else:
                        print "Rate try 5 times still empty."
                        sys.exit(14)

        return social_list

if __name__ == '__main__':
        try:
                input = sys.argv[1]
                if input == "oper_day":
                        oper_all = oper()
                        oper_readme = r'''
                        运营商统计
                        一共爬取次数：%d
                        成功次数：%d
                        失败次数：%d
                        成功率：%s%%
                        第50%%个的爬取时间: %d秒
                        第95%%个的爬取时间: %d秒
                        第99%%个的爬取时间: %d秒
                        ''' % (oper_all[2],oper_all[0],oper_all[1],oper_all[3],oper_all[4],oper_all[5],oper_all[6])
                        print oper_readme
                elif input == "social_day":
                        social_all = social()
                        social_readme = r'''
                        社保统计
                        一共爬取次数：%d
                        成功次数：%d
                        失败次数：%d
                        成功率：%s%%
                        第50%%个的爬取时间: %d秒
                        第95%%个的爬取时间: %d秒
                        第99%%个的爬取时间: %d秒
                        ''' % (social_all[2],social_all[0],social_all[1],social_all[3],social_all[4],social_all[5],social_all[6])
                        print social_readme
                elif input == "oper_rate":
                        oper_rate = oper_rate()
                        if oper_rate:
                                print "时间段: %s —%s".rjust(0," ") %(start_time,end_time)
                                for i in oper_rate:
                                        operate_readme = r'''
                                                ----------------
                                                省份：%s
                                                运营商: %s
                                                成功率：%s%%
                                                '''  %(str(i['tags']['province']),str(i['tags']['operator']),str(i['values'][0][1]))
                                        print operate_readme
                        else:
                                sys.exit(12)
                elif input == "social_rate":
                        social_rate = social_rate()
                        if social_rate:
                                print "时间段: %s —%s".rjust(0," ") %(start_time,end_time)
                                for i in social_rate:
                                        social_readme = r'''
                                                ----------------
                                                城市: %s
                                                成功率：%s%%
                                                '''  %(str(i['tags']['city']),str(i['values'][0][1]))
                                        print social_readme
                        else:
                                sys.exit(14)
                else:
                        print "You have a problem with the options you have entered."
        except IndexError:
                print "Enter at least one parameter."
        except:
                print "数据库没有返回结果"
