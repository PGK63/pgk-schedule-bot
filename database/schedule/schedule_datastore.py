from database.schedule.model.schedule_entity import ScheduleEntity


def create_schedule(json, department_id, date):
    ScheduleEntity.create(json=json, department_id=department_id, date=date)
