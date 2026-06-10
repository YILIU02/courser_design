from flask import Blueprint, g

from ..models import Department, Employee, Role
from ..services.core import auth_required, success


bp = Blueprint("meta", __name__, url_prefix="/api/meta")


@bp.get("/options")
@auth_required
def options():
    user = g.current_user
    employee_query = Employee.query.filter(Employee.status == "active")
    if user.role.code == "manager":
        employee_query = employee_query.filter(Employee.department_id == user.department_id)
    elif user.role.code == "employee":
        employee_query = employee_query.filter(Employee.id == user.id)

    return success(
        {
            "departments": [
                {"id": department.id, "code": department.code, "name": department.name}
                for department in Department.query.order_by(Department.id).all()
            ],
            "roles": [
                {"id": role.id, "code": role.code, "name": role.name}
                for role in Role.query.order_by(Role.id).all()
            ],
            "employees": [
                {
                    "id": employee.id,
                    "employee_no": employee.employee_no,
                    "full_name": employee.full_name,
                    "department_id": employee.department_id,
                    "department_name": employee.department.name,
                    "role_code": employee.role.code,
                }
                for employee in employee_query.order_by(Employee.department_id, Employee.id).all()
            ],
            "leave_types": ["年假", "病假", "事假", "调休", "婚假"],
            "project_statuses": ["planned", "active", "paused", "completed"],
        }
    )
