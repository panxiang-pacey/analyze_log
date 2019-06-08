# coding: utf-8
import re
import datetime
from import_db import fun_insert_table

def fun_resolve_mysql_log(v_LogFile):
    i=0
    cnt=0
    list_sql=[]
    start_time = datetime.datetime.now()
    try:
        with open(v_LogFile,'r') as f:
            list_allline = f.readlines()
            rowcount=len(list_allline)
            f.seek(0,0)

            while i < rowcount:
                   i = i + 1
                   line = f.readline()

                   #if len(line) > 1 :
                   if re.match(r'^\d{4}-\d{2}-\d{2}', line):
                          cnt = cnt + 1
                          #print(line)
                          #逐行处理每条记录
                          list_field = line.split(' ',3) #限制分裂次数
                          #print(list_field)
                          # 表结构log_id timestamp thread_id severity message
                          v_message = list_field[3].replace('\n', '')
                          v_message = v_message.replace("'","\\\'")
                          v_sql = "insert ignore into t_data_mysqld_log(timestamp,thread_id,severity,message) values ('{0}','{1}','{2}','{3}');".format(list_field[0],list_field[1],list_field[2],v_message)
                          #print(v_sql)
                          list_sql.append(v_sql)

            print('日志文件中记录数：', cnt)
            #print(list_sql)
            add_record=fun_insert_table(list_sql,'t_data_mysqld_log')
            print('本次数据库新增行数：', add_record)
            #print(add_record)
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            print ('耗时',delta.seconds,'秒')
            return add_record


    except Exception as err:
        print(err)
        return err

if __name__ == '__main__':
    fun_resolve_mysql_log(r'mysqld.log')
