# coding: utf-8
import os
import datetime
import mysql.connector
import configparser
from dual_mysql_log import  fun_resolve_mysql_log
from dual_nginx_access_log import fun_resolve_nginx_access_log
from dual_uwsgi_log import fun_resolve_uwsgi_log
from dual_linux_secure_log import fun_resolve_linux_secure_log
from dual_linux_messages_log import fun_resolve_linux_messages_log


def fun_exec_log(v_exec_step,v_record_count,v_start_time,v_end_time,v_run_seconds,v_err_log):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199', database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "insert into t_exec_log(exec_step,record_count,start_time,end_time,run_seconds,err_log) values ('{0}',{1},'{2}','{3}',{4},'{5}');".format(v_exec_step,v_record_count,v_start_time,v_end_time,v_run_seconds,v_err_log)
        #print(v_sql)
        cursor.execute(v_sql)
    except Exception as err:
        print(err)
    finally:
        cursor.close()
        conn.commit()
        conn.close()




if __name__ == '__main__':

    #读取日志文件路径
    try:
        #file_path = r'/opt/analyze_log/config.ini'
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir,'config.ini')
        print('配置文件路径：',file_path)
        config = configparser.ConfigParser()
        config.read(file_path, encoding='UTF-8')  #计划任务执行时报错 绝对路径 不触发异常
        #config[section][option] #读取section中的option的值
        #config.get(section, option)#得到section中option的值，返回为string类型

        if 'log_path' in config: ## 判断配置文件中是否存在log_path块
            mysqld_log_path = config.get('log_path','mysqld_log') #NoOptionError异常
            nginx_access_log_path = config.get('log_path','nginx_access_log')
            uwsgi_log_path = config.get('log_path','uwsgi_log')
            linux_messages_log_path = config.get('log_path','linux_messages_log')
            linux_secure_log_path = config.get('log_path','linux_secure_log')
        else:
            print('配置文件中不存在log_path块')

    except Exception as err:
        #print('配置文件Option错误！')
        print(err)
        err_log = str(err).replace("'", "\\\'")
        fun_exec_log('读取配置文件',-1, '','', -1, err_log)


    #处理MySQL错误日志
    try:
        exec_step='处理MySQL错误日志'
        record_count = -1
        err_log = '正常'
        start_time = datetime.datetime.now()

        insert_result = fun_resolve_mysql_log(r'{0}'.format(mysqld_log_path))
        if type(insert_result) == int :
            record_count = insert_result
        else:
            err_log = str(insert_result).replace("'", "\\\'") #捕获子函数抛出的异常

    except Exception as err:
        err_log = str(err).replace("'", "\\\'")

    finally:
        end_time = datetime.datetime.now()
        delta = end_time - start_time
        run_seconds = delta.seconds
        fun_exec_log(exec_step, record_count, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"), run_seconds, err_log)


    #处理nginx的access日志
    try:
        exec_step='处理nginx的access日志'
        record_count = -1
        err_log = '正常'
        start_time = datetime.datetime.now()

        insert_result = fun_resolve_nginx_access_log(r'{0}'.format(nginx_access_log_path))
        if type(insert_result) == int:
            record_count = insert_result
        else:
            err_log = str(insert_result).replace("'", "\\\'") #捕获子函数抛出的异常

    except Exception as err:
        err_log = str(err).replace("'", "\\\'")
    finally:
        end_time = datetime.datetime.now()
        delta = end_time - start_time
        run_seconds = delta.seconds
        fun_exec_log(exec_step, record_count, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"), run_seconds, err_log)




    # 处理uwsgi日志
    try:
            exec_step = '处理uwsgi日志'
            record_count = -1
            err_log = '正常'
            start_time = datetime.datetime.now()

            insert_result = fun_resolve_uwsgi_log(r'{0}'.format(uwsgi_log_path))
            if type(insert_result) == int:
                record_count = insert_result
            else:
                err_log = str(insert_result).replace("'", "\\\'")  # 捕获子函数抛出的异常

    except Exception as err:
            err_log = str(err).replace("'", "\\\'")
    finally:
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            run_seconds = delta.seconds
            fun_exec_log(exec_step, record_count, start_time.strftime("%Y-%m-%d %H:%M:%S"),
                         end_time.strftime("%Y-%m-%d %H:%M:%S"), run_seconds, err_log)



    # 处理linux的messages日志
    try:
        exec_step = '处理linux的messages日志'
        record_count = -1
        err_log = '正常'
        start_time = datetime.datetime.now()

        insert_result = fun_resolve_linux_messages_log(r'{0}'.format(linux_messages_log_path))
        if type(insert_result) == int:
            record_count = insert_result
        else:
            err_log = str(insert_result).replace("'", "\\\'")  # 捕获子函数抛出的异常

    except Exception as err:
        err_log = str(err).replace("'", "\\\'")
    finally:
        end_time = datetime.datetime.now()
        delta = end_time - start_time
        run_seconds = delta.seconds
        fun_exec_log(exec_step, record_count, start_time.strftime("%Y-%m-%d %H:%M:%S"),
                     end_time.strftime("%Y-%m-%d %H:%M:%S"), run_seconds, err_log)




    # 处理linux的secure日志
    try:
        exec_step = '处理linux的secure日志'
        record_count = -1
        err_log = '正常'
        start_time = datetime.datetime.now()

        insert_result = fun_resolve_linux_secure_log(r'{0}'.format(linux_secure_log_path))
        if type(insert_result) == int:
            record_count = insert_result
        else:
            err_log = str(insert_result).replace("'", "\\\'")  # 捕获子函数抛出的异常

    except Exception as err:
        err_log = str(err).replace("'", "\\\'")
    finally:
        end_time = datetime.datetime.now()
        delta = end_time - start_time
        run_seconds = delta.seconds
        fun_exec_log(exec_step, record_count, start_time.strftime("%Y-%m-%d %H:%M:%S"),
                     end_time.strftime("%Y-%m-%d %H:%M:%S"), run_seconds, err_log)




