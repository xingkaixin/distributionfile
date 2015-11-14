

##监听服务
- 监听指定目录的文件`创建`、`更名`
- 监听到的文件，进入文件路由匹配查询
- 队列中






# Celery


celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker1
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker2
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker3
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker4


# Celery flower
celery flower -A worker.celery --address=127.0.0.1



# Test
dd if=/dev/zero of=1.file bs=1024 count=0 seek=$[1024*1000*3]
