! /bin/bash
# 2015/5/11
# author by zyb
set -x

echo "backup bengin staring........."
ALIYUN_SERVER="1"
ALIYUN_USER="sdd"
ALIYUN_KEY="/root/.ssh/aar"
ALIYUN_STORE_PATH="/www/mongodb_backup/"
date_time=`date +"%Y-%m-%d"`
work_path=`pwd`
mkdir $work_path/collection
dump_command="/usr/bin/mongoexport -u shanxin -p jpua7HWe -d pandora"
#collections=" touristPhraseData touristCreditData SYBlacklist"
collections="touristPhraseData touristCreditData SYBlacklist tbSuccessfulName loginNameParallelismTbName purui_test buyRiskResult taoBaoSecurity addressResult phoneResult idCardResult cmbResult jingDongHtml errorInput TaoBao blacklist jingDongResult tbStResultHTml authValid JingDong tbLoginHtmlOne tbOfflineResult system.users bcomResult unionpayStats authorizationUserInfo system.indexes"
$dump_command -c registRiskResult -o $work_path/collection/registRiskResult.dat &
wait
gzip $work_path/collection/registRiskResult.dat
$dump_command -c taoBaoResult -o $work_path/collection/taoBaoResult.dat
gzip $work_path/collection/taoBaoResult.dat

for i in $collections
do
    $dump_command -c $i -o $work_path/collection/$i.dat
done

tar zcf collection_$date_time.tgz collection

if [ -d collection ]; then
	rm -rf collection
fi

scp -i $ALIYUN_KEY $work_path/collection_$date_time.tgz $ALIYUN_USER@$ALIYUN_SERVER:$ALIYUN_STORE_PATH

rm $work_path/collection_$date_time.tgz

echo "backup ok"
