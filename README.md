# SELab

山东大学 2026 春软工实验 —— 人才招聘系统。

## 技术栈

- **后端**：Django 5.1 + Django REST Framework + MySQL（PyMySQL 驱动）
- **前端**：Vue 3 + Vite + TypeScript + Ant Design Vue + Pinia

## 目录结构

```
├── manage.py            # Django 启动入口
├── requirements.txt     # 后端依赖
├── server/              # Django 工程配置（settings / urls / wsgi）
├── myapp/               # 后端业务应用（models / views / urls / 中间件）
└── frontend/            # 前端工程
```

## 环境要求

- Python 3.10+（开发环境用的 3.13）
- Node.js 16+ 与 yarn
- MySQL 8（推荐用 Docker 起，见下）

## 后端启动

### 1. 准备数据库

用 Docker 起一个 MySQL（库名、账号密码与 `server/settings.py` 对齐）：

```bash
docker run -d --name mysql-job -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=4643830 \
  -e MYSQL_DATABASE=python_job \
  mysql:8
```

> 已有本地 MySQL 也可以，自行建库 `python_job` 并保证 `root / 4643830 / 127.0.0.1:3306` 可连，
> 或修改 `server/settings.py` 里的 `DATABASES` 配置。

### 2. 装依赖

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 建表并启动

```bash
python manage.py migrate           # 根据迁移文件建表
python manage.py runserver 127.0.0.1:8000
```

后端跑在 `http://127.0.0.1:8000`，接口前缀 `/myapp/`。

- 默认管理员：首次访问 `/myapp/admin/adminLogin` 自动创建 `admin / 123`
- 普通用户：通过前端注册，或 `POST /myapp/index/user/register` 创建

## 前端启动

```bash
cd frontend
yarn
yarn dev
```

前端默认请求 `http://127.0.0.1:8000`（见 `frontend/src/store/constants.ts` 的 `BASE_URL`），
确保后端已启动。

## 说明

- 数据存在 MySQL 中，不随仓库走；clone 后需自行起库并 `migrate`。
- 迁移文件 `myapp/migrations/` 已纳入版本库，是建表依据，请勿删除。
