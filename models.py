import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('spacex.sqlite')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        db_tables = 'users'
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print("TABLES Created")
    DATABASE.close()