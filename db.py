# coding=utf-8
import pymysql
import tormysql

app_pool = tormysql.ConnectionPool(
    max_connections=80,  # max open connections
    idle_seconds=180,  # conntion idle timeout time, 0 is not timeout 连接空闲超过idle_seconds 后会自动关闭回收连接的
    wait_connection_timeout=3,  # wait connection timeout
    host="127.0.0.1",
    user="app",
    passwd="app_pass",
    db="myapp",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)
