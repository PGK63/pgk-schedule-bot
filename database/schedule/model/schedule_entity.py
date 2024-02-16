from peewee import PrimaryKeyField, Field, ForeignKeyField, DateField

from database.common.BaseModel import BaseModel
from database.department.entities.department_entity import DepartmentEntity


class ScheduleEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    json = Field(column_name='json')
    department_id = ForeignKeyField(DepartmentEntity, field='department_id', to_field="id")
    date = DateField(column_name='date')

    class Meta:
        table_name = 'schedules'
