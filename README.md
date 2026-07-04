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

## 演示账号

- 管理员：`admin / CdAdmin#2026!A7`
- 研发负责人：`rd_manager / CdMgr#2026!A7`
- 普通员工：`rd_user / CdEmp#2026!A7`

以上凭据仅用于仓库演示说明，线上界面不应展示或自动填充。

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
