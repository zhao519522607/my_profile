#! /bin/bash

path="/data/shell/"
mail_list=" "


/usr/local/bin/fab -f $path/fabfile.py total >> /dev/null
/usr/local/bin/fab -f $path/fabfile.py success >> /dev/null
/usr/local/bin/fab -f $path/fabfile.py failed >> /dev/null
/usr/local/bin/fab -f $path/fabfile.py timeout >> /dev/null
/usr/local/bin/fab -f $path/fabfile.py time_per >> /dev/null

cat /data/shell/files/cost_all |sed -n 's/.*用户[0-9]\{11\}消耗时间\([0-9]\{1,10\}\).*/\1/p' | sort -n > /tmp/cost_all

total(){
        count_a=0
        for i in `ls -l /data/shell/files/total_* |awk '{print $9}'`
        do  
                aa=`awk '{print $1}' $i`
                let count_a+=$aa
        done

        echo "一共爬取次数: $count_a"
}

success(){
          count_b=0
        for i in `ls -l /data/shell/files/success_* |awk '{print $9}'`
        do  
                aa=`awk '{print $1}' $i`
                let count_b+=$aa
        done

        echo "成功次数: $count_b"
}

failed(){
          count_c=0
        for i in `ls -l /data/shell/files/failed_* |awk '{print $9}'`
        do
                aa=`awk '{print $1}' $i`
                let count_c+=$aa
        done

        echo "失败次数: $count_c"
}

timeout(){
          count_d=0
        for i in `ls -l /data/shell/files/timeout_* |awk '{print $9}'`
        do
                aa=`awk '{print $1}' $i`
                let count_d+=$aa
        done

        echo "其中超时次数: $count_d"
}

time_50(){
        line_nums=`cat /tmp/cost_all |wc -l`
        line_50=`echo $(echo "$line_nums*0.5"|bc) |awk -F . '{print $1}'`
        tmp_e=`sed -n "${line_50}p" /tmp/cost_all`
        count_e=`echo "scale=2; $tmp_e/1000" | bc -l`
}

time_95(){
        line_nums=`cat /tmp/cost_all |wc -l`
        line_95=`echo $(echo "$line_nums*0.95"|bc) |awk -F . '{print $1}'`
        tmp_f=`sed -n "${line_95}p" /tmp/cost_all`
        count_f=`echo "scale=2; $tmp_f/1000" | bc -l`
}

time_99(){
        line_nums=`cat /tmp/cost_all |wc -l`
        line_99=`echo $(echo "$line_nums*0.99"|bc) |awk -F . '{print $1}'`
        tmp_g=`sed -n "${line_99}p" /tmp/cost_all`
        count_g=`echo "scale=2; $tmp_g/1000" | bc -l`
}

main(){
        total
        success
        failed
        timeout
        time_50
        time_95
        time_99
        #let i=$count_b*100/$count_a
        i=`echo "scale=2; $count_b*100/$count_a " | bc -l`
        echo "成功率: $i%"
        echo "第50%个的爬取时间: $count_e秒"
        echo "第95%个的爬取时间: $count_f秒"
        echo "第99%个的爬取时间: $count_g秒"
        rm -rf /tmp/maxtime
        rm -rf /tmp/mintime
        rm -rf /tmp/avgtime
}

main > /tmp/mail_contxt

mutt -s "运营商授权结果统计" $mail_list < /tmp/mail_contxt

echo "邮件发送成功."
