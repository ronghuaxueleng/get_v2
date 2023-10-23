# -*- coding: utf-8 -*-

import datetime
from peewee import *

db = SqliteDatabase('infos.db')


class Info(Model):
    _id = PrimaryKeyField
    postId = CharField(unique=True)
    userName = CharField()
    url = CharField(null=True)
    imagesCount = IntegerField(null=True)
    state = CharField(default=0)
    createdTime = DateTimeField(default=datetime.datetime.now)
    grabState = IntegerField(default=0, null=False)  # 抓取状态
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


class Image(Model):
    _id = PrimaryKeyField
    root_url = CharField()
    image_url = CharField()
    createdTime = DateTimeField(default=datetime.datetime.now)
    grabState = IntegerField(default=0, null=False)  # 抓取状态
    timestamp = DateTimeField(null=True, default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


def delete_prompt():
    return Info.delete().execute()


def init_table():
    db.connect()
    db.create_tables([Info, Image])


if __name__ == '__main__':
    db.connect()
    db.create_tables([Info, Image])
