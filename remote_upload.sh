#！ /bin/bash
#自述
echo "~~~~~~~~~~~~~~~~~~~~~~"
echo "Author by zyb"
echo "Create time 2015/7/17"
echo "Use to push package"
echo "~~~~~~~~~~~~~~~~~~~~~~"

#定义各种路径
list_dir="/data/shell/list"
Upload_dir="/data/upload"
file_dir="/data/shell"
logs_dir="/data/shell/logs"
time=`date +'%Y%m%d-%H%M'`

#上传函数
upload_package(){
read -p "example biz-portal/web-portal/car_ranting -->请输入要更的项目：" choice

case $choice in
        biz-portal)
                        pscp -h $list_dir/$choice.list -l www -o $logs_dir/upload_$time $file_dir/biz-portal.war $Upload_dir ;;
        web-portal)
                        pscp -h $list_dir/$choice.list -l www -o $logs_dir/upload_$time $file_dir/web-portal-jar-with-dependencies.jar $Upload_dir ;;
       car_ranting)
                        pscp -h $list_dir/$choice.list -l www -o $logs_dir/upload_$time $file_dir/car_ranting_web.tgz $Upload_dir ;;
                 *)
                        echo  "Sorry,这个选项暂不支持。"   ;;
esac

}

#执行更新指令函数
list(){
while read line
do
        IP=`echo $line |awk -F: '{print $1}'`
        PORT=`echo $line |awk -F: '{print $2}'`
        ssh -p $PORT www@$IP "/data/shell/update.sh"
done < $list_dir/$choice.list
}

#执行更脚本函数
remote_update(){
read -p "example biz-portal/web-portal/car_ranting -->请输入要更的项目：" choice

case $choice in
        biz-portal)
                        list && echo "Your are success." ;;
        web-portal)
                        list && echo "Your are success." ;;
       car_ranting)
                        list && echo "Your are success." ;;
                 *)
                        echo  "Sorry,这个选项暂不支持。"   ;;
esac

}

#定义主函数
main(){

read -p "example upload/update  -->请选择你要进行的操作：" choice
case $choice in
        upload)
                        upload_package ;;
        update)
                        remote_update  ;;
             *)
                         echo  "Sorry,这个选项暂不支持。"   ;;
esac
}

#运行主函数
main
