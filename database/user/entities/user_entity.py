from peewee import PrimaryKeyField, IntegerField

from database.common.BaseModel import BaseModel


class UserEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    chat_id = IntegerField(column_name='chat_id')

    class Meta:
        table_name = 'users'
