监听分发程序
========================

## 监听
- 监听指定目录的文件`创建`、`修改`、`更名`
- 监听到的文件保存在redis中

## 分发
- 程序每个整点分钟执行，获取全部保存的redis键值，并打上键更新值，防止重复处理
- 键值会进行匹配，对于不需要处理的文件，则对键进行过期处理，需要处理的，按照APP_FILE_ROUTE的配置信息，进行分发，分发成功后过期键值


## 注意事项
- 文件分发规则，配置在APP_FILE_ROUTE中，linux大小写敏感，配置时需注意，配置路径时注意区分相对路径，绝对路径
- 符合的文件需要按照`APP_FILE_ROUTE.SRC_NAME`_时间戳.`APP_FILE_ROUTE.SRC_EXTENSION`生成，大小写敏感，必须有时间戳，时间戳放在最后一个时间戳后

## 配置日期格式
![](format.png)


## 安装
- 配置环境变量*ENV*，'DEVELOPMENT | TEST | PRODUCTION' 三个值对应三种不同的配置
- 修改*app/conf.py*,'WATCH_PATH'设置监听的目录,'DB_ENGINE'，数据库连接方式，不同的数据库需要安装不同的包

## 启动(手动)
- 监听服务 cd app && python dogserver.py
- 分发调度器 celery beat -A worker.celery
- 分发程序 celery worker -A worker.celery  -P gevent -c 100 --loglevel=info -n worker1


## 其他

**KV**
redis-server /etc/redis.conf

**SQL**


**生成文件**
dd if=/dev/zero of=1.file bs=1024 count=0 seek=$[1024*1000*3]


