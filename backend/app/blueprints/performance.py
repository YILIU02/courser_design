from datetime import date

from flask import Blueprint, g, request
from sqlalchemy import and_, func

from ..models import Employee, PerformanceRecord
from ..services.core import auth_required, success
from ..services.serializers import performance_to_dict


bp = Blueprint("performance", __name__, url_prefix="/api/performance")


def base_query(user):
    query = PerformanceRecord.query.join(Employee, Employee.id == PerformanceRecord.employee_id)
    if user.role.code == "manager":
        query = query.filter(PerformanceRecord.department_id == user.department_id)
    elif user.role.code == "employee":
        query = query.filter(PerformanceRecord.employee_id == user.id)
    return query


@bp.get("")
@auth_required
def list_performance():
    user = g.current_user
    query = base_query(user)
    year = request.args.get("year", type=int)
    latest_only = request.args.get("latest_only", default=1, type=int)
    employee_id = request.args.get("employee_id", type=int)

    if employee_id:
        query = query.filter(PerformanceRecord.employee_id == employee_id)
    if year:
        query = query.filter(PerformanceRecord.year == year)
    elif latest_only:
        subquery = (
            base_query(user)
            .with_entities(
                PerformanceRecord.employee_id.label("employee_id"),
                func.max(PerformanceRecord.year).label("max_year"),
            )
            .group_by(PerformanceRecord.employee_id)
            .subquery()
        )
        query = query.join(
            subquery,
            and_(
                PerformanceRecord.employee_id == subquery.c.employee_id,
                PerformanceRecord.year == subquery.c.max_year,
            ),
        )

    records = query.order_by(PerformanceRecord.year.desc(), PerformanceRecord.total_score.desc()).all()
    years = [
        row[0]
        for row in base_query(user)
        .with_entities(PerformanceRecord.year)
        .distinct()
        .order_by(PerformanceRecord.year.desc())
        .all()
    ]
    current_year = year or (years[0] if years else date.today().year)
    average_score = round(sum(record.total_score for record in records) / len(records), 2) if records else 0
    return success({"items": [performance_to_dict(record) for record in records], "years": years, "current_year": current_year, "average_score": average_score})
