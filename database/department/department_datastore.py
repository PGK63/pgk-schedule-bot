from database.department.entities.department_entity import DepartmentEntity


def get_departments():
    return DepartmentEntity.select()
