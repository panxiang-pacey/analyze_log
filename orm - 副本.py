# coding: utf-8
from flask_login import UserMixin
from web_app import db

class User(db.Model, UserMixin):#从 UserMixin 继承
    __tablename__ = 't_user'
    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_code = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(100))
    user_password = db.Column(db.String(100))


    def __init__(self, user_code,user_name, user_password):
        self.user_code = user_code
        self.user_name = user_name
        self.user_password = user_password

    def __repr__(self):
        return '<User %r>' % self.user_name

    # get_id()方法默认返回的用户的id. 如果用户不存在,应该返回None.
    def get_id(self):
        return self.user_id






