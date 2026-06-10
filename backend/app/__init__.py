from flask import Flask
from flask_cors import CORS

from .blueprints.attendance import bp as attendance_bp
from .blueprints.auth import bp as auth_bp
from .blueprints.dashboard import bp as dashboard_bp
from .blueprints.employees import bp as employees_bp
from .blueprints.leaves import bp as leaves_bp
from .blueprints.meta import bp as meta_bp
from .blueprints.performance import bp as performance_bp
from .blueprints.projects import bp as projects_bp
from .config import Config
from .extensions import db
from .services.core import APIError, failure
from .services.seed import seed_database


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": [item.strip() for item in app.config["CORS_ORIGINS"].split(",") if item.strip()]}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(leaves_bp)

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return failure(error.message), error.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return failure("请求资源不存在。"), 404

    @app.cli.command("seed")
    def seed_command():
        seed_database(fresh=True)
        print("database seeded")

    return app
