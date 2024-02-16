from database.user.entities.student_entity import StudentEntity
from database.user.entities.teacher_entity import TeacherEntity
from database.user.entities.user_entity import UserEntity


def create_student(t_id, chat_id, group, department_id):
    UserEntity.create(id=t_id, chat_id=chat_id)
    StudentEntity.create(user_id=t_id, group_name=group, department_id=department_id)


def create_teacher(t_id, chat_id, first_name, last_name, department_id):
    UserEntity.create(id=t_id, chat_id=chat_id)
    TeacherEntity.create(user_id=t_id, first_name=first_name, last_name=last_name, department_id=department_id)
