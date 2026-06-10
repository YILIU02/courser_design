from werkzeug.security import check_password_hash

from flask import Blueprint, g, request

from ..models import Employee
from ..services.core import APIError, auth_required, employee_summary, issue_token, require_fields, success


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, "username", "password")
    user = Employee.query.filter_by(username=payload["username"].strip()).first()
    if not user or not check_password_hash(user.password_hash, payload["password"]):
        raise APIError("账号或密码错误。", 401)
    if user.status != "active":
        raise APIError("当前账号已被禁用。", 403)
    return success({"token": issue_token(user), "user": employee_summary(user)}, "登录成功")


@bp.get("/me")
@auth_required
def me():
    return success(employee_summary(g.current_user))
