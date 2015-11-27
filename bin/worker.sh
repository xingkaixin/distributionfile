#!/bin/bash


pid=`ps -ef| grep "celery worker" | grep "worker1" |  grep -v grep | head -n 1 | awk '{print $2}'`


while(($pid>0))
do
    kill -9 $pid
    pid=`ps -ef| grep "celery worker" | grep "worker1" |  grep -v grep | head -n 1 | awk '{print $2}'`
done

source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker1
