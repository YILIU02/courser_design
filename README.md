# 企业级员工协同管理系统

基于 `Vue 3 + Vite + Element Plus + Flask + SQLAlchemy + MySQL` 的员工管理平台，覆盖员工、项目、考勤、绩效与请假审批等业务模块。

## 目录结构

```text
src/        前端应用
backend/    Flask 后端
```

## 后端要求

- Python `3.11+`
- MySQL `5.7+` 或 `8.x`

创建数据库：

```sql
CREATE DATABASE course_design CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

复制配置文件并修改数据库连接：

```bash
cp .env.example .env
```

`.env` 示例：

```env
APP_ENV=production
SECRET_KEY=replace-with-strong-secret
DATABASE_URL=mysql+pymysql://course_app:replace-with-strong-db-password@127.0.0.1:3306/course_design?charset=utf8mb4
CORS_ORIGINS=http://8.134.191.89:8080
DEMO_PASSWORD=replace-with-a-unique-12-character-or-longer-password
```

安装依赖并初始化种子数据：

```bash
pip install -r requirements.txt
flask --app backend/run.py seed
python backend/run.py
```

## 演示账号

本地演示可设置 `DEMO_PASSWORD` 后执行种子命令，并使用以下账号：

- 管理员：`admin / CdAdmin#2026!A7`
- 研发负责人：`rd_manager / CdMgr#2026!A7`
- 普通员工：`rd_user / CdEmp#2026!A7`

线上环境应设置不同的 `DEMO_PASSWORD`，并可通过 `flask --app backend/run.py rotate-demo-password` 轮换已有演示账号密码。

## 前端启动

```bash
npm install
npm run dev
```

开发环境下前端通过 Vite 代理访问 `http://127.0.0.1:5000/api`。

## 工程说明

- 统一响应结构、权限校验与路由守卫
- 使用数据库索引、聚合查询、批量预加载降低 N+1 请求
- 按管理员、部门负责人、员工三种角色控制数据范围
- 前端采用统一后台布局与正式系统样式

## 生产安全与部署

- 生产环境必须设置 `APP_ENV=production`、随机 `SECRET_KEY` 和独立数据库账号的 `DATABASE_URL`，缺失时后端拒绝启动。
- 登录按 IP 与账号限制为 15 分钟 8 次，`deploy/nginx.conf` 还提供独立的入口限流。
- 登录状态保存在 `sessionStorage`，关闭浏览器会话后自动清除。
- 后端仅监听 `127.0.0.1:5000`，公网只暴露 Nginx 的 `8080` 端口。
- 当前仅有公网 IP，保留 HTTP 可访问。取得域名和可信证书后，应启用 HTTPS、HTTP 跳转和 HSTS。
