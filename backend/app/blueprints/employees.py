from flask import Blueprint, g, request
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models import Employee, Role
from ..services.core import APIError, auth_required, require_fields, success
from ..services.serializers import employee_to_dict


bp = Blueprint("employees", __name__, url_prefix="/api/employees")


def scoped_query(user):
    query = Employee.query
    if user.role.code == "manager":
        query = query.filter(Employee.department_id == user.department_id)
    elif user.role.code == "employee":
        query = query.filter(Employee.id == user.id)
    return query


@bp.get("")
@auth_required
def list_employees():
    user = g.current_user
    query = scoped_query(user)
    keyword = request.args.get("keyword", "").strip()
    dept_id = request.args.get("dept_id", type=int)
    role_id = request.args.get("role_id", type=int)
    page = request.args.get("page", default=1, type=int)
    page_size = min(request.args.get("page_size", default=10, type=int), 50)

    if dept_id and user.role.code == "admin":
        query = query.filter(Employee.department_id == dept_id)
    if role_id:
        query = query.filter(Employee.role_id == role_id)
    if keyword:
        like_value = f"%{keyword}%"
        query = query.filter(
            or_(
                Employee.employee_no.like(like_value),
                Employee.full_name.like(like_value),
                Employee.username.like(like_value),
            )
        )

    total = query.count()
    rows = (
        query.order_by(Employee.department_id.asc(), Employee.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return success({"items": [employee_to_dict(row) for row in rows], "total": total})


@bp.post("")
@auth_required
def create_employee():
    user = g.current_user
    if user.role.code not in ("admin", "manager"):
        raise APIError("当前角色无权新增员工。", 403)

    payload = request.get_json(silent=True) or {}
    require_fields(
        payload,
        "employee_no",
        "username",
        "full_name",
        "email",
        "department_id",
        "role_id",
        "password",
    )
    department_id = int(payload["department_id"])
    if user.role.code == "manager" and department_id != user.department_id:
        raise APIError("部门负责人只能新增本部门员工。", 403)
    role_id = int(payload["role_id"])
    if user.role.code == "manager":
        employee_role = Role.query.get(role_id)
        if not employee_role or employee_role.code != "employee":
            raise APIError("部门负责人只能新增普通员工账号。", 403)

    employee = Employee(
        employee_no=payload["employee_no"].strip(),
        username=payload["username"].strip(),
        password_hash=generate_password_hash(payload["password"]),
        full_name=payload["full_name"].strip(),
        email=payload["email"].strip(),
        phone=payload.get("phone", "").strip(),
        title=payload.get("title", "").strip(),
        education=payload.get("education", "本科").strip(),
        department_id=department_id,
        role_id=role_id,
        status=payload.get("status", "active"),
    )
    db.session.add(employee)
    db.session.commit()
    return success(employee_to_dict(employee), "新增员工成功")


@bp.put("/<int:employee_id>")
@auth_required
def update_employee(employee_id):
    user = g.current_user
    if user.role.code not in ("admin", "manager"):
        raise APIError("当前角色无权修改员工。", 403)
    employee = scoped_query(user).filter(Employee.id == employee_id).first()
    if not employee:
        raise APIError("员工不存在。", 404)

    payload = request.get_json(silent=True) or {}
    for field in ("full_name", "email", "phone", "title", "education", "status"):
        if field in payload:
            setattr(employee, field, payload[field].strip() if isinstance(payload[field], str) else payload[field])

    if "department_id" in payload:
        department_id = int(payload["department_id"])
        if user.role.code == "manager" and department_id != user.department_id:
            raise APIError("部门负责人只能分配本部门。", 403)
        employee.department_id = department_id

    if "role_id" in payload and user.role.code == "admin":
        employee.role_id = int(payload["role_id"])

    if payload.get("password"):
        employee.password_hash = generate_password_hash(payload["password"])

    db.session.commit()
    return success(employee_to_dict(employee), "员工信息已更新")
