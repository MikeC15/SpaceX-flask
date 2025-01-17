import os #for deployment
from playhouse.db_url import connect#deploymeny
import datetime
from peewee import *
from flask_login import UserMixin

#use if line if live, else in development
if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
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
    def __str__(self):
        return "<Comment: {}, id: {}>".format(self.content, self.id)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Comment], safe=True)
    print("TABLES Created")
    DATABASE.close()