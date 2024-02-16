from peewee import Model, PostgresqlDatabase

db = PostgresqlDatabase('pgk-schedule', user='postgres', password='danbelZzAa6190',
                        host='danbel.ru', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db
