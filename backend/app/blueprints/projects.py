from datetime import datetime

from flask import Blueprint, g, request
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models import Employee, Project, ProjectMember
from ..services.core import APIError, auth_required, require_fields, success
from ..services.serializers import project_to_dict


bp = Blueprint("projects", __name__, url_prefix="/api/projects")


def scoped_query(user):
    query = Project.query.options(selectinload(Project.members).selectinload(ProjectMember.employee))
    if user.role.code == "manager":
        query = query.filter(Project.department_id == user.department_id)
    elif user.role.code == "employee":
        query = query.join(ProjectMember, ProjectMember.project_id == Project.id).filter(ProjectMember.employee_id == user.id)
    return query


@bp.get("")
@auth_required
def list_projects():
    user = g.current_user
    query = scoped_query(user)
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status", "").strip()
    dept_id = request.args.get("dept_id", type=int)

    if keyword:
        like_value = f"%{keyword}%"
        query = query.filter(or_(Project.name.like(like_value), Project.project_code.like(like_value)))
    if status:
        query = query.filter(Project.status == status)
    if dept_id and user.role.code == "admin":
        query = query.filter(Project.department_id == dept_id)

    rows = query.order_by(Project.updated_at.desc()).all()
    return success([project_to_dict(row) for row in rows])


@bp.post("")
@auth_required
def create_project():
    user = g.current_user
    if user.role.code not in ("admin", "manager"):
        raise APIError("当前角色无权新增项目。", 403)

    payload = request.get_json(silent=True) or {}
    require_fields(payload, "project_code", "name", "department_id", "manager_id", "start_date")
    department_id = int(payload["department_id"])
    if user.role.code == "manager" and department_id != user.department_id:
        raise APIError("部门负责人只能创建本部门项目。", 403)

    manager = Employee.query.get(int(payload["manager_id"]))
    if not manager:
        raise APIError("项目负责人不存在。", 404)
    if manager.department_id != department_id:
        raise APIError("项目负责人必须属于项目所在部门。")

    project = Project(
        project_code=payload["project_code"].strip(),
        name=payload["name"].strip(),
        summary=payload.get("summary", "").strip(),
        status=payload.get("status", "planned"),
        priority=payload.get("priority", "medium"),
        progress=int(payload.get("progress", 0)),
        budget=payload.get("budget", 0) or 0,
        start_date=datetime.fromisoformat(payload["start_date"]).date(),
        end_date=datetime.fromisoformat(payload["end_date"]).date() if payload.get("end_date") else None,
        department_id=department_id,
        manager_id=manager.id,
    )
    db.session.add(project)
    db.session.flush()

    member_ids = {manager.id, *[int(member_id) for member_id in payload.get("member_ids", [])]}
    members = Employee.query.filter(Employee.id.in_(member_ids)).all() if member_ids else []
    for member in members:
        if member.department_id != department_id:
            raise APIError("项目成员必须属于项目所在部门。")
    for member_id in member_ids:
        db.session.add(
            ProjectMember(
                project_id=project.id,
                employee_id=member_id,
                responsibility="owner" if member_id == manager.id else "member",
            )
        )

    db.session.commit()
    return success(project_to_dict(project), "项目已创建")


@bp.put("/<int:project_id>")
@auth_required
def update_project(project_id):
    user = g.current_user
    if user.role.code not in ("admin", "manager"):
        raise APIError("当前角色无权编辑项目。", 403)
    project = scoped_query(user).filter(Project.id == project_id).first()
    if not project:
        raise APIError("项目不存在。", 404)

    payload = request.get_json(silent=True) or {}
    for field in ("name", "summary", "status", "priority"):
        if field in payload:
            setattr(project, field, payload[field].strip() if isinstance(payload[field], str) else payload[field])
    for field in ("progress", "manager_id", "department_id"):
        if field in payload and payload[field] not in (None, ""):
            setattr(project, field, int(payload[field]))
    if "budget" in payload and payload["budget"] not in (None, ""):
        project.budget = payload["budget"]
    if "start_date" in payload and payload["start_date"]:
        project.start_date = datetime.fromisoformat(payload["start_date"]).date()
    if "end_date" in payload:
        project.end_date = datetime.fromisoformat(payload["end_date"]).date() if payload["end_date"] else None
    if user.role.code == "manager" and project.department_id != user.department_id:
        raise APIError("部门负责人只能维护本部门项目。", 403)
    manager = Employee.query.get(project.manager_id)
    if not manager or manager.department_id != project.department_id:
        raise APIError("项目负责人必须属于项目所在部门。")

    if "member_ids" in payload:
        member_ids = {project.manager_id, *[int(member_id) for member_id in payload["member_ids"]]}
        members = Employee.query.filter(Employee.id.in_(member_ids)).all() if member_ids else []
        for member in members:
            if member.department_id != project.department_id:
                raise APIError("项目成员必须属于项目所在部门。")
        ProjectMember.query.filter(ProjectMember.project_id == project.id).delete()
        for member_id in member_ids:
            db.session.add(
                ProjectMember(
                    project_id=project.id,
                    employee_id=member_id,
                    responsibility="owner" if member_id == project.manager_id else "member",
                )
            )

    db.session.commit()
    project = Project.query.options(selectinload(Project.members).selectinload(ProjectMember.employee)).get(project.id)
    return success(project_to_dict(project), "项目已更新")
