# coding: utf-8
import re
import datetime
from import_db import fun_insert_table

def fun_resolve_nginx_access_log(v_LogFile):
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

                   if re.match(r'^\d{10}.\d{3}', line):
                          cnt = cnt + 1
                          #print(line)
                          #逐行处理每条记录
                          '''  $msec
                            $remote_addr - $remote_user 
                            [$time_local] 
                            $request
                            $status 
                            $body_bytes_sent 
                            $http_referer
                            $http_user_agent
                            $http_x_forwarded_for
                        '''
                          list_field = line.split(' ',4)
                          msec=list_field[0]
                          remote_addr = list_field[1]
                          remote_user = list_field[3]
                          list_temp=re.split('"',list_field[4])
                          time_local = list_temp[0]
                          request=list_temp[1]
                          list_2=list_temp[2].strip().split(' ')
                          status=list_2[0]
                          body_bytes_sent=list_2[1]
                          http_referer=list_temp[3]
                          http_user_agent=list_temp[5]
                          http_x_forwarded_for=list_temp[7]
                          #print(request)
                          #print(http_user_agent)
                          request = request.replace("'", "\\\'") #20180904
                          #request = request.replace("`", "\`")  #反引号

                          # 表结构#log_id msec remote_addr remote_user time_local reqest status body_bytes_sent http_referer http_user_agent http_x_forwarded_for

                          v_sql = "insert ignore into t_data_nginx_access_log(msec,remote_addr,remote_user,time_local,request,status,body_bytes_sent,http_referer,http_user_agent,http_x_forwarded_for) values ('{0}','{1}','{2}','{3}','{4}','{5}',{6},'{7}','{8}','{9}');".format(msec,remote_addr,remote_user,time_local,request,status,body_bytes_sent,http_referer,http_user_agent,http_x_forwarded_for)
                          #print(v_sql)
                          list_sql.append(v_sql)

            print('日志文件中记录数：',cnt)
            #print(list_sql)
            add_record=fun_insert_table(list_sql,'t_data_nginx_access_log')
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
    fun_resolve_nginx_access_log(r'access.log')
