from peewee import PrimaryKeyField, IntegerField, ForeignKeyField

from database.common.BaseModel import BaseModel
from database.user.entities.user_role_entity import UserRoleEntity


class UserEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    chat_id = IntegerField(column_name='chat_id')
    user_role_id = ForeignKeyField(UserRoleEntity, field='user_role_id', to_field='id')

    class Meta:
        table_name = 'users'
