# AGENTS.md

Django 项目。使用 SimpleUI 管理后台主题，中文界面。

## Project

- **Python** 3.14.0, **Django** 5.0.14, **SimpleUI** 2026.1.13
- **Database**: SQLite (`db.sqlite3`)
- **Entry point**: `manage.py` → `image_editor/settings.py`
- **Virtual env**: `.venv/` (项目根目录)

## Commands

```bash
# 激活虚拟环境
.venv\Scripts\activate

# Django
python manage.py check           # 系统检查
python manage.py runserver       # 启动 http://127.0.0.1:8000
python manage.py migrate         # 执行迁移
python manage.py makemigrations  # 创建迁移
python manage.py shell           # Django shell
python manage.py test            # 运行测试
python manage.py createsuperuser # 创建超管
```

## Architecture

```
image_editor/            # Django 项目包
├── settings.py          # INSTALLED_APPS: simpleui → admin → ... → editor
├── urls.py              # 仅 /admin/ 路由
├── wsgi.py / asgi.py    # 部署入口
editor/                  # Django 应用
├── models.py            # 待开发
├── views.py             # 待开发
├── admin.py             # 待开发
db.sqlite3               # SQLite 数据库
```

## Conventions

- SimpleUI 在 `INSTALLED_APPS` **首位**，必须在 `django.contrib.admin` 之前
- 语言 `zh-hans`，时区 `Asia/Shanghai`
- `ALLOWED_HOSTS = ['*']`（开发阶段）
- **不要**升级 Django ≥ 6.0 — SimpleUI 最高兼容 5.x

## Known Issues

### Python 3.14 × Django 5.0 补丁

文件：`.venv/Lib/site-packages/django/template/context.py:37-40`

`copy(super())` 在 Python 3.14 失效 → 500 错误。已替换为：

```python
def __copy__(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate
```

> 重装 Django 后需重新打补丁。

## Admin

- **URL**: http://127.0.0.1:8000/admin/
- **用户**: `123456` / `102030`（超管，`辛巴`，`3024768711@qq.com`）

## Notes

- 无 `requirements.txt`，依赖安装在 `.venv` 中
- `editor/` 为新建应用，models/views/admin 均待开发
- `urls.py` 当前仅注册 `/admin/` 路由
