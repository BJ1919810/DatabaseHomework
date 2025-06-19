# Library Management System (LMS)

## 项目简介
基于Python Tkinter和PostgreSQL开发的图书管理系统，提供管理员和用户双角色操作界面。

## 核心功能
### 管理员模块
- 📚 图书信息管理（CRUD）
- 📝 借阅记录管理
- 👥 用户账户管理

### 用户模块
- 🔍 图书查询
- 📖 图书借阅/归还
- 📊 借阅记录查看

## 技术架构
```mermaid
graph TD
    A[Tkinter GUI] --> B[业务逻辑层]
    B --> C[PostgreSQL数据库]
    C --> D[(book_k表)]
    C --> E[(record_k表)]
    C --> F[(user_k表)]
