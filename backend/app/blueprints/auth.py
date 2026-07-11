import threading
import time
from collections import defaultdict, deque

from werkzeug.security import check_password_hash

from flask import Blueprint, current_app, g, request

from ..models import Employee
from ..services.core import APIError, auth_required, employee_summary, issue_token, require_fields, success


bp = Blueprint("auth", __name__, url_prefix="/api/auth")
login_attempts = defaultdict(deque)
login_attempts_lock = threading.Lock()


def login_rate_key(username):
    forwarded = request.headers.get("X-Forwarded-For", "").split(",", 1)[0].strip()
    return f"{forwarded or request.remote_addr or 'unknown'}:{username.lower()}"


def is_rate_limited(key):
    cutoff = time.time() - current_app.config["LOGIN_RATE_WINDOW_SECONDS"]
    with login_attempts_lock:
        attempts = login_attempts[key]
        while attempts and attempts[0] <= cutoff:
            attempts.popleft()
        return len(attempts) >= current_app.config["LOGIN_RATE_MAX_ATTEMPTS"]


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    require_fields(payload, "username", "password")
    username = str(payload["username"]).strip()[:64]
    rate_key = login_rate_key(username)
    if is_rate_limited(rate_key):
        raise APIError("登录尝试过于频繁，请稍后再试。", 429)
    user = Employee.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, payload["password"]):
        with login_attempts_lock:
            login_attempts[rate_key].append(time.time())
        raise APIError("账号或密码错误。", 401)
    if user.status != "active":
        raise APIError("当前账号已被禁用。", 403)
    with login_attempts_lock:
        login_attempts.pop(rate_key, None)
    return success({"token": issue_token(user), "user": employee_summary(user)}, "登录成功")


@bp.get("/me")
@auth_required
def me():
    return success(employee_summary(g.current_user))
