# 企业级员工协同管理系统

基于 `Vue 3 + Vite + Element Plus` 的前端控制台，配套 `Flask + SQLAlchemy + MySQL` 后端服务，覆盖以下业务域：

- 员工管理
- 项目管理
- 考勤管理
- 绩效管理
- 请假审批

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
SECRET_KEY=replace-with-strong-secret
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/course_design?charset=utf8mb4
CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

安装依赖并初始化种子数据：

```bash
pip install -r requirements.txt
flask --app backend/run.py seed
python backend/run.py
```

默认演示账号：

- 管理员：`admin / Admin@123`
- 研发负责人：`rd_manager / Manager@123`
- 普通员工：`rd_user / Staff@123`

## 前端启动

```bash
npm install
npm run dev
```

开发环境下前端通过 Vite 代理访问 `http://127.0.0.1:5000/api`。

## 工程说明

- 统一响应结构、统一权限校验、统一路由守卫
- 使用数据库索引、聚合查询、批量预加载降低 N+1 请求
- 按管理员、部门负责人、员工三种角色控制数据范围
- 前端采用统一后台布局与正式系统样式
