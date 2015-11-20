#!/bin/bash

source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
if [ -a celerybeat.pid ]; then
    rm -rf celerybeat.pid
fi
celery beat -A worker.celery
