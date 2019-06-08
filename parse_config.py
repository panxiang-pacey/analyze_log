# coding: utf-8

import os
import configparser

def fun_get_conn_str():
    # 获取数据库连接信息
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'config.ini')
        print('配置文件路径：', file_path)

        config = configparser.ConfigParser()
        config.read(file_path, encoding='UTF-8')  #不触发异常

        if 'db' in config:  ## 判断配置文件中是否存在db块
            drivername = config.get('db', 'drivername')  # NoOptionError异常
            username = config.get('db', 'username')
            password = config.get('db', 'password')
            host = config.get('db', 'host')
            port = config.get('db', 'port')
            database = config.get('db', 'database')
            charset = config.get('db', 'charset')

            #conn_str = 'mysql+mysqlconnector://nprobe:nprobe@132.232.57.199:3306/db_nprobe?charset=utf8mb4'
            conn_str = '{0}://{1}:{2}@{3}:{4}/{5}?charset={6}'.format(drivername,username,password,host,port,database,charset)
            return conn_str

        else:
            print('未找到配置文件或配置文件中不存在db块')

    except Exception as err:
        print(err)


if __name__ == '__main__':
    print(fun_get_conn_str())