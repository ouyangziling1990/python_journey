#!/bin/sh
export LC_ALL=en_US.UTF-8
#cd /home/user/BDPlatform/scripts

check_process() {
 # echo "$ts: checking $1"
  [ "$1" = "" ]  && return 0
  [ `pgrep -n $1` ] && return 1 || return 0
}
while [ 1 ]; do
    send=`date '+%Y-%m-%d %H:%M:%S'`
    echo "$send: check sync function is running, begin "
    check_process 'manage.py'
    if [ $? -eq 0 ]; then
        echo 'is running '
    else 
        echo "restart function script "
        #nohup python3 carSyncDispatchFunction.py & 
    fi
    sleep 5
done
exit 0
