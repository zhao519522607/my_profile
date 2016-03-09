#! /bin/bash
#create time : 2015/5/12
#Author by : zyb
#use to dump oracle

work_path=`pwd`
script_name=`basename $0`
echo "this is oracle backup script."
echo "There are three kinds of backup, Monday full backup; Tuesday incremental backup; Wednesday incremental backup; Thursday incremental backup; Friday cumulative backup; Saturday incremental backup; Sunday ncremental backup."
echo "crontab -l
0 1 * * 1 $work_path/$script_name full > /dev/null 2>&1
0 1 * * 2 $work_path/$script_name incr > /dev/null 2>&1
0 1 * * 3 $work_path/$script_name incr > /dev/null 2>&1
0 1 * * 4 $work_path/$script_name incr > /dev/null 2>&1
0 1 * * 5 $work_path/$script_name cumu > /dev/null 2>&1
0 1 * * 6 $work_path/$script_name incr > /dev/null 2>&1
0 1 * * 7 $work_path/$script_name incr > /dev/null 2>&1
"

db_username="system"
db_password="123456"
backup_dir="/data2/oracle/backup"
date_time=`date +%Y-%m-%d`

#help fuc
help_fuc()
{
 echo "=============================="
 echo "you only choice full/incr/cumu"
 echo "=============================="
}

#full backup
back_full()
{
  exp $db_username/$db_password inctype=complete file=$backup_dir/exp_incr_$date_time.dmp log=$backup_dir/exp_incr_$date_time.log
}

#incremental backup
back_incremental()
{
  exp $db_username/$db_password inctype=incremental file=$backup_dir/exp_incr_$date_time.dmp log=$backup_dir/exp_incr_$date_time.log
}

#cumulative backup
back_cumulative()
{
  exp $db_username/$db_password inctype=cumulative file=$backup_dir/exp_incr_$date_time.dmp log=$backup_dir/exp_incr_$date_time.log
}

case $1 in
   full)
	  back_full
            ;;
   incr)
          back_incremental
            ;;
   cumu)
          back_cumulative
            ;;
      *)
          help_fuc
            ;;
esac
