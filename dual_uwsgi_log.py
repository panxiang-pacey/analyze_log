# coding: utf-8
import re
import datetime
from import_db import fun_insert_table

def fun_resolve_uwsgi_log(v_LogFile):
    i=0
    cnt=0
    list_sql=[]
    start_time = datetime.datetime.now()
    try:
        with open(v_LogFile,'r', encoding='latin1') as f: #, encoding='utf-8'  latin1 通过vim查看文件编码 :set fileencoding
            list_allline = f.readlines()
            rowcount=len(list_allline)
            f.seek(0,0)

            while i < rowcount:
                   i = i + 1
                   line = f.readline()

                   #if len(line) > 1 :
                   if re.match(r'^"\d{13}"', line): #毫秒
                          cnt = cnt + 1
                          #print(line)
                          #逐行处理每条记录
                          list_field = re.findall(r'"(.*?)"\s',line) #20181207修复"/WebID/IISWebAgentIF.dll?postdata="><script>foo</script>"
                          #print(list_field)
                          # 表结构log_id unix_timestamp remote_addr remote_user request_time request_method request_uri server_protocol status size http_referer http_user_agent
                          v_request_uri = list_field[5].replace("'", "\\\'")
                          v_request_uri= v_request_uri.replace("\\'", "\"") #20181208修复
                          v_http_user_agent = list_field[10].replace("'", "\\\'")
                          v_sql = "insert ignore into t_data_uwsgi_log(unix_timestamp,remote_addr,remote_user,request_time,request_method,request_uri,server_protocol,status,size,http_referer,http_user_agent) " \
                                  "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}','{10}');".format(list_field[0],list_field[1],list_field[2],list_field[3],list_field[4],v_request_uri,list_field[6],list_field[7],list_field[8],list_field[9],v_http_user_agent)
                          #print(v_sql)
                          list_sql.append(v_sql)

            print('日志文件中记录数：', cnt)
            #print(len(list_sql))
            add_record=fun_insert_table(list_sql,'t_data_uwsgi_log')
            print('本次数据库新增行数：', add_record)
            end_time = datetime.datetime.now()
            delta = end_time - start_time
            print ('耗时',delta.seconds,'秒')
            return add_record


    except Exception as err:
        print(err)
        return err

if __name__ == '__main__':
    fun_resolve_uwsgi_log(r'uwsgi.log')