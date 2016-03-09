 #! /bin/bash
#set -e -x

#解密
#openssl enc -aes-256-cbc -d -in aa.en -out aa -kfile /etc/vsftpd/shuxiang_668.key
#秘钥文件
#openssl genrsa -out /etc/vsftpd/shuxiang_668.key 1024
mi_yao="/etc/vsftpd/shuxiang_668.key"
#*************dir start*******************
#挂载目录
m_dir="/ftp_dir"
#加密ftp目录
f_dir="/mount_dir"
#查找挂载目录下的所有子目录输出到临时文件
find $m_dir -type d > /tmp/dir_temp
sed -i "s$m_dir$f_dir/g" /tmp/dir_temp

while read line
do
        if [ ! -d "$line" ];then
                mkdir -p $line
        fi
done < /tmp/dir_temp
#****************dir end******************

#***************file start****************
#查找挂载目录下的所有文件
find $m_dir -type f > /tmp/file_temp
#去除空文件
#while read null_file
#do
#       if [ -s $null_file ];then
#               echo $null_file >> /tmp/nonull_file
#       fi
#done < /tmp/file_temp
sed -i "s$m_dir$f_dir/g" /tmp/file_temp

while read file
do
        if [ ! -f "$file" ];then
                sc_file=`echo $file |sed 's/mount_dir/ftp_dir/g'`
                openssl enc -aes-256-cbc -in $sc_file -out $file.en -kfile $mi_yao
        fi
done < /tmp/file_temp

#删除不是指定格式的文件
#find $f_dir -type f |grep -v "\.en$" |xargs rm -rf





加密方式：
openssl genrsa -out privkey.pem 2048 
openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095   

openssl smime -encrypt -aes256 -in testdb.out.gz.2014-12-29 -binary -outform DEM -out testdb.out.gz.2014-12-29.enc publickey.pem

解密方式：
openssl smime -decrypt -in testdb.out.gz.2014-12-29.enc -binary -inform DEM -inkey privatekey.pem -out testdb.out.gz
