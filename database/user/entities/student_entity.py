from peewee import PrimaryKeyField, TextField, ForeignKeyField

from database.common.BaseModel import BaseModel
from database.department.entities.department_entity import DepartmentEntity


class StudentEntity(BaseModel):
    user_id = PrimaryKeyField(column_name='user_id')
    group_name = TextField(column_name="group_name")
    department_id = ForeignKeyField(DepartmentEntity, field='department_id', to_field="id")

    class Meta:
        table_name = 'students'
