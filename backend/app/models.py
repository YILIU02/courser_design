from datetime import date, datetime

from sqlalchemy import Index, UniqueConstraint

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Department(db.Model, TimestampMixin):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False, unique=True, index=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class Role(db.Model, TimestampMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False, unique=True, index=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class Employee(db.Model, TimestampMixin):
    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_employee_scope", "department_id", "role_id", "status"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(32), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(32), nullable=False, default="")
    title = db.Column(db.String(64), nullable=False, default="")
    education = db.Column(db.String(32), nullable=False, default="本科")
    status = db.Column(db.String(16), nullable=False, default="active", index=True)
    hire_date = db.Column(db.Date, nullable=False, default=date.today)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    department = db.relationship("Department", lazy="joined")
    role = db.relationship("Role", lazy="joined")


class Project(db.Model, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (
        Index("ix_project_scope", "department_id", "status"),
    )

    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(32), nullable=False, unique=True, index=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    summary = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(16), nullable=False, default="active", index=True)
    priority = db.Column(db.String(16), nullable=False, default="medium")
    progress = db.Column(db.Integer, nullable=False, default=0)
    budget = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    department = db.relationship("Department", lazy="joined")
    manager = db.relationship("Employee", foreign_keys=[manager_id], lazy="joined")
    members = db.relationship(
        "ProjectMember",
        cascade="all, delete-orphan",
        lazy="selectin",
        back_populates="project",
    )


class ProjectMember(db.Model):
    __tablename__ = "project_members"
    __table_args__ = (
        UniqueConstraint("project_id", "employee_id", name="uq_project_employee"),
        Index("ix_project_member_employee", "employee_id", "project_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    responsibility = db.Column(db.String(16), nullable=False, default="member")
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    project = db.relationship("Project", back_populates="members")
    employee = db.relationship("Employee", lazy="joined")


class AttendanceRecord(db.Model, TimestampMixin):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("employee_id", "work_date", name="uq_attendance_employee_date"),
        Index("ix_attendance_scope", "work_date", "employee_id"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    work_date = db.Column(db.Date, nullable=False, default=date.today)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(16), nullable=False, default="pending", index=True)
    remark = db.Column(db.String(255), nullable=False, default="")

    employee = db.relationship("Employee", lazy="joined")


class PerformanceRecord(db.Model, TimestampMixin):
    __tablename__ = "performance_records"
    __table_args__ = (
        UniqueConstraint("employee_id", "year", name="uq_performance_employee_year"),
        Index("ix_performance_scope", "department_id", "year"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False, index=True)
    business_score = db.Column(db.Float, nullable=False, default=0)
    skill_score = db.Column(db.Float, nullable=False, default=0)
    collaboration_score = db.Column(db.Float, nullable=False, default=0)
    attendance_score = db.Column(db.Float, nullable=False, default=0)
    total_score = db.Column(db.Float, nullable=False, default=0)
    grade = db.Column(db.String(16), nullable=False, default="C")
    comment = db.Column(db.String(255), nullable=False, default="")

    employee = db.relationship("Employee", foreign_keys=[employee_id], lazy="joined")
    reviewer = db.relationship("Employee", foreign_keys=[reviewer_id], lazy="joined")
    department = db.relationship("Department", lazy="joined")


class LeaveRequest(db.Model, TimestampMixin):
    __tablename__ = "leave_requests"
    __table_args__ = (
        Index("ix_leave_scope", "department_id", "status", "start_date"),
    )

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    leave_type = db.Column(db.String(32), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(16), nullable=False, default="pending", index=True)
    decision_comment = db.Column(db.String(255), nullable=False, default="")

    employee = db.relationship("Employee", foreign_keys=[employee_id], lazy="joined")
    approver = db.relationship("Employee", foreign_keys=[approver_id], lazy="joined")
    department = db.relationship("Department", lazy="joined")
