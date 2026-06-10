from datetime import date

from flask import Blueprint, g
from sqlalchemy import func

from ..models import AttendanceRecord, Employee, LeaveRequest, PerformanceRecord, Project, ProjectMember
from ..services.core import auth_required, success
from ..services.serializers import attendance_to_dict, performance_to_dict, project_to_dict


bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@bp.get("/overview")
@auth_required
def overview():
    user = g.current_user

    employee_query = Employee.query.filter(Employee.status == "active")
    project_query = Project.query
    attendance_query = AttendanceRecord.query.filter(AttendanceRecord.work_date == date.today())
    leave_query = LeaveRequest.query.filter(LeaveRequest.status == "pending")
    performance_query = PerformanceRecord.query

    if user.role.code == "manager":
        employee_query = employee_query.filter(Employee.department_id == user.department_id)
        project_query = project_query.filter(Project.department_id == user.department_id)
        attendance_query = attendance_query.join(Employee, Employee.id == AttendanceRecord.employee_id).filter(Employee.department_id == user.department_id)
        leave_query = leave_query.filter(LeaveRequest.department_id == user.department_id)
        performance_query = performance_query.filter(PerformanceRecord.department_id == user.department_id)
    elif user.role.code == "employee":
        project_query = (
            project_query.join(ProjectMember, ProjectMember.project_id == Project.id)
            .filter(ProjectMember.employee_id == user.id)
            .distinct()
        )
        attendance_query = attendance_query.filter(AttendanceRecord.employee_id == user.id)
        leave_query = leave_query.filter(LeaveRequest.employee_id == user.id)
        performance_query = performance_query.filter(PerformanceRecord.employee_id == user.id)
        employee_query = employee_query.filter(Employee.id == user.id)

    project_status = (
        project_query.with_entities(Project.status, func.count(Project.id))
        .group_by(Project.status)
        .all()
    )
    latest_year = performance_query.with_entities(func.max(PerformanceRecord.year)).scalar()
    latest_records = []
    if latest_year:
        latest_records = (
            performance_query.filter(PerformanceRecord.year == latest_year)
            .order_by(PerformanceRecord.total_score.desc())
            .limit(5)
            .all()
        )

    recent_projects = project_query.order_by(Project.updated_at.desc()).limit(4).all()
    my_today = AttendanceRecord.query.filter_by(employee_id=user.id, work_date=date.today()).first()
    attendance_total = attendance_query.count()
    attendance_completed = attendance_query.filter(AttendanceRecord.check_in.isnot(None)).count()

    return success(
        {
            "stats": {
                "employee_total": employee_query.count(),
                "project_total": project_query.count(),
                "pending_leave_total": leave_query.count(),
                "attendance_total": attendance_total,
                "attendance_completed": attendance_completed,
            },
            "project_status": [{"status": status, "count": count} for status, count in project_status],
            "recent_projects": [project_to_dict(project) for project in recent_projects],
            "latest_performance": [performance_to_dict(record) for record in latest_records],
            "today_attendance": attendance_to_dict(my_today) if my_today else None,
        }
    )
