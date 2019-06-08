# coding: utf-8
import re
import datetime
from import_db import fun_insert_table

def fun_resolve_linux_messages_log(v_LogFile):
    i=0
    cnt=0
    list_sql=[]
    start_time = datetime.datetime.now()
    try:
        with open(v_LogFile,'r', encoding='utf-8') as f:
            list_allline = f.readlines()
            rowcount=len(list_allline)
            f.seek(0,0)

            #获取前一小时
            now_dt = end_time = datetime.datetime.now()
            delta_one = now_dt + datetime.timedelta(hours=-1)
            one_dt = delta_one.strftime("%Y-%m-%d %H")
            print('抽取'+one_dt+'时的日志')

            while i < rowcount:
                   i = i + 1
                   line = f.readline()

                   if len(line) > 1 :
                          cnt = cnt + 1
                          #print(line)
                          #逐行处理每条记录
                          ctime = line[0:15]
                          iso_8601 = fun_iso_8601(ctime)
                          #print(iso_8601)
                          list_field_3 = line[16:].split(' ', 1)  # 限制分裂次数
                          host = list_field_3[0]
                          list_field_2 = list_field_3[1].split(':', 1)  # 限制分裂次数
                          process_id = list_field_2[0]
                          event = list_field_2[1]

                          #取前一小时的数据
                          #print(iso_8601) #2018-09-10 09:28:41
                          #one_dt = '2018-09-14 14' #测试
                          if iso_8601[0:13] == one_dt:
                              # 表结构log_id iso_8601  ctime  host process_id event
                              event = event.replace("'", "\\\'")
                              v_sql = "insert into t_data_linux_messages_log(iso_8601,ctime,host,process_id,event) " \
                                      "values ('{0}','{1}','{2}','{3}','{4}');".format(iso_8601,ctime,host,process_id,event)
                              #print(v_sql)
                              list_sql.append(v_sql)

            print('日志文件中记录数：', cnt)
            #print(list_sql[0]) #list index out of range  无数据
            add_record=fun_insert_table(list_sql,'t_data_linux_messages_log')
            print('本次数据库新增行数：', add_record)
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            print ('耗时',delta.seconds,'秒')
            return add_record


    except Exception as err:
        print(err)
        return err

def fun_iso_8601(v_ctime):
    dic_month = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04', 'May': '05', 'Jun': '06','Jul': '07', 'Aug': '08', 'Sep': '09','Oct': '10', 'Nov': '11', 'Dec': '12'};
    cur_dt = end_time = datetime.datetime.now()
    delta = cur_dt + datetime.timedelta(hours=-1)
    year = delta.strftime("%Y")
    en_month = v_ctime[0:3]
    num_month = dic_month.get(en_month,'00')
    day_time = v_ctime[4:].strip().zfill(11)  #处理个位数字的天数 zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    str_datetime = year + '-' + num_month + '-' + day_time
    #print(str_datetime)
    return str_datetime


if __name__ == '__main__':
    fun_resolve_linux_messages_log(r'messages')


