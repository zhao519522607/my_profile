#! /bin/bash
my_dir="/data/tomcat-8080/logs/Log_analysis"
if [ -d $my_dir ];then
        echo "dir is Already exists"
        rm -rf $my_dir/*
else
        mkdir $my_dir
fi

cd /data/tomcat-8080/logs
cp *.gz $my_dir
cd $my_dir

for i in `ls -l|awk '{print $9}' |grep -v '^$'`
do
        gzip -d $i
done

cp /data/tomcat-8080/logs/catalina.out $my_dir
grep -ir "详单禁查" ./ |grep -o "loginName=[0-9]\{11\}" |awk -F "=" '{print $2}' |sort |uniq > /data/shell/phone_list
rm -rf $my_dir/*
