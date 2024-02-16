from peewee import PrimaryKeyField, TextField, IntegerField, ForeignKeyField

from database.common.BaseModel import BaseModel
from database.department.entities.department_entity import DepartmentEntity


class TeacherEntity(BaseModel):
    user_id = PrimaryKeyField(column_name='user_id')
    first_name = TextField(column_name="first_name")
    last_name = TextField(column_name="last_name")
    department_id = ForeignKeyField(DepartmentEntity, field='department_id', to_field="id")

    class Meta:
        table_name = 'teachers'
