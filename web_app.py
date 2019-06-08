# coding: utf-8
import os
import datetime
from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from query_data import fun_query_mysql_data
from query_data import fun_query_nginx_access_data
from query_data import fun_query_uwsgi_data
from query_data import fun_query_linux_secure_data
from query_data import fun_query_linux_messages_data

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from parse_config import fun_get_conn_str

app = Flask(__name__)
app.debug = True

# 驱动MySQL-connector-python
#conn_str = 'mysql+mysqlconnector://nprobe:nprobe@132.232.57.199:3306/db_nprobe?charset=utf8mb4'
conn_str = fun_get_conn_str()
print(conn_str)

engine = create_engine(conn_str,pool_size=100,pool_recycle=3600)  #,pool_pre_ping=True
#针对与MySQL操作相关的错误引发此异常。例如：连接太多; 主机名无法解析; 握手不好; 服务器正在关闭，通信错误。
#engine = create_engine(conn_str,poolclass=NullPool)  #禁用连接池 'NoneType' object has no attribute 'twophase'

DBSession = sessionmaker(bind=engine)
session = DBSession()

app.config["SECRET_KEY"] = os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。



#flask_login模块
login_manager = LoginManager()
login_manager.init_app(app) #延迟创建app
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.login_message = "请登录后查看！"
login_manager.login_message_category = "info"


@login_manager.user_loader #回调函数
#根据 user_id 找到对应的 user 对象,
# 如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.
def load_user(user_id):
    from orm import User
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
    except Exception as err:
        print('load_user函数错误：')
        print(err)
        session.rollback()
    finally:
       session.close()
        #user = session.query(User).filter_by(user_id=user_id).first() #UnboundLocalError: local variable 'user' referenced before assignment
    return user
#如果一次启动多个实例，报'NoneType' object has no attribute 'twophase'错误



@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    #用户提交登录信息进行验证
    if request.method == "POST":
        username = request.form.get('username',type=str,default=None) #未输入返回None
        password = request.form.get('password',type=str,default=None)
        if request.form.get("remember"):#选中on，不选中None
            remember_checked = True
        else:
            remember_checked = False
        #print(request.form.get("remember"))
        #先判断是否输入用户名和密码
        if len(username) > 0 and len(password) > 0:
            #print(username)
            #print(username)
            # 获取要登陆的用户对象
            from orm import User
            try:
                #user = User.query.filter_by(user_code=username,user_password=password).first()
                user = session.query(User).filter_by(user_code=username,user_password=password).first()
            except Exception as err:
                print(err)
                session.rollback()
            finally:
                session.close()
            print(user)
            if user:
                login_user(user,remember=remember_checked) #用户名密码正确，允许登录（设置为已登录状态，将user_id等信息存入Session中）#记住我
                #return render_template('home.html')
                return redirect(url_for('home')) #url地址栏显示正确
            #用户名密码不正确
            else:
                error = '用户名或密码错误，请重新登录!'
                return render_template('login.html', error=error)

        #未输入用户名或密码
        else:
            error = '请输入用户名和密码进行登录!'
            return render_template('login.html', error=error)

    #用户访问登录界面
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))  # url地址栏显示正确



@app.route('/mysql', methods=['GET', 'POST'])
@login_required
def mysql():
    #print(request.get_data())
    now = datetime.datetime.now()
    str_date = now.strftime('%Y-%m-%d')
    #print('str_date:',str_date)
    if request.method == "POST":
        ts = request.form.get('timestamp', type=str, default = str_date)
        print(ts)
        json_data = fun_query_mysql_data(ts)
        return json_data
    else:
        return render_template('mysql.html')



@app.route('/nginx_access', methods=['GET', 'POST'])
@login_required
def nginx_access():
    #print(request.get_data())
    now = datetime.datetime.now()
    str_date = now.strftime('%Y-%m-%d')
    #print('str_date:',str_date)
    if request.method == "POST":
        ts = request.form.get('timestamp', type=str, default = str_date)
        print(ts)
        json_data = fun_query_nginx_access_data(ts)
        return json_data
    else:
        return render_template('nginx_access.html')


@app.route('/uwsgi', methods=['GET', 'POST'])
@login_required
def uwsgi():
    #print(request.get_data())
    now = datetime.datetime.now()
    str_date = now.strftime('%Y-%m-%d')
    #print('str_date:',str_date)
    if request.method == "POST":
        ts = request.form.get('timestamp', type=str, default = str_date)
        print(ts)
        json_data = fun_query_uwsgi_data(ts)
        return json_data
    else:
        return render_template('uwsgi.html')



@app.route('/linux_messages', methods=['GET', 'POST'])
@login_required
def linux_messages():
    #print(request.get_data())
    now = datetime.datetime.now()
    str_date = now.strftime('%Y-%m-%d')
    #print('str_date:',str_date)
    if request.method == "POST":
        ts = request.form.get('timestamp', type=str, default = str_date)
        print(ts)
        json_data = fun_query_linux_messages_data(ts)
        return json_data
    else:
        return render_template('linux_messages.html')



@app.route('/linux_secure', methods=['GET', 'POST'])
@login_required
def linux_secure():
    #print(request.get_data())
    now = datetime.datetime.now()
    str_date = now.strftime('%Y-%m-%d')
    #print('str_date:',str_date)
    if request.method == "POST":
        ts = request.form.get('timestamp', type=str, default = str_date)
        print(ts)
        begin_dt = datetime.datetime.now() #20180926 调试记录多时datagrid加载错误
        json_data = fun_query_linux_secure_data(ts)
        print(json_data) #20180926 调试记录多时datagrid加载错误
        end_dt = datetime.datetime.now() #20180926 调试记录多时datagrid加载错误
        delta = end_dt - begin_dt #20180926 调试记录多时datagrid加载错误
        run_seconds = delta.seconds #20180926 调试记录多时datagrid加载错误
        print(run_seconds) #20180926 调试记录多时datagrid加载错误
        return json_data
    else:
        return render_template('linux_secure.html')









if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)