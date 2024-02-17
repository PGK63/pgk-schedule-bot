from peewee import TextField, ForeignKeyField

from database.common.BaseModel import BaseModel
from database.department.entities.department_entity import DepartmentEntity
from database.user.entities.user_entity import UserEntity


class TeacherEntity(BaseModel):
    user_id = ForeignKeyField(UserEntity, field='user_id', to_field='id', primary_key=True)
    first_name = TextField(column_name="first_name")
    last_name = TextField(column_name="last_name")
    department_id = ForeignKeyField(DepartmentEntity, field='department_id', to_field='id')

    class Meta:
        table_name = 'teachers'
