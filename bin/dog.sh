#!/bin/bash


pid=`ps -ef| grep "python dogserver.py" | grep -v grep | head -n 1 | awk '{print $2}'`

while true
do
    if [ ! -n "$pid" ]; then
        echo "null"
        break
    else
        echo "not null"
        kill -9 $pid
        pid=`ps -ef| grep "python dogserver.py" | grep -v grep | head -n 1 | awk '{print $2}'`
    fi
    echo PID $pid

    break
done


source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
python dogserver.py

