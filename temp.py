# coding: utf-8
#利用python的re模块通过正则表达式对日志进行分析处理
#通过Python的re模块，按照应用服务器的日志格式编写正则

import re

#https://zhuanlan.zhihu.com/p/32686063
##### 自定义部分 #####
# 定义日志格式，利用非贪婪匹配和分组匹配，需要严格参照日志定义中的分隔符和引号
log_pattern = r'^(?P<remote_addr>.*?) - \[(?P<time_local>.*?)\] "(?P<request>.*?)"' \
              r' (?P<status>.*?) (?P<body_bytes_sent>.*?)' \
              r' "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)" - (?P<http_x_forwarded_for>.*)$'
# request的正则，其实是由 "request_method request_uri server_protocol"三部分组成
request_uri_pattern = r'^(?P<request_method>(GET|POST|HEAD|DELETE)?) (?P<request_uri>.*?) (?P<server_protocol>HTTP.*)$'
# 日志目录
log_dir = 'log.txt'


##### 自定义部分结束 #####

i = 0
cnt = 0

try:
    with open(log_dir, 'r') as f:
        list_allline = f.readlines()
        rowcount = len(list_allline)
        f.seek(0, 0)

        while i < rowcount:
            i = i + 1
            line_str = f.readline()

            log_pattern_obj = re.compile(log_pattern)

            processed = log_pattern_obj.search(line_str)
            print(processed)
            if not processed:
                    '''如果正则根本就无法匹配该行记录时'''
                    print("Can't process this line: {}".format(line_str))
                    #return server, '', 0, '', 0, '', '', '', '', '', ''
            else:
                pass
                    # remote_addr (客户若不经过代理，则可认为用户的真实ip)
                    #remote_addr = processed.group('remote_addr')

                    # time_local
                    #time_local = processed.group('time_local')
except Exception as err:
    print(err)


