#! /bin/bash

mail_list_day=" "
mail_list_rate=" "


oper_day()
{
        python /data/shell/influxdb_total.py oper_day > /tmp/oper_mail
        if [ $? -ne 11 ]
        then
                mutt -s "运营商授权结果统计" $mail_list_day < /tmp/oper_mail
                echo "邮件发送成功."
        fi  
}

oper_rate()
{
        echo "运营商成功率预警" > /tmp/operate_mail
        python /data/shell/influxdb_total.py oper_rate >> /tmp/operate_mail
        num_w=`cat /tmp/operate_mail |wc -l`
        if [ $? -ne 12 -a $num_w != 2 ] 
        then
                mutt -s "运营商成功率预警" $mail_list_rate < /tmp/operate_mail
                echo "邮件发送成功."
        fi  
}

social_day()
{
        python /data/shell/influxdb_total.py social_day > /tmp/social_mail
        if [ $? -ne 13 ]
        then
                mutt -s "社保授权结果统计" $mail_list_day < /tmp/social_mail
                echo "邮件发送成功."
        fi  
}

social_rate()
{
        echo "社保成功率预警" > /tmp/socialrate_mail
        python /data/shell/influxdb_total.py social_rate >> /tmp/socialrate_mail
        num_w=`cat /tmp/socialrate_mail |wc -l`
        if [ $? -ne 14 -a $num_w != 2 ]
        then
                mutt -s "社保成功率预警" $mail_list_rate < /tmp/socialrate_mail
                echo "邮件发送成功."
        fi
}

case $1 in
        oper_day)
                        oper_day     ;;
        oper_rate)
                        oper_rate    ;;
        social_day)
                        social_day   ;;
        social_rate)
                        social_rate  ;;
        *)
                        echo "You have a problem with the options you have entered."  ;;
esac
                   
