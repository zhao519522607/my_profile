#!/bin/bash
#*/1 * * * * /root/http_code.sh

export LC_ALL=zh_CN.UTF-8
URL="http://192.168.10.15:800/nn/aa.html"

HTTP_CODE=`curl -o /dev/null -s -w "%{http_code}" "${URL}"`
echo $HTTP_CODE

if [ $HTTP_CODE != 200 ];then
killall -9 java
killall -9 java
killall -9 nginx
killall -9 nginx
cd /opt/tomcat1/work/
rm -rf Catalina
cd /opt/tomcat2/work/
rm -rf Catalina
/opt/tomcat1/bin/startup.sh
/opt/nginx3/sbin/nginx
sleep 20
/opt/tomcat2/bin/startup.sh
/opt/nginx4/sbin/nginx

fi
从 DNS 解析到 202.102.75.162 主机

curl -I -H "Host:www.sina.com.cn" http://202.102.75.169/
HTTP/1.1 200 OK
