from datetime import date, datetime, timedelta
from decimal import Decimal

from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models import (
    AttendanceRecord,
    Department,
    Employee,
    LeaveRequest,
    PerformanceRecord,
    Project,
    ProjectMember,
    Role,
)


def score_grade(total_score):
    if total_score >= 90:
        return "A"
    if total_score >= 80:
        return "B"
    if total_score >= 70:
        return "C"
    return "D"


def seed_database(fresh=False):
    if fresh:
        db.drop_all()
    db.create_all()

    if Role.query.count() and Department.query.count() and Employee.query.count():
        return

    roles = [
        Role(code="admin", name="系统管理员"),
        Role(code="manager", name="部门负责人"),
        Role(code="employee", name="员工"),
    ]
    departments = [
        Department(code="rd", name="研发部"),
        Department(code="marketing", name="市场部"),
        Department(code="finance", name="财务部"),
        Department(code="operations", name="运营部"),
    ]
    db.session.add_all(roles + departments)
    db.session.flush()

    role_map = {role.code: role for role in roles}
    dept_map = {dept.code: dept for dept in departments}

    employees = [
        Employee(
            employee_no="A1001",
            username="admin",
            password_hash=generate_password_hash("Admin@123"),
            full_name="刘奕",
            email="admin@enterprise.local",
            phone="13800000001",
            title="系统管理员",
            education="硕士",
            department_id=dept_map["rd"].id,
            role_id=role_map["admin"].id,
            hire_date=date(2022, 3, 1),
        ),
        Employee(
            employee_no="M2001",
            username="rd_manager",
            password_hash=generate_password_hash("Manager@123"),
            full_name="周敏",
            email="rd_manager@enterprise.local",
            phone="13800000002",
            title="研发负责人",
            education="硕士",
            department_id=dept_map["rd"].id,
            role_id=role_map["manager"].id,
            hire_date=date(2022, 5, 1),
        ),
        Employee(
            employee_no="E3001",
            username="rd_user",
            password_hash=generate_password_hash("Staff@123"),
            full_name="陈楠",
            email="rd_user@enterprise.local",
            phone="13800000003",
            title="后端工程师",
            education="本科",
            department_id=dept_map["rd"].id,
            role_id=role_map["employee"].id,
            hire_date=date(2023, 2, 15),
        ),
        Employee(
            employee_no="M2101",
            username="ops_manager",
            password_hash=generate_password_hash("Manager@123"),
            full_name="何璐",
            email="ops_manager@enterprise.local",
            phone="13800000004",
            title="运营负责人",
            education="本科",
            department_id=dept_map["operations"].id,
            role_id=role_map["manager"].id,
            hire_date=date(2021, 9, 1),
        ),
        Employee(
            employee_no="E3101",
            username="ops_user",
            password_hash=generate_password_hash("Staff@123"),
            full_name="王凯",
            email="ops_user@enterprise.local",
            phone="13800000005",
            title="运营专员",
            education="本科",
            department_id=dept_map["operations"].id,
            role_id=role_map["employee"].id,
            hire_date=date(2023, 8, 2),
        ),
        Employee(
            employee_no="E3201",
            username="finance_user",
            password_hash=generate_password_hash("Staff@123"),
            full_name="李欣",
            email="finance_user@enterprise.local",
            phone="13800000006",
            title="财务分析师",
            education="硕士",
            department_id=dept_map["finance"].id,
            role_id=role_map["employee"].id,
            hire_date=date(2024, 1, 3),
        ),
    ]
    db.session.add_all(employees)
    db.session.flush()

    user_map = {employee.username: employee for employee in employees}

    projects = [
        Project(
            project_code="PRJ-2026-001",
            name="企业主数据中台",
            summary="统一员工、组织与绩效数据口径，支撑多部门协同。",
            status="active",
            priority="high",
            progress=72,
            budget=Decimal("580000.00"),
            start_date=date.today() - timedelta(days=120),
            end_date=date.today() + timedelta(days=60),
            department_id=dept_map["rd"].id,
            manager_id=user_map["rd_manager"].id,
        ),
        Project(
            project_code="PRJ-2026-002",
            name="运营排班优化",
            summary="通过规则引擎和数据分析降低人力排班成本。",
            status="active",
            priority="medium",
            progress=48,
            budget=Decimal("260000.00"),
            start_date=date.today() - timedelta(days=75),
            end_date=date.today() + timedelta(days=45),
            department_id=dept_map["operations"].id,
            manager_id=user_map["ops_manager"].id,
        ),
        Project(
            project_code="PRJ-2026-003",
            name="预算执行看板",
            summary="面向财务与管理层的预算执行可视化系统。",
            status="planned",
            priority="medium",
            progress=18,
            budget=Decimal("180000.00"),
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=90),
            department_id=dept_map["finance"].id,
            manager_id=user_map["admin"].id,
        ),
    ]
    db.session.add_all(projects)
    db.session.flush()

    members = [
        ProjectMember(project_id=projects[0].id, employee_id=user_map["rd_manager"].id, responsibility="owner"),
        ProjectMember(project_id=projects[0].id, employee_id=user_map["rd_user"].id, responsibility="member"),
        ProjectMember(project_id=projects[0].id, employee_id=user_map["admin"].id, responsibility="sponsor"),
        ProjectMember(project_id=projects[1].id, employee_id=user_map["ops_manager"].id, responsibility="owner"),
        ProjectMember(project_id=projects[1].id, employee_id=user_map["ops_user"].id, responsibility="member"),
        ProjectMember(project_id=projects[2].id, employee_id=user_map["finance_user"].id, responsibility="member"),
        ProjectMember(project_id=projects[2].id, employee_id=user_map["admin"].id, responsibility="owner"),
    ]
    db.session.add_all(members)

    for delta in range(0, 15):
        work_date = date.today() - timedelta(days=delta)
        if work_date.weekday() >= 5:
            continue
        for username in ("rd_user", "ops_user", "finance_user", "rd_manager", "ops_manager"):
            employee = user_map[username]
            check_in = datetime.combine(work_date, datetime.min.time()).replace(hour=8, minute=40 + (employee.id % 5))
            check_out = datetime.combine(work_date, datetime.min.time()).replace(hour=18, minute=5 + (employee.id % 7))
            db.session.add(
                AttendanceRecord(
                    employee_id=employee.id,
                    work_date=work_date,
                    check_in=check_in,
                    check_out=check_out if delta != 0 else None,
                    status="present" if delta != 0 else "checked_in",
                    remark="",
                )
            )

    for year in (2024, 2025, 2026):
        for username in ("rd_user", "ops_user", "finance_user", "rd_manager", "ops_manager"):
            employee = user_map[username]
            business = 78 + ((employee.id + year) % 12)
            skill = 80 + ((employee.id + year * 2) % 10)
            collaboration = 76 + ((employee.id + year * 3) % 14)
            attendance = 82 + ((employee.id + year * 4) % 10)
            total = round(business * 0.35 + skill * 0.3 + collaboration * 0.2 + attendance * 0.15, 2)
            reviewer = user_map["admin"] if employee.role.code == "manager" else user_map["rd_manager"] if employee.department.code == "rd" else user_map["ops_manager"] if employee.department.code == "operations" else user_map["admin"]
            db.session.add(
                PerformanceRecord(
                    employee_id=employee.id,
                    reviewer_id=reviewer.id,
                    department_id=employee.department_id,
                    year=year,
                    business_score=business,
                    skill_score=skill,
                    collaboration_score=collaboration,
                    attendance_score=attendance,
                    total_score=total,
                    grade=score_grade(total),
                    comment="年度绩效稳定，建议持续提升跨团队协作效率。",
                )
            )

    db.session.add_all(
        [
            LeaveRequest(
                employee_id=user_map["rd_user"].id,
                approver_id=user_map["rd_manager"].id,
                department_id=user_map["rd_user"].department_id,
                leave_type="年假",
                start_date=date.today() + timedelta(days=3),
                end_date=date.today() + timedelta(days=4),
                days=2,
                reason="家庭事务处理",
                status="pending",
            ),
            LeaveRequest(
                employee_id=user_map["ops_user"].id,
                approver_id=user_map["ops_manager"].id,
                department_id=user_map["ops_user"].department_id,
                leave_type="调休",
                start_date=date.today() - timedelta(days=7),
                end_date=date.today() - timedelta(days=7),
                days=1,
                reason="个人事务办理",
                status="approved",
                decision_comment="已批准，注意提前交接。",
            ),
        ]
    )
    db.session.commit()
