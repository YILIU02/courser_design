from datetime import date, datetime

from flask import Blueprint, g, request
from sqlalchemy import and_, or_

from ..extensions import db
from ..models import AttendanceRecord, Employee
from ..services.core import APIError, auth_required, success
from ..services.serializers import attendance_to_dict


bp = Blueprint("attendance", __name__, url_prefix="/api/attendance")


def list_query(user):
    query = AttendanceRecord.query.join(Employee, Employee.id == AttendanceRecord.employee_id)
    if user.role.code == "manager":
        query = query.filter(Employee.department_id == user.department_id)
    elif user.role.code == "employee":
        query = query.filter(AttendanceRecord.employee_id == user.id)
    return query


@bp.get("")
@auth_required
def list_attendance():
    user = g.current_user
    query = list_query(user)
    keyword = request.args.get("keyword", "").strip()
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if keyword:
        like_value = f"%{keyword}%"
        query = query.filter(or_(Employee.full_name.like(like_value), Employee.employee_no.like(like_value)))
    if start_date and end_date:
        query = query.filter(
            and_(
                AttendanceRecord.work_date >= datetime.fromisoformat(start_date).date(),
                AttendanceRecord.work_date <= datetime.fromisoformat(end_date).date(),
            )
        )

    records = query.order_by(AttendanceRecord.work_date.desc(), AttendanceRecord.id.desc()).limit(120).all()
    today_record = AttendanceRecord.query.filter_by(employee_id=user.id, work_date=date.today()).first()
    return success(
        {
            "today": attendance_to_dict(today_record) if today_record else None,
            "items": [attendance_to_dict(record) for record in records],
        }
    )


@bp.post("/check-in")
@auth_required
def check_in():
    user = g.current_user
    if user.role.code == "admin":
        raise APIError("管理员账号不参与个人打卡。", 400)
    today = date.today()
    record = AttendanceRecord.query.filter_by(employee_id=user.id, work_date=today).first()
    if record and record.check_in:
        raise APIError("今天已完成签到。")
    if not record:
        record = AttendanceRecord(employee_id=user.id, work_date=today)
        db.session.add(record)
    record.check_in = datetime.now()
    record.status = "checked_in"
    db.session.commit()
    return success(attendance_to_dict(record), "签到成功")


@bp.post("/check-out")
@auth_required
def check_out():
    user = g.current_user
    if user.role.code == "admin":
        raise APIError("管理员账号不参与个人打卡。", 400)
    record = AttendanceRecord.query.filter_by(employee_id=user.id, work_date=date.today()).first()
    if not record or not record.check_in:
        raise APIError("请先完成签到。")
    if record.check_out:
        raise APIError("今天已完成签退。")
    record.check_out = datetime.now()
    record.status = "present"
    db.session.commit()
    return success(attendance_to_dict(record), "签退成功")
