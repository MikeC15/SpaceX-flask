import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('spacex.sqlite')


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_tables = 'users'
        database = DATABASE

class Comment(Model):
    content = CharField()
    likes = IntegerField()
    flight_number = CharField()
    user = ForeignKeyField(User, related_name='comments')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_tables = 'comments'
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Comment], safe=True)
    print("TABLES Created")
    DATABASE.close()