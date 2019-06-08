# coding: utf-8

import json
import mysql.connector
from flask import jsonify



def fun_query_mysql_data(v_ts):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',
                                       database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "select * from t_data_mysqld_log where timestamp like '{0}%' order by timestamp desc".format(v_ts)
        print(v_sql)
        cursor.execute(v_sql)
        rows = cursor.fetchall()
        result_list = []
        row_count = 0
        # dic_row = {"log_id": "1", "timestamp": "2", "thread_id": "3", "severity": "4", "message": "5"}
        for record in rows:
            row_count = row_count + 1
            # print(record)
            dic_row = {"log_id": "1", "timestamp": "2", "thread_id": "3", "severity": "4", "message": "5"}
            dic_row["log_id"] = record[0]
            dic_row["timestamp"] = record[1]
            dic_row["thread_id"] = record[2]
            dic_row["severity"] = record[3]
            dic_row["message"] = record[4]
            # print(dic_row)
            result_list.append(dic_row)
        # print(result_list)
        dic_result = {"total": "1", "rows": "2"}
        dic_result["total"] = row_count;
        dic_result["rows"] = result_list;
        #print(json.dumps(dic_result))
        return jsonify(dic_result)

    except Exception as err:
        print(err)

    cursor.close()
    conn.close()



def fun_query_uwsgi_data(v_ts):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',
                                       database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "select * from t_data_uwsgi_log where FROM_UNIXTIME(unix_timestamp/1000, '%Y-%m-%d %H:%i:%s') like '{0}%' order by unix_timestamp desc".format(v_ts)
        print(v_sql)
        cursor.execute(v_sql)
        rows = cursor.fetchall()
        result_list = []
        row_count = 0

        for record in rows:
            row_count = row_count + 1
            # print(record)
            dic_row = {"log_id": "1", "unix_timestamp": "2", "remote_addr": "3", "remote_user": "4", "request_time": "5", "request_method": "6", "request_uri": "7", "server_protocol": "8","status": "9", "size": "10", "http_referer": "11", "http_user_agent": "12"}
            dic_row["log_id"] = record[0]
            dic_row["unix_timestamp"] = record[1]
            dic_row["remote_addr"] = record[2]
            dic_row["remote_user"] = record[3]
            dic_row["request_time"] = record[4]
            dic_row["request_method"] = record[5]
            dic_row["request_uri"] = record[6]
            dic_row["server_protocol"] = record[7]
            dic_row["status"] = record[8]
            dic_row["size"] = record[9]
            dic_row["http_referer"] = record[10]
            dic_row["http_user_agent"] = record[11]
            # print(dic_row)
            result_list.append(dic_row)
        # print(result_list)
        dic_result = {"total": "1", "rows": "2"}
        dic_result["total"] = row_count;
        dic_result["rows"] = result_list;
        #print(json.dumps(dic_result))
        return jsonify(dic_result)

    except Exception as err:
        print(err)
    finally:
        cursor.close()
        conn.close()



def fun_query_nginx_access_data(v_ts):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',
                                       database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "select * from t_data_nginx_access_log where FROM_UNIXTIME(msec, '%Y-%m-%d %H:%i:%s') like '{0}%' order by msec desc".format(v_ts)
        print(v_sql)
        cursor.execute(v_sql)
        rows = cursor.fetchall()
        result_list = []
        row_count = 0

        for record in rows:
            row_count = row_count + 1
            # print(record)
            dic_row = {"log_id": "1", "msec": "2", "remote_addr": "3", "remote_user": "4", "time_local": "5", "request": "6", "status": "7", "body_bytes_sent": "8", "http_referer": "9", "http_user_agent": "10", "http_x_forwarded_for": "11"}
            dic_row["log_id"] = record[0]
            dic_row["msec"] = record[1]
            dic_row["remote_addr"] = record[2]
            dic_row["remote_user"] = record[3]
            dic_row["time_local"] = record[4]
            dic_row["request"] = record[5]
            dic_row["status"] = record[6]
            dic_row["body_bytes_sent"] = record[7]
            dic_row["http_referer"] = record[8]
            dic_row["http_user_agent"] = record[9]
            dic_row["http_x_forwarded_for"] = record[10]
            # print(dic_row)
            result_list.append(dic_row)
        # print(result_list)
        dic_result = {"total": "1", "rows": "2"}
        dic_result["total"] = row_count;
        dic_result["rows"] = result_list;
        #print(json.dumps(dic_result))
        return jsonify(dic_result)

    except Exception as err:
        print(err)

    cursor.close()
    conn.close()





def fun_query_linux_secure_data(v_ts):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',
                                       database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "select * from t_data_linux_secure_log where iso_8601 like '{0}%' and event like '%Failed%' order by iso_8601 desc".format(v_ts)
        print(v_sql)
        cursor.execute(v_sql)
        rows = cursor.fetchall()
        result_list = []
        row_count = 0
        # dic_row = {"log_id": "1", "iso_8601": "2", "ctime": "3","host": "4", "process_id": "5", "event": "6"}
        for record in rows:
            row_count = row_count + 1
            # print(record)
            dic_row = {"log_id": "1", "iso_8601": "2", "ctime": "3","host": "4", "process_id": "5", "event": "6"}
            dic_row["log_id"] = record[0]
            dic_row["iso_8601"] = record[1]
            dic_row["ctime"] = record[2]
            dic_row["host"] = record[3]
            dic_row["process_id"] = record[4]
            dic_row["event"] = record[5]
            # print(dic_row)
            result_list.append(dic_row)
        # print(result_list)
        dic_result = {"total": "1", "rows": "2"}
        dic_result["total"] = row_count;
        dic_result["rows"] = result_list;
        #print(json.dumps(dic_result))  #测试
        return jsonify(dic_result)

    except Exception as err:
        print(err)

    cursor.close()
    conn.close()





def fun_query_linux_messages_data(v_ts):
    try:
        conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',
                                       database='db_nprobe',
                                       buffered=True)
        cursor = conn.cursor()
        v_sql = "select * from t_data_linux_messages_log where iso_8601 like '{0}%' order by iso_8601 desc".format(v_ts)
        print(v_sql)
        cursor.execute(v_sql)
        rows = cursor.fetchall()
        result_list = []
        row_count = 0
        # dic_row = {"log_id": "1", "iso_8601": "2", "ctime": "3","host": "4", "process_id": "5", "event": "6"}
        for record in rows:
            row_count = row_count + 1
            # print(record)
            dic_row = {"log_id": "1", "iso_8601": "2", "ctime": "3","host": "4", "process_id": "5", "event": "6"}
            dic_row["log_id"] = record[0]
            dic_row["iso_8601"] = record[1]
            dic_row["ctime"] = record[2]
            dic_row["host"] = record[3]
            dic_row["process_id"] = record[4]
            dic_row["event"] = record[5]
            # print(dic_row)
            result_list.append(dic_row)
        # print(result_list)
        dic_result = {"total": "1", "rows": "2"}
        dic_result["total"] = row_count;
        dic_result["rows"] = result_list;
        #print(json.dumps(dic_result))  #测试
        return jsonify(dic_result)

    except Exception as err:
        print(err)

    cursor.close()
    conn.close()





if __name__ == '__main__':
    fun_query_linux_messages_data("2018-09-14")
