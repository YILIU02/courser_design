from functools import wraps

from flask import current_app, g, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from ..models import Employee


class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def success(data=None, message="ok"):
    return {"code": 0, "message": message, "data": data}


def failure(message, data=None):
    return {"code": 1, "message": message, "data": data}


def serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="course-design-auth")


def issue_token(user):
    return serializer().dumps({"user_id": user.id})


def resolve_token(token):
    try:
        payload = serializer().loads(token, max_age=current_app.config["TOKEN_MAX_AGE"])
    except SignatureExpired as exc:
        raise APIError("登录状态已过期，请重新登录。", 401) from exc
    except BadSignature as exc:
        raise APIError("无效的登录令牌。", 401) from exc
    user = Employee.query.get(payload["user_id"])
    if not user or user.status != "active":
        raise APIError("当前账号不可用。", 401)
    return user


def auth_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not token:
            token = request.headers.get("token", "").strip()
        if not token:
            raise APIError("缺少登录令牌。", 401)
        g.current_user = resolve_token(token)
        return view(*args, **kwargs)

    return wrapped


def role_required(*role_codes):
    def decorator(view):
        @wraps(view)
        @auth_required
        def wrapped(*args, **kwargs):
            if g.current_user.role.code not in role_codes:
                raise APIError("当前角色无权执行该操作。", 403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def apply_scope(query, user, model):
    if user.role.code == "admin":
        return query
    if user.role.code == "manager":
        return query.filter(model.department_id == user.department_id)
    return query.filter(model.id == user.id)


def require_fields(payload, *fields):
    missing = [field for field in fields if payload.get(field) in (None, "", [])]
    if missing:
        raise APIError(f"缺少必填字段: {', '.join(missing)}")


def employee_summary(user):
    return {
        "id": user.id,
        "employee_no": user.employee_no,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "title": user.title,
        "education": user.education,
        "department_id": user.department_id,
        "department_name": user.department.name,
        "role_id": user.role_id,
        "role_code": user.role.code,
        "role_name": user.role.name,
        "status": user.status,
        "hire_date": user.hire_date.isoformat(),
    }
