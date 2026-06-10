from datetime import datetime

from flask import Blueprint, g, request

from ..extensions import db
from ..models import Employee, LeaveRequest
from ..services.core import APIError, auth_required, require_fields, success
from ..services.serializers import leave_to_dict


bp = Blueprint("leaves", __name__, url_prefix="/api/leaves")


def resolve_approver(user):
    manager = (
        Employee.query.filter(
            Employee.department_id == user.department_id,
            Employee.role.has(code="manager"),
            Employee.status == "active",
        )
        .order_by(Employee.id.asc())
        .first()
    )
    if manager and manager.id != user.id:
        return manager
    admin = Employee.query.filter(Employee.role.has(code="admin"), Employee.status == "active").order_by(Employee.id.asc()).first()
    if not admin:
        raise APIError("未找到可用审批人。", 500)
    return admin


@bp.get("")
@auth_required
def list_leaves():
    user = g.current_user
    scope = request.args.get("scope", "mine")
    status = request.args.get("status", "").strip()
    query = LeaveRequest.query

    if scope == "approvals":
        if user.role.code == "employee":
            raise APIError("当前角色无权查看审批列表。", 403)
        if user.role.code == "manager":
            query = query.filter(LeaveRequest.department_id == user.department_id)
    else:
        query = query.filter(LeaveRequest.employee_id == user.id)

    if status:
        query = query.filter(LeaveRequest.status == status)

    rows = query.order_by(LeaveRequest.created_at.desc()).all()
    return success([leave_to_dict(row) for row in rows])


@bp.post("")
@auth_required
def create_leave():
    user = g.current_user
    payload = request.get_json(silent=True) or {}
    require_fields(payload, "leave_type", "start_date", "end_date", "reason")
    start_date = datetime.fromisoformat(payload["start_date"]).date()
    end_date = datetime.fromisoformat(payload["end_date"]).date()
    if end_date < start_date:
        raise APIError("结束日期不能早于开始日期。")

    approver = resolve_approver(user)
    leave_request = LeaveRequest(
        employee_id=user.id,
        approver_id=approver.id,
        department_id=user.department_id,
        leave_type=payload["leave_type"].strip(),
        start_date=start_date,
        end_date=end_date,
        days=float((end_date - start_date).days + 1),
        reason=payload["reason"].strip(),
        status="pending",
    )
    db.session.add(leave_request)
    db.session.commit()
    return success(leave_to_dict(leave_request), "请假申请已提交")


@bp.post("/<int:leave_id>/decision")
@auth_required
def approve_leave(leave_id):
    user = g.current_user
    if user.role.code == "employee":
        raise APIError("当前角色无权审批请假。", 403)
    payload = request.get_json(silent=True) or {}
    require_fields(payload, "status")
    leave_request = LeaveRequest.query.get(leave_id)
    if not leave_request:
        raise APIError("请假记录不存在。", 404)
    if user.role.code == "manager" and leave_request.department_id != user.department_id:
        raise APIError("只能审批本部门请假。", 403)
    if payload["status"] not in ("approved", "rejected"):
        raise APIError("审批状态无效。")

    leave_request.status = payload["status"]
    leave_request.decision_comment = payload.get("decision_comment", "").strip()
    leave_request.approver_id = user.id
    db.session.commit()
    return success(leave_to_dict(leave_request), "审批结果已提交")
