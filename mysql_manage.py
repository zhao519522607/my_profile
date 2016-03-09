#! /usr/bin/python
#coding:utf8
import MySQLdb,sys


def mysql_connect(sql):
    conn = MySQLdb.connect(host='myhost',user='mysqluser',passwd='mysqlpassword',db='mysqldb')
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    conn.commit()
    cursor.close ()
    conn.close ()
    return row


def dns_select():
    domain_name = raw_input("input the domain_name [www]: ")
    #zone_name = raw_input("input the zone_name [wecash.net]: ")
    zone_name = "wecash.net"
    select_sql= "select host,zone,data,type from dns_records where host='"+domain_name+"' and zone='"+zone_name+"'"
    #print select_sql
    return mysql_connect(select_sql)

def dns_select_all_records():
        select_sql= "select host from dns_records"
        return mysql_connect(select_sql)

def record_exist(zone_name,domain_name):
    select_sql= "select host,zone,data,type from dns_records where host='"+domain_name+"' and zone='"+zone_name+"'"
    #print select_sql
    return mysql_connect(select_sql)

def dns_insert():
    domain_type = "A"
    try:
        domain_name = raw_input("please input the domain name [www]: ")
        #zone_name = raw_input("please input the zone name [wecash.net]: ")
        zone_name = "wecash.net"
        record = record_exist(zone_name,domain_name)
        if record:
                error_print("The record already exist!")
                print record
        else:
                ip_address = raw_input("please input the ip address [192.168.56.1]: ")
                insert_sql = "INSERT INTO dns_records (zone,host,type,data,ttl,retry) values ('"+zone_name+"','"+domain_name+"','"+domain_type+"','"+ip_address+"',86400,15)"
                insert_status = mysql_connect(insert_sql)
                if not insert_status:
                        exist = record_exist(zone_name,domain_name)
                        if exist:
                                correcct_print("insert success !")
                                correcct_print(exist)
                        else:
                                error_print("can not find the insert record! insert failed")
    except KeyboardInterrupt:
        error_print(" abort input and back to manage")
        manage()

def dns_update():
    try:
        domain_name = raw_input("please input want to change domain name which [www]: ")
        #zone_name = raw_input("please input the zone name [wecash.net]: ")
        zone_name = 'wecash.net'
        record_in = record_exist(zone_name,domain_name)
        if not record_in:
                error_print("the dns record was not found ,please check your input,or insert this record")
        else:
                ip_new_address = raw_input("please input the new ip address [192.168.56.1]: ")
                update_sql="update dns_records set data='"+ip_new_address+"' where host='"+domain_name+"' and zone='"+zone_name+"'"
                update = mysql_connect(update_sql)
                if not update :
                        print '''
\033[1;32;40mThis is change before to record\033[0m
%s
                              ''' %record_in
                        ans = record_exist(zone_name,domain_name)
                        if ans :
                                correcct_print("update success")
                                print ans
                        else:
                                error_print("update failed,new data was not found !")
                else:
                        error_print("update failed!")

    except KeyboardInterrupt:
        error_print("abort input and back to manage ")
        manage()

def dns_delete():
    try:
        domain_name = raw_input("please input the domain name you want delete [www]: ")
        #zone_name = raw_input("please input the zone name you want to delete [wecash.net]: ")
        zone_name = 'wecash.net'
        #ip_address = raw_input("please input the domain's ip address [192.168.56.1]: ")
    except KeyboardInterrupt:
        error_print("abort input and back to manage!")
        manage()
    #delete_sql = "delete from dns_records where host='"+domain_name+"' and zone='"+zone_name+"' and data='"+ip_address+"'"
    delete_sql = "delete from dns_records where host='"+domain_name+"' and zone='"+zone_name+"'"
    #print delete_sql
    record_in = record_exist(zone_name,domain_name)
    if record_in:
        print "find the record:"
        print record_in
        delete = str(raw_input("delete this record ? [y/n]"))
        if delete == "y":
            mysql_connect(delete_sql)
            delete_status = record_exist(zone_name,domain_name)
            if not delete_status:
                correcct_print("record was deleted !")
            else:
                error_print("delete failed the record is still here!")
                print delete_status
        else:
            error_print("action abort!")
    else:
        error_print("not found the record!")
        print domain_name+"."+zone_name


def correcct_print(obj):
    print '\033[1;32;40m%s\033[0m' % obj

def error_print(obj):
    print '\033[1;31;40m%s\033[0m' % obj


def manage():
    while True:
        print """
please choice which options you want?
[0] exit now
[1] select
[2] insert
[3] update
[4] delete
[9] all_records """
        options = raw_input("input the number of options: ").split()[0]
        if options == "1":
            record_tup = dns_select()
            if record_tup:
                i = 0
                correcct_print("find the record ")
                while i < len(record_tup):
                    print record_tup[i]
                    i=i+1

            else:
                error_print("not found the record!")

        elif options== "2":
            dns_insert()

        elif options == "3":
            dns_update()
        elif options == "4":
            dns_delete()
        elif options == "9":
            print dns_select_all_records()
        elif options == "0":
            correcct_print("**********EXIT NOW ***********")
            break
        else:
            error_print("invalid options please try again")



if __name__ == "__main__":
    try:
        manage()
    except KeyboardInterrupt:
        error_print("back to manage options!")
        manage()
    except IndexError:
        manage()
    finally:
        sys.exit(1)
