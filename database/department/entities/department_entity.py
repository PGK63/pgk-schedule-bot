from peewee import TextField, PrimaryKeyField

from database.common.BaseModel import BaseModel


class DepartmentEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = TextField(column_name="name")

    class Meta:
        table_name = 'departments'
