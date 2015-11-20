#!/bin/bash

source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker1
