from peewee import PrimaryKeyField, TextField

from database.common.BaseModel import BaseModel


class UserRoleEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    role = TextField(column_name='role')

    class Meta:
        table_name = 'user_roles'
