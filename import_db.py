# coding: utf-8
import mysql.connector

def fun_insert_table(v_list_sql,v_table_name):
        try:
            conn = mysql.connector.connect(user='nprobe', password='nprobe', host='132.232.57.199',database='db_nprobe',buffered=True)
            cursor = conn.cursor()
            cursor.execute('select count(*) from {0}'.format(v_table_name))
            pre_record  = cursor.fetchone()
            for v_sql in v_list_sql:
                #print(v_sql)
                cursor.execute(v_sql)
            cursor.execute('select count(*) from {0}'.format(v_table_name))
            cur_record  = cursor.fetchone()
            add_record = cur_record[0] - pre_record[0]

        except Exception as err:
            print(err)
        cursor.close()
        conn.commit()
        conn.close()
        return add_record

if __name__ == '__main__':
    fun_insert_table(['select * from t_data_mysqld_log;'],'t_exec_log')