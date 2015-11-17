

##监听
- 监听指定目录的文件`创建`、`修改`、`更名`
- 监听到的文件保存在redis中

##处理
- 程序每个整点分钟执行，获取全部保存的redis键值，并打上键更新值，防止重复处理
- 键值会进行匹配，对于不需要处理的文件，则对键进行过期处理，需要处理的，按照APP_FILE_ROUTE的配置信息，进行分发，分发成功后过期键值


##规范
- 文件分发规则，配置在APP_FILE_ROUTE中，linux大小写敏感，配置时需注意，配置路径时注意区分相对路径，绝对路径
- 符合的文件需要按照`APP_FILE_ROUTE.SRC_NAME`_时间戳.`APP_FILE_ROUTE.SRC_EXTENSION`生成，大小写敏感，必须有时间戳，时间戳放在最后一个时间戳后




# Wathdog
python dogserver.py

# Celery

celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker1
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker2
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker3
celery worker -A worker.celery  -P gevent -c 1000 --loglevel=info -n worker4

# celery beat
celery beat -A worker.celery

# Celery flower
celery flower -A worker.celery --address=127.0.0.1



# Test
dd if=/dev/zero of=1.file bs=1024 count=0 seek=$[1024*1000*3]
