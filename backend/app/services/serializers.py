def employee_to_dict(employee):
    return {
        "id": employee.id,
        "employee_no": employee.employee_no,
        "username": employee.username,
        "full_name": employee.full_name,
        "email": employee.email,
        "phone": employee.phone,
        "title": employee.title,
        "education": employee.education,
        "status": employee.status,
        "hire_date": employee.hire_date.isoformat(),
        "department_id": employee.department_id,
        "department_name": employee.department.name,
        "role_id": employee.role_id,
        "role_code": employee.role.code,
        "role_name": employee.role.name,
    }


def project_to_dict(project):
    members = [
        {
            "id": member.employee.id,
            "employee_no": member.employee.employee_no,
            "full_name": member.employee.full_name,
            "department_name": member.employee.department.name,
            "responsibility": member.responsibility,
        }
        for member in project.members
    ]
    return {
        "id": project.id,
        "project_code": project.project_code,
        "name": project.name,
        "summary": project.summary,
        "status": project.status,
        "priority": project.priority,
        "progress": project.progress,
        "budget": float(project.budget),
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat() if project.end_date else None,
        "department_id": project.department_id,
        "department_name": project.department.name,
        "manager_id": project.manager_id,
        "manager_name": project.manager.full_name,
        "member_count": len(members),
        "members": members,
    }


def attendance_to_dict(record):
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "employee_no": record.employee.employee_no,
        "employee_name": record.employee.full_name,
        "department_name": record.employee.department.name,
        "work_date": record.work_date.isoformat(),
        "check_in": record.check_in.isoformat() if record.check_in else None,
        "check_out": record.check_out.isoformat() if record.check_out else None,
        "status": record.status,
        "remark": record.remark,
    }


def performance_to_dict(record):
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "employee_no": record.employee.employee_no,
        "employee_name": record.employee.full_name,
        "department_name": record.department.name,
        "reviewer_name": record.reviewer.full_name,
        "year": record.year,
        "business_score": record.business_score,
        "skill_score": record.skill_score,
        "collaboration_score": record.collaboration_score,
        "attendance_score": record.attendance_score,
        "total_score": record.total_score,
        "grade": record.grade,
        "comment": record.comment,
    }


def leave_to_dict(record):
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "employee_name": record.employee.full_name,
        "employee_no": record.employee.employee_no,
        "department_name": record.department.name,
        "approver_id": record.approver_id,
        "approver_name": record.approver.full_name,
        "leave_type": record.leave_type,
        "start_date": record.start_date.isoformat(),
        "end_date": record.end_date.isoformat(),
        "days": record.days,
        "reason": record.reason,
        "status": record.status,
        "decision_comment": record.decision_comment,
        "created_at": record.created_at.isoformat(),
    }
