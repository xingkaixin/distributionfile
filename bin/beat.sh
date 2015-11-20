#!/bin/bash

source ~/.bash_profile
source ~/venv/bin/activate
cd ../app
celery beat -A worker.celery
