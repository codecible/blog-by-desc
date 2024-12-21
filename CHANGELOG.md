# Changelog

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## Unreleased
### Added
- 项目代码重构，将现有Python代码迁移到`backend`目录
- 创建FastAPI标准目录结构
- 迁移现有生成逻辑到服务层
- 创建Vue 3项目，设置前端项目结构
- 配置Element Plus和必要依赖
- 创建Docker化项目结构
- 添加Docker Compose文件
- 添加VSCode Remote Container配置
- 添加VSCode Docker插件
- 添加README.md文档
- 添加项目结构.md文档
- 添加项目改造.md文档   

## [0.1.1] - 2024-12-21

### Added
- Monica AI API 集成
- 文章生成核心功能
- 缓存机制
- 异步处理支持
- 代码结构化
- 增加CHANGELOG.md更新日志维护

### Changed
- API 调用重试机制
- 日志记录系统

## [0.1.0] - 2024-12-20

### Added
- 项目初始化
- 基础项目结构搭建
- README.md 文档
- 配置文件支持
- 环境变量管理
- API 客户端封装
- 文章生成器核心类