#!/bin/bash


pid=`ps -ef| grep "python dogserver.py" | grep -v grep | head -n 1 | awk '{print $2}'`


while(($pid>0))
do
    kill -9 $pid
    pid=`ps -ef| grep "python dogserver.py" | grep -v grep | head -n 1 | awk '{print $2}'`
done



source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
python dogserver.py
