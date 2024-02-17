from database.user.entities.student_entity import StudentEntity
from database.user.entities.teacher_entity import TeacherEntity
from database.user.entities.user_entity import UserEntity

__STUDENT_ROLE_ID = 1
__TEACHER_ROLE_ID = 2


def get_user_by_chat_id(c_id) -> UserEntity:
    user = UserEntity.get_or_none(UserEntity.chat_id == c_id)
    return user


def get_students_by_dep_id(dep_id):
    return StudentEntity.select().where(StudentEntity.department_id == dep_id)


def get_student_by_id(user_id) -> StudentEntity:
    return StudentEntity.get_or_none(StudentEntity.user_id == user_id)


def get_teachers_by_dep_id(dep_id):
    return TeacherEntity.select().where(TeacherEntity.department_id == dep_id)


def get_teacher_by_id(user_id) -> TeacherEntity:
    return TeacherEntity.get_or_none(TeacherEntity.user_id == user_id)


def create_student(chat_id, group, department_id):
    user = UserEntity.create(chat_id=chat_id, user_role_id=__STUDENT_ROLE_ID)
    StudentEntity.create(user_id=user.id, group_name=group, department_id=department_id)


def create_teacher(chat_id, first_name, last_name, department_id):
    user = UserEntity.create(chat_id=chat_id, user_role_id=__TEACHER_ROLE_ID)
    TeacherEntity.create(user_id=user.id, first_name=first_name, last_name=last_name, department_id=department_id)


def delete_user_by_chat_id(c_id):
    qry = UserEntity.delete().where(UserEntity.chat_id == c_id)
    qry.execute()
