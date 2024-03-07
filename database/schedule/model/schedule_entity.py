from peewee import PrimaryKeyField, Field, DateField

from database.common.BaseModel import BaseModel


class ScheduleEntity(BaseModel):
    id = PrimaryKeyField(column_name='id')
    json = Field(column_name='json')
    department_id = Field(column_name='department_id')
    date = DateField(column_name='date')

    class Meta:
        table_name = 'schedules'
