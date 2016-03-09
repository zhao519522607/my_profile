#! /usr/bin/env  python
from __future__ import division
# pymongo 3.1.1
# http://api.mongodb.org/python/current/
from pymongo import MongoClient
from pymongo import ReadPreference
from influxdb import InfluxDBClient
time = strftime("%Y-%m-%dT%H:%M:00Z", gmtime())
#time = strftime("%Y-%m-%dT%H:00:00Z", gmtime())

# Arguments for mongodb
mongodb_server     = ' '
mongodb_port       = ' '
mongodb_db_name    = ' '
mongodb_collection = ' '
mongodb_username   = ' '
mongodb_password   = ' '

# Arguments for influxdb
influxdb_host     = ' '
influxdb_port     = 8080
influxdb_username = ''
influxdb_password = ''
influxdb_dbname   = 'stat'

key_array = ['CHINA_MOBILE-BEI_JING', 'CHINA_MOBILE-TIAN_JIN', 'CHINA_MOBILE-SHAN_XI', 'CHINA_MOBILE-HE_BEI', 'CHINA_MOBILE-NEI_MENG_GU',
             'CHINA_MOBILE-LIAO_NING', 'CHINA_MOBILE-JI_LIN', 'CHINA_MOBILE-HEI_LONG_JIANG',
             'CHINA_MOBILE-SHANG_HAI', 'CHINA_MOBILE-JIANG_SU', 'CHINA_MOBILE-ZHE_JIANG', 'CHINA_MOBILE-AN_HUI', 'CHINA_MOBILE-FU_JIAN', 'CHINA_MOBILE-JIANG_XI', 'CHINA_MOBILE-SHAN_DONG',             'CHINA_MOBILE-HE_NAN', 'CHINA_MOBILE-HU_NAN', 'CHINA_MOBILE-HU_BEI', 'CHINA_MOBILE-GUANG_DONG', 'CHINA_MOBILE-GUANG_XI', 'CHINA_MOBILE-HAI_NAN',
             'CHINA_MOBILE-CHONG_QIONG', 'CHINA_MOBILE-SI_CHUAN', 'CHINA_MOBILE-GUI_ZHOU', 'CHINA_MOBILE-YUN_NAN', 'CHINA_MOBILE-XI_ZHANG',
             'CHINA_MOBILE-SHANXI', 'CHINA_MOBILE-GAN_SU', 'CHINA_MOBILE-QING_HAI', 'CHINA_MOBILE-NING_XIA', 'CHINA_MOBILE-XIN_JIANG',
             'CHINA_MOBILE-XIANGGANG', 'CHINA_MOBILE-AO_MEN', 'CHINA_MOBILE-TAI_WAN',

             'CHINA_UNICOM-BEI_JING', 'CHINA_UNICOM-TIAN_JIN', 'CHINA_UNICOM-SHAN_XI', 'CHINA_UNICOM-HE_BEI', 'CHINA_UNICOM-NEI_MENG_GU',
             'CHINA_UNICOM-LIAO_NING', 'CHINA_UNICOM-JI_LIN', 'CHINA_UNICOM-HEI_LONG_JIANG',
             'CHINA_UNICOM-SHANG_HAI', 'CHINA_UNICOM-JIANG_SU', 'CHINA_UNICOM-ZHE_JIANG', 'CHINA_UNICOM-AN_HUI', 'CHINA_UNICOM-FU_JIAN', 'CHINA_UNICOM-JIANG_XI', 'CHINA_UNICOM-SHAN_DONG',
             'CHINA_UNICOM-HE_NAN', 'CHINA_UNICOM-HU_NAN', 'CHINA_UNICOM-HU_BEI', 'CHINA_UNICOM-GUANG_DONG', 'CHINA_UNICOM-GUANG_XI', 'CHINA_UNICOM-HAI_NAN',
             'CHINA_UNICOM-CHONG_QIONG', 'CHINA_UNICOM-SI_CHUAN', 'CHINA_UNICOM-GUI_ZHOU', 'CHINA_UNICOM-YUN_NAN', 'CHINA_UNICOM-XI_ZHANG',
             'CHINA_UNICOM-SHANXI', 'CHINA_UNICOM-GAN_SU', 'CHINA_UNICOM-QING_HAI', 'CHINA_UNICOM-NING_XIA', 'CHINA_UNICOM-XIN_JIANG',
             'CHINA_UNICOM-XIANGGANG', 'CHINA_UNICOM-AO_MEN', 'CHINA_UNICOM-TAI_WAN',

             'CHINA_TELECOM-BEI_JING', 'CHINA_TELECOM-TIAN_JIN', 'CHINA_TELECOM-SHAN_XI', 'CHINA_TELECOM-HE_BEI', 'CHINA_TELECOM-NEI_MENG_GU',
             'CHINA_TELECOM-LIAO_NING', 'CHINA_TELECOM-JI_LIN', 'CHINA_TELECOM-HEI_LONG_JIANG',
             'CHINA_TELECOM-HE_NAN', 'CHINA_TELECOM-HU_NAN', 'CHINA_TELECOM-HU_BEI', 'CHINA_TELECOM-GUANG_DONG', 'CHINA_TELECOM-GUANG_XI', 'CHINA_TELECOM-HAI_NAN',
             'CHINA_TELECOM-CHONG_QIONG', 'CHINA_TELECOM-SI_CHUAN', 'CHINA_TELECOM-GUI_ZHOU', 'CHINA_TELECOM-YUN_NAN', 'CHINA_TELECOM-XI_ZHANG',
             'CHINA_TELECOM-SHANXI', 'CHINA_TELECOM-GAN_SU', 'CHINA_TELECOM-QING_HAI', 'CHINA_TELECOM-NING_XIA', 'CHINA_TELECOM-XIN_JIANG',
             'CHINA_TELECOM-XIANGGANG', 'CHINA_TELECOM-AO_MEN', 'CHINA_TELECOM-TAI_WAN'
             ]

# Init dict
from collections import defaultdict
success_count_dict          = defaultdict(int)
failure_count_dict          = defaultdict(int)
operator_failure_count_dict = defaultdict(int)
rate_dict                   = defaultdict(float)
system_rate_dict            = defaultdict(float)

for key in key_array:
    success_count_dict[key] = 0
    rate_dict[key]          = 0.00
    system_rate_dict[key]   = 0.00

import copy
failure_count_dict = copy.deepcopy(success_count_dict)


def getMobileLocation(collection, mobile_number):

    location_data = collection.find_one({'_id': mobile_number})

    return location_data


if __name__ == "__main__":

    sh_success          = r"/data/tomcat-8380/webapps/jenkins/shell/grepLogShow.sh '\[SUCCESS CRAWLER TASK\]' | sed -n 's/.*\([0-9]\{11\}\).*/\1/p' > /tmp/success.txt"
    sh_failure          = r"/data/tomcat-8380/webapps/jenkins/shell/grepLogShow.sh 'FAILED CRAWLER' | sed -n 's/.*\([0-9]\{11\}\).*/\1/p' > /tmp/failure.txt"
    sh_operator_failure = r"/data/tomcat-8380/webapps/jenkins/shell/grepLogShow.sh 'TRANSPORTATION FAILED CRAWLER' | sed -n 's/.*\([0-9]\{11\}\).*/\1/p' > /tmp/operator_failure.txt"

    from subprocess import Popen, PIPE

    # search for success
    p_success = Popen([sh_success, ''], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_success, err_success = p_success.communicate()

    # search for failure
    p_failure = Popen([sh_failure, ''], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_failure, err_failure= p_failure.communicate()

    # search for operator failure
    p_operator_failure = Popen([sh_operator_failure, ''], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    out_operator_failure, err_operator_failure= p_operator_failure.communicate()

    uri = 'mongodb://'+mongodb_username + ':' + mongodb_password + '@'+ mongodb_server + ':' + mongodb_port
    client = MongoClient(uri)

    db = client.get_database(mongodb_db_name, read_preference = ReadPreference.SECONDARY)

    mobile_location_collection = db[mongodb_collection]

    with open("/tmp/success.txt") as f:

        for line in f:

            if not line:
                continue

            mobile_location = getMobileLocation(mobile_location_collection, line[0:7])

            if not mobile_location:
                continue

            location = mobile_location['data']['provinceCode']
            type = mobile_location['data']['type']
            type_location = type + "-" + location

            success_count_dict[type_location] += 1

    with open("/tmp/failure.txt") as f:

        for line in f:

            if not line:
                continue

            mobile_location = getMobileLocation(mobile_location_collection, line[0:7])

            if not mobile_location:
                continue

            location = mobile_location['data']['provinceCode']
            type = mobile_location['data']['type']
            type_location = type + "-" + location

            failure_count_dict[type_location] += 1

    with open("/tmp/operator_failure.txt") as f:

        for line in f:

            if not line:
                continue

            mobile_location = getMobileLocation(mobile_location_collection, line[0:7])

            if not mobile_location:
                continue

            location = mobile_location['data']['provinceCode']
            type = mobile_location['data']['type']
            type_location = type + "-" + location

            operator_failure_count_dict[type_location] += 1


    # Init influxdb client
    client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_username, influxdb_password, influxdb_dbname)

    for key in key_array:
        s_count   = success_count_dict[key]
        f_count   = failure_count_dict[key]
        o_f_count = operator_failure_count_dict[key]

        if (s_count == 0 and f_count == 0):
            continue

        rate_dict[key] = round(s_count / (s_count + f_count), 2)*100
        system_rate_dict[key] = round( s_count / (s_count + f_count - o_f_count), 2)*100

        operator_type = key[0: key.index("-")]
        province      = key[key.index("-") + 1:]

        json_body = [
            {
                "measurement":"operator",
                "tags":{
                    "operator_type": operator_type,
                    "province":province
                },
                "time":time,
                "fields": {
                    'success': s_count,
                    'failure': f_count,
                    'operator_failure': o_f_count,
                    'rate': rate_dict[key],
                    'system_rate': system_rate_dict[key]
                }
            }
        ]

        client.write_points(json_body)

        #print key
        #print u"rate:" + str(rate_dict[key])
        #print u"system rate:" + str(system_rate_dict[key])
        #print u"success count:" + str(s_count)
        #print u"failure count:" + str(f_count)
        #print u"    caused by operator for without 6 month call info:" + str(o_f_count)
        #print u"total:" + str(s_count+f_count)
        #print "----------------------------------"

    print "done"
